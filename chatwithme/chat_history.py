import json

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    ToolMessage,
)

from chatwithme.models import ChatRoom, ChatLog

MAX_HISTORY_MESSAGES = 50


class DjangoChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.room, _ = ChatRoom.objects.get_or_create(session_id=session_id)
        self._messages_cache = None

    @property
    def messages(self):
        if self._messages_cache is not None:
            return self._messages_cache
        
        logs = ChatLog.objects.filter(room=self.room).order_by("-timestamp")[:MAX_HISTORY_MESSAGES]
        logs = list(reversed(logs)) 
        result = []

        for log in logs:
            if log.type == "human":
                result.append(HumanMessage(content=log.message))

            elif log.type == "ai":
                meta = json.loads(log.extra_json or "{}")

                result.append(
                    AIMessage(
                        content=log.message,
                        tool_calls=meta.get("tool_calls") if meta.get("tool_calls") else [],
                    )
                )

            elif log.type == "tool":
                meta = json.loads(log.extra_json or "{}")
                tool_call_id = meta.get("tool_call_id")

                if tool_call_id:  # critical guard for tool calls
                    result.append(
                        ToolMessage(
                            content=log.message,
                            name=meta.get("name"),
                            tool_call_id=tool_call_id,
                        )
                    )
            else:  # system
                result.append(SystemMessage(content=log.message))

        self._messages_cache = result
        return result

    def add_message(self, message):
        self._messages_cache = None
        
        if isinstance(message, HumanMessage):
            msg_type = "human"
            extra = None

        elif isinstance(message, AIMessage):
            msg_type = "ai"
            extra = (
                json.dumps({"tool_calls": message.tool_calls})
                if message.tool_calls
                else None
            )

        elif isinstance(message, ToolMessage):
            msg_type = "tool"
            extra = json.dumps({
                "name": message.name,
                "tool_call_id": message.tool_call_id,
            })

        else:  # SystemMessage
            msg_type = "system"
            extra = None

        ChatLog.objects.create(
            room=self.room,
            type=msg_type,
            message=message.content,
            extra_json=extra,
        )

    def clear(self):
        self._messages_cache = None
        ChatLog.objects.filter(room=self.room).delete()
