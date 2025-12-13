from chatwithme.llm_tools.utils import build_faiss_content_context, faiss_content_search
from langchain_core.tools import tool

import logging

logger = logging.getLogger(__name__)


@tool
def search_knowledge_base(query: str) -> str:
    """
    Search internal blog and project knowledge base.
    Use this tool when the user asks about projects, blogs,
    technical details, or past content.
    """
    logger.info(f'query(search_knowledge_base): {query}')
    try:
        results = faiss_content_search(query, top_k=5)
        logger.info(f'query(search_knowledge_base) does not match results: {results}')
        if not results:
            return "No relevant internal knowledge found."

        logger.info(f'query(search_knowledge_base) start building content context')
        context = build_faiss_content_context(results)
        logger.info(f'query(search_knowledge_base) end building content context')
        return context
    except Exception as e:
        print(f'query(search_knowledge_base): {e}')
        logger.error(f"No relevant internal knowledge found.: {query}")
        logger.error(f'query(search_knowledge_base): {e}')
        return "ERR No relevant internal knowledge found."
