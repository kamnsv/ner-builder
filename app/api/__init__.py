from fastapi import FastAPI

from .router import Router
from cfg import api as url_api

from .llm import LLMApi
from .kg import KnowledgeGraphApi

class Routers:

    def __init__(self, app: FastAPI):
        self.app = app
        for name, api in self.sections.items():
            app.include_router(api(),
                               prefix=f'{url_api}/{name}',
                               tags=[str(api)])          
       
            
    @property        
    def sections(self) -> dict[str, Router]:
        kg = KnowledgeGraphApi()
        
        @self.app.on_event("shutdown")
        async def shutdown_event():
            await kg.close()
    
        return {
            'kg':  kg,
            'llm': LLMApi(),
        } 
   