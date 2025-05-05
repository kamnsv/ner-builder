import logging
from typing import Annotated

from fastapi import APIRouter, Query, Body, HTTPException

from ..router import Router
from models import EntityModel
from kg import KnowledgeGraph

class EntityApi(Router, KnowledgeGraph):
    def set_routes(self, api: APIRouter):
        @api.post('/entities', summary="Добавление сущностей", description='''''')
        async def add_node(entities: list[EntityModel]):
            logging.info('add_node %s', entities)
            [await self._add_node(entity) for entity in entities]
         
        @api.delete("/entity/{name}", summary="Удалить сущность")
        async def remove_node(name: str):
            logging.info('remove_node %s', name)
            if not await self._remove_node(name):
                raise HTTPException(404, f"Сущность {name.title()} не найдена")

        @api.put("/entity", summary="Изменить сущность")
        async def update_node(name: Annotated[str, Query(description="Имя сущности")], 
                              new_type: Annotated[str, Query(description="Новый тип")]
                              ):
            logging.info('change_node %s', name)
            if not await self._change_node(name, new_type):
                raise HTTPException(404, f"Сущность {name.title()} не найдена")
            
        @api.post("/entities/merge", summary="Объединить сущности")
        async def merge_nodes(
            entity_name: str = Query(..., description="Сущность"),
            duplicate_name: str = Query(..., description="Дубликат сущности"),
            result_entity: EntityModel = Body(..., description="Объединенная сущность")
        ):
            logging.info('merge_nodes %s ^ %s = %s', entity_name, duplicate_name, result_entity)
            await self._merge_nodes(entity_name, duplicate_name, result_entity)

        @api.get("/entity/{name}", summary="Найти сущность")
        async def get_node(name: str) -> EntityModel:
            node = await self._get_node(name)
            if not node:
                raise HTTPException(404, f"Сущность {name.title()} не найдена")
            return node
        
        @api.get("/entities/{type}", summary="Найти сущности одного типа")
        async def get_node(type: str) -> list[EntityModel]:
            nodes = await self._get_nodes_by_type(type)
            if not len(nodes):
                raise HTTPException(404, f"Сущностей типа {EntityModel(type=type).type} не найдены")
            return nodes
        