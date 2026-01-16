from openai import OpenAI
from os import getenv


def get_embedder(text: list[str] | str) -> list:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=getenv("OPENROUTER_API_KEY"),
    )

    res = client.embeddings.create(
        model="google/gemini-embedding-001",
        input=text,
        encoding_format="float",
        extra_headers={
            "HTTP-Referer": "farukseker.com.tr",
            "X-Title": "farukseker",
        },
    )

    if type(text) == str:
        return res.data[0].embedding
    return [d.embedding for d in res.data]