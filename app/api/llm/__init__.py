from .llm import LargeLanguageModelApi
from llm import TabbyLLM


class TabbyApi(LargeLanguageModelApi, TabbyLLM):
    def __str__(self):
        return 'LargeLanguageModelApi'
    