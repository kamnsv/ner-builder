from neo4j import AsyncGraphDatabase

from .kg import KnowledgeGraph
from models import EntityModel, RelationshipModel
from cfg import kg_url, kg_user, kg_pswd
    
    
class Neo4jKG(KnowledgeGraph):        
    def __init__(self):
        self._driver = AsyncGraphDatabase.driver(kg_url, auth=(kg_user, kg_pswd))

    async def close(self):
        await self._driver.close()

    async def _add_node(self, entity: EntityModel):
        query = f"MERGE (n:{entity.type} {{name: $name}})"
        async with self._driver.session() as session:
            await session.run(query, name=entity.name)

    async def _remove_node(self, name: str) -> bool:
        query_check = "MATCH (n {name: $name}) RETURN count(n) as count"
        query_delete = "MATCH (n {name: $name}) DETACH DELETE n"
        async with self._driver.session() as session:
            result = await session.run(query_check, name=name)
            record = await result.single()
            count = record["count"] if record else 0
            if count == 0:
                return False
            await session.run(query_delete, name=name)
            return True
            
    async def _remove_node_spec_type(self, entity: EntityModel):
        query = f"MATCH (n:{entity.type} {{name: $name}}) DETACH DELETE n"
        async with self._driver.session() as session:
            await session.run(query, name=entity.name)
            
    async def _change_node(self, name: str, new_type: str) -> bool:
        entity = EntityModel(name=name, type=new_type)
        query = (
            "MATCH (n {name: $name}) "
            "WITH n, labels(n) AS old_labels "
            "CALL apoc.create.removeLabels(n, old_labels) YIELD node AS n1 "
            "CALL apoc.create.addLabels(n1, [$new_type]) YIELD node "
            "RETURN count(node) AS updated_count"
        )
        
        async with self._driver.session() as session:
            result = await session.run(
                query,
                name=entity.name,
                new_type=entity.type
            )
            record = await result.single()
            updated_count = record["updated_count"] if record else 0
            return updated_count > 0


    async def _get_node(self, name: str) -> EntityModel | None:
        entity = EntityModel(name=name)
        query = (
            "MATCH (n {name: $name}) "
            "RETURN n.name AS name, "
            "head(labels(n)) AS type"  # Берём первую метку как тип
        )
        async with self._driver.session() as session:
            result = await session.run(query, name=entity.name)
            record = await result.single()
            if record:
                return EntityModel(name=record["name"], type=record["type"])
            return None

    async def _get_nodes_by_type(self, entity_type: str) -> list[EntityModel]:
        """
        Возвращает все сущности указанного типа (метки)
        
        :param entity_type: Метка узла (например "PERSON", "ORGANIZATION")
        :return: Список EntityModel
        """
        entity = EntityModel(type=entity_type)
        query = (
            "MATCH (n:%s) "  # Фильтр по конкретной метке
            "RETURN n.name AS name, "
            "labels(n) AS types"  # Все метки узла
            % entity.type
        )
        
        async with self._driver.session() as session:
            result = await session.run(query)
            nodes = []
            async for record in result:
                # Используем основную метку как тип
                main_type = record["types"][0] if record["types"] else EntityModel(type="UNKNOWN").type
                nodes.append(EntityModel(
                    name=record["name"],
                    type=main_type
                ))
            return nodes


    async def _add_relationship(self, rel: RelationshipModel):
        query = (
            "MERGE (a:`$subject_type` {name: $subject}) "
            "MERGE (b:`$object_type` {name: $object}) "
            "MERGE (a)-[r:`$action`]->(b) "
        ).replace("$subject_type", rel.subject_type.upper()) \
        .replace("$object_type", rel.object_type.upper()) \
        .replace("$action", rel.action.lower())
        
        async with self._driver.session() as session:
            await session.run(
                query,
                subject=rel.subject.title(),
                object=rel.object.title()
            )

    async def _remove_relationship(self, rel: RelationshipModel):
        query = (
            "MATCH (a {name: $subject})-[r:`%s`]->(b {name: $object}) "
            "DELETE r" % rel.action.lower()
        )
        async with self._driver.session() as session:
            await session.run(query, subject=rel.subject.title(), object=rel.object.title())

    async def _get_relationships(self, name: str) -> list[RelationshipModel]:
        query = (
            "MATCH (a {name: $name})-[r]->(b) "
            "RETURN a.name AS subject, type(r) AS action, b.name AS object, "
            "head(labels(a)) AS subject_type, "
            "head(labels(b)) AS object_type"
        )
        async with self._driver.session() as session:
            result = await session.run(query, name=name.title())
            rels = [RelationshipModel(**record) async for record in result]
            return rels
        
    async def _change_name(self, name: str, new_name: str):
        name = EntityModel(name=name).name
        new_name = EntityModel(name=new_name).name
        query = (
            "MATCH (n {name: $current_name}) "
            "SET n.name = $new_name "
            "RETURN n"
        )    
        async with self._driver.session() as session:
            result = await session.run(
                query,
                current_name=name,
                new_name=new_name
            )
    
    async def _take_relationships(self, name: str, doner_name: str):
        query = (
            "MATCH (a {name: $from_name})-[r]->(other) "
            "WITH a, r, other, type(r) AS rel_type "
            "MATCH (b {name: $to_name}) "
            "CALL apoc.create.relationship(b, rel_type, properties(r), other) "
            "YIELD rel "
            "DELETE r "
            
            "WITH a "
            "MATCH (other)-[r]->(a) "
            "WITH r, other, type(r) AS rel_type "
            "MATCH (b {name: $to_name}) "
            "CALL apoc.create.relationship(other, rel_type, properties(r), b) "
            "YIELD rel "
            "DELETE r"
        )
        name = EntityModel(name=name).name
        doner_name = EntityModel(name=doner_name).name
        async with self._driver.session() as session:
            await session.run(
                query,
                from_name=doner_name,
                to_name=name
            )
            
    async def _merge_nodes(self, name: str, duplicate_name: str, result_entity: EntityModel):
        name = EntityModel(name=name).name
        duplicate_name = EntityModel(name=duplicate_name).name
        await self._change_node(name, result_entity.type)
        await self._change_name(name, result_entity.name)
        await self._take_relationships(result_entity.name, duplicate_name)
        await self._remove_node(duplicate_name)

        
    async def _rename_relationship(self, node_a:str, node_b:str, old_type:str, new_type:str):
        query = (
            "MATCH (a {name: $node_a})-[r]->(b {name: $node_b}) "
            "WHERE type(r) = $old_type "
            "CALL apoc.refactor.setType(r, $new_type) "
            "YIELD input, output "
            "RETURN output"
        )
        
        async with self._driver.session() as session:
            await session.run(
                query,
                node_a=node_a,
                node_b=node_b,
                old_type=old_type,
                new_type=new_type
            )