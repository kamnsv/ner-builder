import logging
from typing import Annotated
from abc import ABC, abstractmethod

from fastapi import APIRouter, Body, Query

from ..router import Router
from models import AnswerModel    


class LargeLanguageModelApi(Router, ABC):
    def set_routes(self, api: APIRouter):
        @api.post('/Instructions', summary="Ввод инструкций для языковой модели", 
                 description='''''')
        async def send_prompt(
            system_prompt: Annotated[str, Body(..., description="Системная инструкция для LLM")],
            user_query: Annotated[str, Body(..., description="Пользовательский запрос")],
            return_type: Annotated[str, Query(description="Формат ответа", enum=['text', 'json'])] = 'json'
        ) -> str:
            answer = AnswerModel(text = await self.generate_answer(system_prompt, user_query))
            if 'json' == return_type:
                return answer.json
            return answer.text
        
    @abstractmethod
    async def generate_answer(self, system_prompt: str, user_query: str) -> str:
        pass         
    
    def __str__(self):
        return 'LargeLanguageModelApi'