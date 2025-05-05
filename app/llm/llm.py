    
from abc import ABC, abstractmethod


class LargeLanguageModel(ABC):
    @abstractmethod
    async def generate_answer(self, system_prompt: str, user_query: str) -> str:
        pass         
    