import json
from abc import ABC

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage

from chatwithme.models import ChatRoom, ChatLog


class DjangoChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id):
        self.session_id = session_id
        self.room, _ = ChatRoom.objects.get_or_create(
            session_id=session_id,
        )

    @property
    def messages(self):
        logs = (
            ChatLog.objects
            .filter(room=self.room)
            .order_by("timestamp")
        )

        result = []
        for log in logs:
            if log.type == "human":
                result.append(HumanMessage(content=log.message))
            elif log.type == "ai":
                if log.extra_json and (meta := json.loads(log.extra_json)):
                    result.append(
                        AIMessage(
                            content=log.message,
                            tool_calls=meta.get("tool_calls")
                        )
                    )

                result.append(
                    AIMessage(
                        content=log.message,
                    )
                )

            elif log.type == "tool":
                meta = json.loads(log.extra_json or "{}")

                result.append(
                    ToolMessage(
                        content=log.message,  # tool output (str)
                        name=meta.get("name"),
                        tool_call_id=meta.get("tool_call_id")
                    )
                )
                # result.append(ToolMessage(content=log.message, **log.extra_json))
            else:
                result.append(SystemMessage(content=log.message))
        return result

    def add_message(self, message):
        # Store tool_calls if AIMessage has them
        if isinstance(message, AIMessage) and message.tool_calls:
            extra = json.dumps({
                "tool_calls": message.tool_calls
            })
            ChatLog.objects.create(
                room=self.room,
                message=message.content,
                type=message.type,
                extra_json=extra
            )

        ChatLog.objects.create(
            room=self.room,
            message=message.content,
            type=message.type
        )

    def clear(self):
        # ChatLog.objects.all().delete()
        ...