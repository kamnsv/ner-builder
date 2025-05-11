import logging

from .llm import LargeLanguageModelApi
from llm import TabbyLLM, LocalLLM
from  cfg import tabby_key


if tabby_key:
    logging.info("LLM used Tabby")
    class LLMApi(LargeLanguageModelApi, TabbyLLM):
        def __str__(self):
            return 'LargeLanguageModelApi'
else:
    logging.info("LLM used local CPU")
    class LLMApi(LargeLanguageModelApi, LocalLLM):
        def __str__(self):
            return 'LargeLanguageModelApi'
        