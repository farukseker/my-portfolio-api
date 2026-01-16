from django.conf import settings


class LLMFactory:
    def __init__(
        self,
        model: str = "x-ai/grok-4.1-fast",
        temperature: float = 0.2,
        max_retries: int = 0,
    ):
        self.model = model
        self.temperature = temperature
        self.max_retries = max_retries

    def get_llm(self):
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            model=self.model,
            temperature=self.temperature,
            max_retries=self.max_retries,
            default_headers={
                "HTTP-Referer": 'https://farukseker.com.tr', # settings.SITE_URL,
                "X-Title": 'FarukSeker-WEB' # settings.SITE_NAME,
            },
        )
