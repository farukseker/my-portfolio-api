from chatwithme.llm_tools.utils import BuildsEmbed, build_content_index_embed, get_embedder
from typing import List
import numpy as np
import logging

logger = logging.getLogger(__name__)


def faiss_content_search(
    query: str,
    top_k: int = 5,
    score_top_limit: float = 1.5,
) -> List[dict]:
    try:
        builds_embed: BuildsEmbed = build_content_index_embed()

        emb = get_embedder(query)
        q_emb = np.asarray([emb], dtype="float32")

        distances, idx = builds_embed.index.search(q_emb, top_k)

        qr = []
        for i, score in zip(idx[0], distances[0]):
            if score <= score_top_limit:
                doc = builds_embed.docs[i]
                doc.update({"score": float(score)})
                qr.append(doc)

        return qr
    except Exception as e:
        logger.error(e)
        return []
