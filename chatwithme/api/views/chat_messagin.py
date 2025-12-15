from typing import Literal
from os import getenv
import logging
import json

from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from django.http import StreamingHttpResponse

from chatwithme.api.serializers import HumanMessageSerializer
from chatwithme.models import ChatRoom, ChatLog

from langchain_core.messages import AIMessage, AIMessageChunk, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory

from chatwithme.chat_history import DjangoChatMessageHistory
from chatwithme.llm_tools import search_knowledge_base
from chatwithme.llm_tools import get_blog_meta_data



tools_map = {
    "search_knowledge_base": search_knowledge_base,
    "get_blog_meta_data": get_blog_meta_data,
}

logger = logging.getLogger(__name__)


def get_llm(model: str = "x-ai/grok-4.1-fast") -> Literal['ChatOpenAI']:
    from langchain_openai import ChatOpenAI
    llm: ChatOpenAI = ChatOpenAI(
        api_key=getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        model=model,
        # model="mistralai/ministral-14b-2512", # sum da kulan stream sorunlu
        temperature=.2,
        max_retries=0,
        default_headers={
            "HTTP-Referer": 'farukseker.com.tr',
            "X-Title": 'farukseker',
        }
    )
    return llm


class ChatMessagingView(APIView):
    serializer_class = HumanMessageSerializer

    @staticmethod
    def get_session_history(session_id: str):
        return DjangoChatMessageHistory(session_id)

    def build_chat(self, chat_room):
        from chatwithme.prompt_manger import load_row_rules

        rules = [("system", r) for r in load_row_rules()]

        prompt = ChatPromptTemplate.from_messages(
            rules
            + [
                ("placeholder", "{history}"),
                ("human", "{message}"),
            ]
        )
        llm = get_llm()
        llm = llm.bind_tools([
            search_knowledge_base,
            get_blog_meta_data,
        ])

        chain = prompt | llm

        return RunnableWithMessageHistory(
            chain,
            self.get_session_history,
            input_messages_key="message",
            history_messages_key="history",
        )

    @staticmethod
    def stream_generator(chat, user_message, chat_room):
        events = chat.stream(
            {"message": user_message},
            config={"configurable": {"session_id": chat_room.session_id}},
        )

        for event in events:
            if hasattr(event, "content") and event.content and len(event.content) > 0 and isinstance(event, (AIMessage, AIMessageChunk)) and event.content:
                yield event.content

            if event.tool_calls:
                tool_messages: list[ToolMessage] = []
                for call in event.tool_calls:
                    tool = tools_map[call["name"]]
                    result = tool.invoke(call["args"])

                    ChatLog.objects.create(
                        room=chat_room,
                        type="tool",
                        message=result,
                        extra_json=json.dumps({
                            "name": call["name"],
                            "tool_call_id": call["id"],
                        }),
                    )
                    tool_messages.append(
                        ToolMessage(
                            content=result,
                            tool_call_id=call["id"],
                            name=call["name"],
                        )
                    )

                followup = chat.stream(
                    {"message": tool_messages},
                    config={"configurable": {"session_id": chat_room.session_id}},
                )
                for ev in followup:
                    if isinstance(ev, (AIMessage, AIMessageChunk)) and ev.content:
                        yield ev.content


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        chat_id = kwargs.get("chat_id")
        chat_room = ChatRoom.objects.filter(session_id=chat_id).first()

        if not chat_room:
            raise ValidationError("Chat room not found")

        user_message = serializer.validated_data["message"]

        chat = self.build_chat(chat_room)

        response = StreamingHttpResponse(
            self.stream_generator(chat, user_message, chat_room),
            content_type="text/plain; charset=utf-8",
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response
