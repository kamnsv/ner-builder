from fastapi import FastAPI

from .router import Router
from cfg import api as url_api

from .ner import NamedEntityRecognitionApi
from .llm import TabbyLLMAPI


class Routers:

    def __init__(self, app: FastAPI):
        for name, api in self.sections.items():
            app.include_router(api(),
                               prefix=f'{url_api}/{name}',
                               tags=[str(api)])          
       
            
    @property        
    def sections(self) -> dict[str, Router]:
        return {
            #'kg':  KnowledgeGraphApi(),
            'llm': TabbyLLMAPI(),
            'ner': NamedEntityRecognitionApi(),
        } 
   