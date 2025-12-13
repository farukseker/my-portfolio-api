from abc import ABC

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

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
                result.append(AIMessage(content=log.message))
            else:
                result.append(SystemMessage(content=log.message))
        return result

    def add_message(self, message):
        ChatLog.objects.create(
            room=self.room,
            message=message.content,
            type=message.type
        )

    def clear(self):
        # ChatLog.objects.all().delete()
        ...