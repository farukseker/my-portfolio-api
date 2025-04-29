import os.path
from config.settings.base import PROMPT_TEMPLATES_BASE_DIR
from dataclasses import dataclass
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_ollama.llms import OllamaLLM
from langchain_core.runnables.base import RunnableSequence
from pydantic import BaseModel
import models


@dataclass()
class Prompt:
    name: str
    prompt: str
    model: object | None = None
    triggers: list[str] | None = None
    input_variables: list[str] | None = None
    __llm_ref: OllamaLLM | None = None

    def __str__(self):
        return self.prompt

    @property
    def template(self) -> PromptTemplate:
        template = PromptTemplate(template=self.prompt, input_variables=self.input_variables)
        template.input_variables = self.input_variables
        return template

    def set_llm(self, llm: OllamaLLM):
        self.__llm_ref = llm

    @property
    def parser(self) -> PydanticOutputParser | None:
        if self.model and issubclass(self.model, BaseModel):
            return PydanticOutputParser(pydantic_object=self.model)
        return None

    @property
    def chain(self) -> RunnableSequence | None:
        try:
            if not self.parser:
                return self.template | self.__llm_ref
            return self.template | self.__llm_ref | self.parser
        except:
            return None


class PromptManager:
    def __init__(self, llm_ref: OllamaLLM):
        self.llm = llm_ref
        self.__prompts: dict[Prompt] = {}
        self.load_all_prompts()

    def do_prompt_context(self, name: str, context: str) -> None:
        model: object | None = None
        input_variables: list[str] | None = None
        triggers: list[str] | None = None
        prompt: str = ''
        for context_var in context.split('\n'):
            if len(var := context_var.split(':')) == 2 and context_var.startswith('!'):
                if var[0] == '!input_variables':
                    input_variables = var[1].strip().split(',')
                if var[0] == '!triggers':
                    triggers = var[1].strip().split(',')
                elif var[0] == '!model':
                    model: str = var[1]
                    if hasattr(models, model):
                        model = getattr(models, model)
            else:
                prompt += context_var

        __prompt = Prompt(name=name, prompt=prompt, input_variables=input_variables, model=model, triggers=triggers)
        __prompt.set_llm(self.llm)
        self.__prompts.update({__prompt.name: __prompt})

    def load_all_prompts(self):
        try:
            if os.path.isdir(PROMPT_TEMPLATES_BASE_DIR):
                for root, dirs, files in os.walk(PROMPT_TEMPLATES_BASE_DIR, topdown=False):
                    for name in files:
                        with open(os.path.join(root, name), 'r', encoding='utf-8') as pf:
                            self.do_prompt_context(
                                name=name,
                                context=pf.read()
                            )
                    # for name in dirs:
        except Exception as exception:
            print(exception)

    def items(self):
        return self.__prompts.items()

    def __getattr__(self, item) -> Prompt:
        return self.__prompts.get(item)


__all__ = ['PromptManager']


if __name__ == '__main__':
    # prompts = PromptManager(OllamaLLM(model='gemma3:4b'))
    # chain = prompts.create_reminder.chain
    # r = chain.invoke({"task_text": "I will buy chocolate from the market today, but I must not forget to buy a bag."})
    # # task='Buy chocolate from the market' notes='Remember to buy a bag of chocolate.' death_line='today'
    # # task='Buy chocolate from the market' notes='Remember to buy a bag.' death_line='today'
    # print(r)

    # without model
    prompts = PromptManager(OllamaLLM(model='gemma3:4b'))
    chain = prompts.summarize_tr.chain

    long_ai_message = """
    Hi there! Based on your request, I've created a complete to-do list including
    initial setup, code cleanup, sending the final email, and updating the tracker.  
    All documents are organized. Let me know if you need changes.
    """

    result = chain.invoke({"chat_message": long_ai_message})
    print(result)
