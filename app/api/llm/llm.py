import logging
from typing import Annotated
import json
from fastapi import APIRouter, Body, Query

import cfg
from ..router import Router
from models import AnswerModel, RelationshipModel
from llm import LargeLanguageModel


class LargeLanguageModelApi(Router, LargeLanguageModel):
    def set_routes(self, api: APIRouter):
        @api.post('/instructions', summary="Ввод инструкций для языковой модели", 
                 description='''''')
        async def send_prompt(
            system_prompt: Annotated[str, Body(..., description="Системная инструкция для LLM")],
            user_query:    Annotated[str, Body(..., description="Пользовательский запрос")],
            return_type:   Annotated[str, Query(description="Формат ответа", enum=['text', 'json'])] = 'json'
        ) -> str | dict | list:
            logging.debug(f"POST instructions {return_type=}")
            answer = AnswerModel(text=await self.generate_answer(system_prompt, user_query))
            return getattr(answer, return_type)
        
        @api.post('/knowledge_graph', summary="Построение графа знаний по тексту", 
                 description='''''')
        async def build_knowledge_graph(
            text: Annotated[str, Body(..., media_type="text/plain", description="Текст для анализа")],
            lang: Annotated[str, Query(description="Язык текста", enum=['en', 'ru'])] = 'en'
        ) -> list[RelationshipModel]:
            logging.debug(f"POST knowledge_graph {lang=}")
            sys_prompt = self.get_sys_prompt(lang)
            response = await self.generate_answer(sys_prompt, text)
            logging.debug(response)
            answer = AnswerModel(text=response)
            return [RelationshipModel(**i) for i in answer.json["relationships"]]
    
    def get_sys_prompt(self, lang: str) -> str:
        with open(f'/app/cfg/sys_prompts/{lang}_prompt.txt', 'r') as f:
            return f.read()
    
