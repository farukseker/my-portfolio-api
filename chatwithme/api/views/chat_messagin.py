import json
from os import getenv
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from chatwithme.api.serializers import HumanMessageSerializer
from chatwithme.models import ChatRoom, ChatLog
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory

from chatwithme.chat_history import DjangoChatMessageHistory
from projects.models import ContentModel

from chatwithme.llm_tools import search_knowledge_base
from chatwithme.llm_tools import get_blog_meta_data
import logging


tools_map = {
    "search_knowledge_base": search_knowledge_base,
    "get_blog_meta_data": get_blog_meta_data,
}

logger = logging.getLogger(__name__)


def get_llm():
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        api_key=getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        model="x-ai/grok-4.1-fast",
        # model="mistralai/ministral-14b-2512", #very good
        # model="google/gemini-3-pro-preview",
        default_headers={
            "HTTP-Referer": 'farukseker.com.tr',
            # getenv("YOUR_SITE_URL"),  # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": 'farukseker',  # getenv("YOUR_SITE_NAME"),  # Optional. Site title for rankings on openrouter.ai.
        }
    )

    return llm


class ChatMessagingView(APIView):
    serializer_class = HumanMessageSerializer
    """
    create a new chat messaging message
    with ai
    """


    @staticmethod
    def get_session_history(session_id: str):
        return DjangoChatMessageHistory(session_id)

    def post(self, request, *args, **kwargs):
        user_message = self.serializer_class(data=request.data)
        if not user_message.is_valid():
            raise ValidationError(user_message.errors)

        chat_id = kwargs.get('chat_id', None)
        chat_room = ChatRoom.objects.filter(session_id=chat_id).first()


        from chatwithme.prompt_manger import load_row_rules
        rules = load_row_rules()
        rules = [SystemMessage(rule) for rule in rules]

        prompt = ChatPromptTemplate.from_messages(
            rules
            +[
                ("placeholder", "{history}"),
                ("human", "{message}")
            ]
        )
        llm = get_llm()
        llm = llm.bind_tools([
            search_knowledge_base,
            get_blog_meta_data
        ])

        chain = prompt | llm

        chat = RunnableWithMessageHistory(
            chain,
            self.get_session_history,
            input_messages_key="message",
            history_messages_key="history",
        )

        r = chat.invoke(
            {"message": user_message.data.get("message")},
            config={"configurable": {"session_id": chat_room.session_id}}
        )


        print(r)
        print(r.tool_calls)
        # ChatLog.objects.create(type="ai", message=r.content,room=chat_room,)

        if r.tool_calls:
            for call in r.tool_calls:
                logger.info(f"call: {call}")
                _tool = tools_map[call["name"]]
                # tool_result = _tool(tool_input=call["args"])
                tool_result = _tool.invoke(call["args"])
                logger.info(f"call re: {tool_result}")

                ChatLog.objects.create(
                    room=chat_room,
                    message=tool_result,
                    extra_json=json.dumps({
                        "name": call["name"],
                        "tool_call_id": call["id"],
                    }),
                    type='tool'
                )

            r = chat.invoke(
                {"message": user_message.data.get("message")},
                config={"configurable": {"session_id": chat_room.session_id}}
            )
            print('tool')
            print(r)
            print(r.tool_calls)
            return Response({"r": r.content})
        return Response({"r": r.content})

