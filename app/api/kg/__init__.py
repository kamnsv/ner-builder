from .entity import EntityApi
from .rel import RelationshipApi
from kg import Neo4jKG


class KnowledgeGraphApi(EntityApi, RelationshipApi, Neo4jKG):
    def __str__(self):
        return 'KnowledgeGraphApi'
    def set_routes(self, api: "APIRouter"):
        for base_cls in self.__class__.__mro__[1:]:  # Пропускаем текущий класс
            if hasattr(base_cls, 'set_routes'):
                base_cls.set_routes(self, api)
                