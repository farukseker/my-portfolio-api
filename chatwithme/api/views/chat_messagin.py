from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from chatwithme.api.serializers import HumanMessageSerializer
from chatwithme.models import ChatRoom
from config.settings.base import GEMINI_AI_API_KEY

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory

from chatwithme.chat_history import DjangoChatMessageHistory


def get_llm():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        google_api_key=GEMINI_AI_API_KEY
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

        return Response({"r": r.content})
