import logging
from abc import ABC, abstractmethod

from models import EntityModel, RelationshipModel


class KnowledgeGraph(ABC):
    @abstractmethod
    async def _add_node(entity: EntityModel):
        pass 
    
    @abstractmethod   
    async def _remove_node(name: str):
        pass
    
    @abstractmethod
    async def _change_node(name:str, new_type:str):
        pass
    
    @abstractmethod
    async def _merge_nodes(name:str, duplicate_name:str, result_entity:EntityModel):
        pass
    
    @abstractmethod
    async def _get_node(name: str) -> EntityModel:
        pass
    
    @abstractmethod
    async def _add_relationship(rel: RelationshipModel):
        pass
    
    @abstractmethod
    async def _remove_relationship(rel: RelationshipModel):
        pass
    
    @abstractmethod
    async def _get_relationships(name: str) -> list[RelationshipModel]:
        pass
    
    @abstractmethod
    async def _get_nodes_by_type(self, entity_type: str) -> list[EntityModel]:
        pass