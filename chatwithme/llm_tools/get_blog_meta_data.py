import logging
from typing import List

from langchain_core.tools import tool
from contents.models import ContentModel

logger = logging.getLogger(__name__)


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
        docs = ContentModel.objects.filter(
            show=True,
            content_type__name__in=["project", "blog"],
        )
        context:str = '\n'.join([f"title: {doc.title}\n slug: {doc.slug}" for doc in docs])
        return context
    except:
        logger.error('No blog posts found.')
        return 'No blog posts found.'