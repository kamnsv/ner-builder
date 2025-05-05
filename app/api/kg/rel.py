import logging
from typing import Annotated
from abc import ABC, abstractmethod

from fastapi import APIRouter, Query

from ..router import Router
from models import RelationshipModel
from kg import KnowledgeGraph

class RelationshipApi(Router, KnowledgeGraph):
    def set_routes(self, api: APIRouter):

        @api.post("/relationships", summary="Добавить связи между сущностями")
        async def add_relationship(rels: list[RelationshipModel]):
            for rel in rels:
                logging.info('add_relationship %s - %s -> %s', rel.subject, rel.action, rel.object)
                await self._add_relationship(rel)

        @api.delete("/relationship", summary="Удалить связь")
        async def remove_relationship(rel: RelationshipModel):
            logging.info('remove_relationship %s - %s -> %s', rel.subject, rel.action, rel.object)
            await self._remove_relationship(rel)

        @api.get("/relationships/{name}", summary="Получить связи сущности")
        async def get_relationships(name: str) -> list[RelationshipModel]:
            logging.info(f'get_relationships {name}')
            return await self._get_relationships(name)
        