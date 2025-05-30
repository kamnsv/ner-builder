import threading
import os
import logging

import urllib.request
from llama_cpp import Llama
from tqdm import tqdm

from .llm import LargeLanguageModel
from cfg import model_url, model_path, model_context, seed



class LocalLLM(LargeLanguageModel):
    _instance = None
    _lock = threading.Lock()

    
    def download_with_progress(self, url, filename):
        response = urllib.request.urlopen(url)
        total_size = int(response.getheader('Content-Length').strip())
        block_size = 1024

        with open(filename, 'wb') as f, tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                f.write(buffer)
                pbar.update(len(buffer))
            
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not os.path.exists(model_path):
            logging.info(f"Скачивание модели из {model_url} в {model_path}")
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            self.download_with_progress(model_url, model_path)
        else:
            logging.info(f"Модель уже скачана в {model_path}")

        cpu_total = os.cpu_count()
        cpu_affinity = len(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else cpu_total

        logging.info(f"Всего логических CPU: {cpu_total=}" )
        logging.info(f"Доступно процессу CPU: {cpu_affinity=}")

        self.llm = Llama(
            model_path=model_path,
            n_ctx=model_context,           
            n_threads=max(1, cpu_affinity - 1),      
            verbose=True,
            temperature=0,
            use_mlock=True,
            low_vram=True,
            seed=seed,     
            top_p=1.0,   
            top_k=1      
        )

    async def generate_answer(self, system_prompt: str, user_query: str) -> str:
        logging.debug(f"{system_prompt=}")
        logging.debug(f"{user_query=}")

        # Для потокобезопасности используем lock
        with self._lock:
            response = self.llm.create_chat_completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ]
            )
        return response['choices'][0]['message']['content']
