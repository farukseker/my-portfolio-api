from chatwithme.llm_tools.utils import (
    BuildsEmbed,
    build_content_index_embed,
)
from typing import List
import numpy as np
import logging

logger = logging.getLogger(__name__)


def faiss_content_search(
    query: str,
    top_k: int = 5,
    score_top_limit: float = 1.5,
) -> List[dict]:
    from chatwithme.llm_tools.utils import get_embedder
    try:
        # Cached / singleton FAISS index
        builds_embed: BuildsEmbed = build_content_index_embed()

        # Query embedding (already float32 list after your fix)
        emb = get_embedder(query)

        # FAISS expects shape: (1, d) and dtype float32
        q_emb = np.asarray(emb, dtype="float32").reshape(1, -1)

        distances, idx = builds_embed.index.search(q_emb, top_k)

        results: List[dict] = []
        for i, score in zip(idx[0], distances[0]):
            if i < 0:
                continue
            if score <= score_top_limit:
                # Copy to avoid mutating cached docs
                doc = builds_embed.docs[i].copy()
                doc["score"] = float(score)
                results.append(doc)

        return results

    except Exception as e:
        logger.exception("faiss_content_search failed: {0}".format(e))
        return []
