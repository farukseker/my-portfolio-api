from projects.models import ContentModel
from dataclasses import dataclass
from typing import List, Any
import numpy as np
import faiss


@dataclass
class BuildsEmbed:
    docs: List[dict[str, Any]]
    index: faiss.IndexFlatL2


def build_content_index_embed() -> BuildsEmbed:
    docs = ContentModel.objects.all()
    emb = np.stack([np.array(d.embedding, dtype=float) for d in docs])
    docs = [
        {
            "title": x.title,
            "type": x.content_type,
            "url": x.slug,
            "content": x.text
        }
        for x in docs
    ]
    d = emb.shape[1]
    index = faiss.IndexFlatL2(d)  # L2 distance, CPU
    index.add(emb)
    return BuildsEmbed(docs, index)
