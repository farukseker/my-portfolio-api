from typing import Literal
from os import getenv
import logging
import json
import threading

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

# Modül seviyesinde LLM instance cache'i - pickle sorunu olmadan
_llm_cache = {}
_cache_lock = threading.Lock()


def get_llm(model: str = "x-ai/grok-4.1-fast"):
    if model not in _llm_cache:
        with _cache_lock:
            # Double-check locking pattern
            if model not in _llm_cache:
                from langchain_openai import ChatOpenAI
                _llm_cache[model] = ChatOpenAI(
                    api_key=getenv("OPENROUTER_API_KEY"),
                    base_url="https://openrouter.ai/api/v1",
                    model=model,
                    temperature=.2,
                    max_retries=0,
                    default_headers={
                        "HTTP-Referer": 'farukseker.com.tr',
                        "X-Title": 'farukseker',
                    }
                )
    
    return _llm_cache[model]


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
        # llm = get_llm()
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
        """
        Stream LLM events safely.
        Any HTTP / network error from upstream LLM is caught and logged,
        so the Gunicorn worker does not crash.
        """
        events = None
        followup = None
        try:
            try:
                events = chat.stream(
                    {"message": user_message},
                    config={"configurable": {"session_id": chat_room.session_id}},
                )
            except Exception as e:
                logger.exception("Error while starting LLM stream", exc_info=e)
                yield "[ERROR] LLM stream could not be started. Please try again later."
                return

            for event in events:
                try:
                    if (
                        hasattr(event, "content")
                        and event.content
                        and len(event.content) > 0
                        and isinstance(event, (AIMessage, AIMessageChunk))
                        and event.content
                    ):
                        yield event.content

                    if hasattr(event, "tool_calls") and event.tool_calls:
                        tool_messages: list[ToolMessage] = []
                        for call in event.tool_calls:
                            tool = tools_map[call["name"]]
                            result = tool.invoke(call["args"])

                            ChatLog.objects.create(
                                room=chat_room,
                                type="tool",
                                message=result,
                                extra_json=json.dumps(
                                    {
                                        "name": call["name"],
                                        "tool_call_id": call["id"],
                                    }
                                ),
                            )
                            tool_messages.append(
                                ToolMessage(
                                    content=result,
                                    tool_call_id=call["id"],
                                    name=call["name"],
                                )
                            )

                        try:
                            followup = chat.stream(
                                {"message": tool_messages},
                                config={
                                    "configurable": {
                                        "session_id": chat_room.session_id
                                    }
                                },
                            )
                            for ev in followup:
                                if isinstance(ev, (AIMessage, AIMessageChunk)) and ev.content:
                                    yield ev.content
                        except Exception as e:
                            logger.exception("Error while streaming followup LLM response", exc_info=e)
                            break
                except Exception as e:
                    logger.exception("Error while processing LLM stream event", exc_info=e)
                    break
        finally:
            # Close streams if possible
            try:
                if followup and hasattr(followup, "close"):
                    followup.close()
            except Exception:
                pass
            try:
                if events and hasattr(events, "close"):
                    events.close()
            except Exception:
                pass

            # Drop references
            try:
                del chat
            except Exception:
                pass
            if events:
                try:
                    del events
                except Exception:
                    pass
            if followup:
                try:
                    del followup
                except Exception:
                    pass

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
