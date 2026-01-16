def build_faiss_content_context(results: list) -> str:
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