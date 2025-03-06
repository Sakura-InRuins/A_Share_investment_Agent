import os

from dotenv import load_dotenv

from core.llm.client.base import BaseClient
from core.llm.client.openai import OpenAIClient
from core.llm.client.zhipuai import ZhipuAIClient
from core.llm.client.localai import LocalAIClient


class Factory:
    @staticmethod
    def getClient(provider: str = None) -> BaseClient:
        load_dotenv()
        provider = provider or os.getenv("LLM_PROVIDER", "openai")
        chat_model_providers = {
            'zhipuai': lambda: ZhipuAIClient(),
            'openai': lambda: OpenAIClient(),
            'localai': lambda: LocalAIClient(),
        }

        provider_func = chat_model_providers.get(provider)
        if provider_func:
            return provider_func()
        else:
            raise Exception(f'Unknown chat model provider: {provider}')
