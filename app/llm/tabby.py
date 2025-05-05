import json
import logging

import aiohttp

from .llm import LargeLanguageModel
from cfg import tabby_url, tabby_key


class TabbyLLM(LargeLanguageModel):
    
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {tabby_key}',
        'Content-Type': 'application/json'
    }
    url = tabby_url + '/v1/chat/completions'
    async def generate_answer(self, system_prompt: str, user_query: str) -> str:
        logging.debug(f"{system_prompt=}")
        logging.debug(f"{user_query=}")
        data = {
            "model": "SaigaGemma2-9B",
            "temperature": 0,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url,
                headers=self.headers,
                json=data
            ) as response:
                assert response.status == 200, f'Ошибка №{response.status} запроса к tabby {tabby_url}'
                return self.build_answer(await response.text())
            
    def build_answer(self, text:str) -> str:
        answer = ''
        for chunk in text.strip().split('\n\n'):
            data = json.loads(chunk[6:])
            content = data.get('choices', [{}])[0].get('delta', {}).get('content', '')
            if content is not None:
                answer += content
        logging.debug(f"{answer=}")
        return answer
    