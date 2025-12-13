from sentence_transformers import SentenceTransformer
from chatwithme.llm_tools.utils import BuildsEmbed, build_content_index_embed
from typing import List
import logging

logger = logging.getLogger(__name__)

def faiss_content_search(query: str, top_k: int = 5, score_top_limit: float = 1.5, device: str = "cpu") -> List[dict]:
    try:
        embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device=device)
        builds_embed: BuildsEmbed = build_content_index_embed()

        q_emb = embed_model.encode([query], convert_to_numpy=True)
        distances, idx = builds_embed.index.search(q_emb, top_k)
        print(len(idx))
        # [
        #     logger.info(f'title: {builds_embed.docs[i].get('title')} | score: {float(score)}')
        #     for i, score in zip(idx[0], distances[0])
        # ]
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