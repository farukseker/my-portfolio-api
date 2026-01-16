import os
import re
from dataclasses import dataclass
from typing import Any
from django.utils import timezone
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from config.settings.base import BASE_DIR
from langchain.messages import SystemMessage
from chatwithme import llm_models

PROMPT_DIR = BASE_DIR / "chatwithme/prompt_templates"


def load_include(path: str) -> str:
    full_path = os.path.join(PROMPT_DIR, path)
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()


def load_row_rules():
    """
    Load rule files with caching and add current datetime context.
    Datetime info is added fresh each time to ensure it's always current.
    """
    from django.core.cache import cache
    
    cache_key = "chatwithme_row_rules"
    row_rules = cache.get(cache_key)
    
    if row_rules is None:
        row_rules = []
        for fname in sorted(os.listdir(PROMPT_DIR)):
            if fname.endswith('.rule'):
                full_path = os.path.join(PROMPT_DIR, fname)
                with open(full_path, "r", encoding="utf-8") as f:
                    row_rules.append(f.read().strip())
        cache.set(cache_key, row_rules, timeout=3600)
    
    # Add current datetime info (always fresh, not cached)
    now = timezone.now()
    datetime_info = f"CURRENT_DATE_TIME: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}\nCURRENT_DAY_OF_WEEK: {now.strftime('%A')}\nCURRENT_YEAR: {now.year}\nCURRENT_MONTH: {now.strftime('%B')}\n"
    
    return [datetime_info] + row_rules


@dataclass
class PromptDef:
    name: str
    prompt_text: str
    messages: list[tuple[str, str]] | None
    input_vars: list[str] | None
    model: BaseModel | None
    triggers: list[str] | None
    rules: str | None
    is_chat: bool
    llm: Any = None

    def _template(self):
        """
        Build ChatPromptTemplate or PromptTemplate based on type.
        """
        if self.is_chat:
            final_messages = []

            # Add row rules first
            for rr in load_row_rules():
                final_messages.append(SystemMessage(rr.strip()))

            # Add prompt-specific rules
            if self.rules:
                final_messages.append(("system", f"EXTRA RULES:\n{self.rules.strip()}"))

            # Add user-defined messages from file
            if self.messages:
                for message in self.messages:
                    final_messages.append(message)

            return ChatPromptTemplate.from_messages(final_messages)

        else:
            # Classic template (non-chat)
            content = (
                    "\n".join(load_row_rules()) + "\n" +
                    "\n".join([x.content for x in self.messages] if self.messages else '') +
                    self.prompt_text
            )

            return PromptTemplate(
                template=content,
                input_variables=self.input_vars or []
            )


    @property
    def parser(self):
        if self.model and issubclass(self.model, BaseModel):
            return PydanticOutputParser(pydantic_object=self.model)
        return None

    @property
    def chain(self):
        template = self._template()
        if not self.parser:
            return template | self.llm
        return template | self.llm | self.parser


class PromptManager:
    def __init__(self, llm_ref):
        self.llm_ref = llm_ref
        self.prompts: dict[str, PromptDef] = {}
        self.load_all_prompts()

    def load_all_prompts(self):
        for root, _, files in os.walk(PROMPT_DIR):
            for fname in files:
                if fname.endswith(".prompt"):
                    self._load_single_prompt(os.path.join(root, fname))

    def _load_single_prompt(self, filepath):
        name = os.path.basename(filepath).replace(".prompt", "")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        p = self.parse_prompt(name, content)
        p.llm = self.llm_ref
        self.prompts[name] = p

    def parse_prompt(self, name: str, context: str) -> PromptDef:
        model = None
        input_vars = None
        triggers = None
        rules = None
        is_chat = False
        messages = []
        body = []

        # Process includes
        includes = re.findall(r"\{include:([^}]+)\}", context)
        for inc in includes:
            context = context.replace(f"{{include:{inc}}}", load_include(inc))

        lines = context.split("\n")
        multiline_role = None
        multi_buffer = []

        for line in lines:
            # Parse metadata lines starting with !
            if line.startswith("!"):
                key, val = line.split(":", 1)
                val = val.strip()

                if key == "!input_variables":
                    input_vars = [x.strip() for x in val.split(",")]
                elif key == "!triggers":
                    triggers = [x.strip() for x in val.split(",")]
                elif key == "!model":
                    if hasattr(llm_models, val):
                        model = getattr(llm_models, val)
                elif key == "!chat":
                    is_chat = val.lower() == "true"
                elif key == "!rules":
                    rules = val
                continue

            # Close multiline block
            if multiline_role and line.strip() == "":
                messages.append((multiline_role, "\n".join(multi_buffer)))
                multiline_role = None
                multi_buffer = []
                continue

            # Detect multiline start "role: |"
            if is_chat and ":" in line and "|" in line:
                role, rest = line.split(":", 1)
                role = role.strip()
                if role in ("system", "human", "assistant"):
                    if rest.strip() == "|":
                        multiline_role = role
                        multi_buffer = []
                        continue

            # Append to multiline buffer
            if multiline_role:
                multi_buffer.append(line)
                continue

            # Parse single-line chat message
            if is_chat and ":" in line:
                role, msg = line.split(":", 1)
                role = role.strip()
                if role in ("system", "human", "assistant"):
                    messages.append((role, msg.strip()))
                    continue

            # Fallback to classic prompt body
            body.append(line)

        return PromptDef(
            name=name,
            prompt_text="\n".join(body).strip(),
            messages=messages if is_chat else None,
            input_vars=input_vars,
            model=model,
            triggers=triggers,
            rules=rules,
            is_chat=is_chat
        )

    def __getattr__(self, key):
        return self.prompts[key]
