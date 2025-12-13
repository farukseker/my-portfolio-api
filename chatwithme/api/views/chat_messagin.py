import json
from os import getenv
from typing import List, Literal, Any

from langchain_openai import ChatOpenAI
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from chatwithme.api.serializers import HumanMessageSerializer
from chatwithme.models import ChatRoom, ChatLog
from config.settings.base import GEMINI_AI_API_KEY

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.tools import tool

from chatwithme.chat_history import DjangoChatMessageHistory
from projects.models import ContentModel

import numpy as np
import faiss

import logging

logger = logging.getLogger(__name__)

def get_llm():
    # llm = ChatGoogleGenerativeAI(
    #     model="gemini-2.5-flash",
    #     temperature=0.2,
    #     google_api_key=GEMINI_AI_API_KEY
    # )
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

def build_index_embed() -> Literal["docs", "index", "emb"]:
    docs = ContentModel.objects.all()
    emb = np.stack([np.array(d.embedding, dtype=float) for d in docs])
    docs = [(x.id, x.text ) for x in docs]
    d = emb.shape[1]
    index = faiss.IndexFlatL2(d)  # L2 distance, CPU
    index.add(emb)
    return docs, index, emb


def faiss_search(query: str, top_k: int = 5) -> List[dict]:
    docs, index, embed_model = build_index_embed()
    q_emb = embed_model.encode([query], convert_to_numpy=True)
    distances, idx = index.search(q_emb, top_k)

    results = []
    for i, score in zip(idx[0], distances[0]):
        doc = docs[i]
        doc["score"] = float(score)
        results.append(doc)

    return results


def build_faiss_context(results: list) -> str:
    blocks = []
    for r in results:
        blocks.append(
            f"""
Title: {r.get('title')}
Type: {r.get('content_type')}
URL: {r.get('slug')}
Content:
{r.get('content')}
"""
        )
    return "\n---\n".join(blocks)

@tool
def search_knowledge_base(query: str) -> str:
    """
    Search internal blog and project knowledge base.
    Use this tool when the user asks about projects, blogs,
    technical details, or past content.
    """
    logger.info(f'query(search_knowledge_base): {query}')
    try:
        results = faiss_search(query, top_k=5)
        if not results:
            return "No relevant internal knowledge found."

        context = build_faiss_context(results)
        return context

    except:
        logger.error(f"No relevant internal knowledge found.: {query}")
        return "No relevant internal knowledge found."


@tool
def get_blog_meta_data(query: str) -> str:
    """
    Use this tool when the user asks to:
    - list blogs
    - show all blog posts
    - show blog titles
    - list blog content
    Return all blog titles and URLs.
    """
    try:
        logger.info('getting blog meta data')
        docs = ContentModel.objects.all()
        context = '\n'.join([f"title: {doc.title}\n slug: {doc.slug}" for doc in docs])
        return context
    except:
        logger.error('No blog posts found.')
        return 'No blog posts found.'

tools_map = {
    "search_knowledge_base": search_knowledge_base,
    "get_blog_meta_data": get_blog_meta_data,
}


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
                _tool = tools_map[call["name"]]
                tool_result = _tool(tool_input=call["args"])

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

        print(r)
        print(r.tool_calls)
        return Response({"r": r.content})

