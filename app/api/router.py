from abc import ABC, abstractmethod

from fastapi import APIRouter


class Router(ABC):
    def __call__(self) -> APIRouter:
        api = APIRouter()
        self.set_routes(api)
        return api
    
    @abstractmethod
    def set_routes(self, api: APIRouter):
        ...

    def __str__(self):
        return self.__class__.__name__
    