import unittest
import uuid
import os
import json

import requests

url_api = os.getenv('TEST_API', 'http://localhost:9001/api')


class TestKnownledgeGraphAPI(unittest.TestCase):
    
    def create_entity(self, data: list[dict]) -> tuple[int, str]:
        url = f'{url_api}/kg/entities'
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=data, headers=headers)
        return response.status_code, response.text
    
    def delete_entity(self, name:str) -> tuple[int, str]:
        url = f'{url_api}/kg/entity/{name}'
        headers = {
            "accept": "application/json"
        }
        response = requests.delete(url, headers=headers)
        return response.status_code, response.text
    
    def get_entities_by_type(self, name_type) -> tuple[int, str]:
        url = f'{url_api}/kg/entities/{name_type}'
        headers = {
            "accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        return response.status_code, response.text
    
    def read_entity(self, name:str) -> tuple[int, str]:
        url = f'{url_api}/kg/entity/{name}'
        response = requests.get(url)
        return response.status_code, response.text
    
    def update_entity_type(self, data: dict) -> tuple[int, str]:
        url = f'{url_api}/kg/entity?name=%(name)s&new_type=%(new_type)s' % data
        headers = {
            "accept": "application/json"
        }
        response = requests.put(url, headers=headers)
        return response.status_code, response.text
        
    def merge_entities_type(self, name1:str, name2: str, data: dict) -> tuple[int, str]:
        url = f'{url_api}/kg/entities/merge?entity_name={name1}&duplicate_name={name2}'
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=data, headers=headers)
        return response.status_code, response.text
    
    
    def add_relationships(self, rels: list[dict]):
        url = f'{url_api}/kg/relationships'
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=rels, headers=headers)
        return response.status_code, response.text
    
    def del_relationship(self, rel: dict):
        url = f'{url_api}/kg/relationship'
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.delete(url, json=rel, headers=headers)
        return response.status_code, response.text 
    
    def get_relationships(self, subject:str) -> list[dict]:
        url = f'{url_api}/kg/relationships/{subject}'
        response = requests.get(url)
        return response.status_code, response.text
        
    def test_crud_entity(self):
        random_name = str(uuid.uuid4()).title()
        random_name2 = str(uuid.uuid4()).title()
        random_type = f"type_{uuid.uuid4().hex[:8]}".upper() 
        entity = {'name': random_name, 'type': random_type}
        entity_new = {'name': random_name, 'new_type': f"type_{uuid.uuid4().hex[:8]}".upper()}

        with self.subTest("Create entity"):
            code, text = self.create_entity([entity])    
            self.assertEqual(code, 200, 
                        f"Expected status 200, got {code}. "
                        f"Response: {text}")
        
        with self.subTest("Get entities by type"):
            code, text = self.get_entities_by_type(random_type)    
            self.assertEqual(code, 200, 
                        f"Expected status 200, got {code}. "
                        f"Response: {text}")
            self.assertEqual(json.loads(text), [entity], 
                        f"Response: {text}")
        
        with self.subTest("Update entity type"):
            code, text = self.update_entity_type(entity_new)
            self.assertEqual(code, 200, 
                        f"Expected status 200, got {code}. "
                        f"Response: {text}")   
        
        with self.subTest("Merge entities"):
            code, text = self.merge_entities_type(random_name, random_name2, entity)
            self.assertEqual(code, 200, 
                        f"Expected status 200, got {code}. "
                        f"Response: {text}")
                
        with self.subTest("Delete entity"):
            code, text = self.delete_entity(random_name)    
            self.assertEqual(code, 200, 
                        f"Expected status 200, got {code}. "
                        f"Response: {text}")


    def test_for_non_existent_data(self):
        random_name = str(uuid.uuid4()).title()
        random_type = f"type_{uuid.uuid4().hex[:8]}".upper() 
        entity_new = {'name': random_name, 'new_type': random_type}
        with self.subTest("Read not existing entity"):
            code, text = self.read_entity(random_name)
            self.assertEqual(code, 404, 
                        f"Expected status 404, got {code}. "
                        f"Response: {text}")
            self.assertEqual(text, f'{{"detail":"Сущность {random_name} не найдена"}}')
    
        with self.subTest("Read not existing type entity"):
            code, text = self.get_entities_by_type(random_type)
            self.assertEqual(code, 404, 
                        f"Expected status 404, got {code}. "
                        f"Response: {text}")
            self.assertEqual(text, f'{{"detail":"Сущностей типа {random_type} не найдены"}}')
            
        with self.subTest("Delete not existing entity"):
            code, text = self.delete_entity(random_name)
            self.assertEqual(code, 404, 
                        f"Expected status 404, got {code}. "
                        f"Response: {text}")
        
        with self.subTest("Update not existing entity"):
            code, text = self.update_entity_type(entity_new)
            self.assertEqual(code, 404, 
                        f"Expected status 404, got {code}. "
                        f"Response: {text}")
            
            
    def test_entities_relationships(self):
        random_subject = str(uuid.uuid4()).title()
        random_subject_type = f"type_{uuid.uuid4().hex[:8]}".upper()        
        random_object = str(uuid.uuid4()).title()
        random_object_type = f"type_{uuid.uuid4().hex[:8]}".upper()        
        random_action = f"action {uuid.uuid4().hex[:8]}".lower()   
        
        payload = [
                {
                    "subject": random_subject,
                    "subject_type": random_subject_type,
                    "action": random_action,
                    "object": random_object,
                    "object_type": random_object_type
                }
        ]
        
        with self.subTest("Add new relationships"):
            code, text = self.add_relationships(payload)
            self.assertEqual(code, 200, 
                        f"Expected status 200, got {code}. "
                        f"Response: {text}")
        
        
        with self.subTest("Read relationships for subject"):
            code, text = self.get_relationships(random_subject)
            self.assertEqual(code, 200, 
                        f"Expected status 200, got {code}. "
                        f"Response: {text}")
            self.assertEqual(json.loads(text), payload, 
                        f"Response: {text}")
        
        with self.subTest("Read relationships for object"):
            code, text = self.get_relationships(random_object)
            self.assertEqual(code, 200, 
                        f"Expected status 200, got {code}. "
                        f"Response: {text}")
            self.assertEqual(len(json.loads(text)), 0, 
                        f"Response: {text}")
            
        with self.subTest("Delete relationship"):
            code, text = self.del_relationship(payload[0])
            self.assertEqual(code, 200, 
                        f"Expected status 200, got {code}. "
                        f"Response: {text}")
        
        with self.subTest("Delete subject"):
            code, text = self.delete_entity(random_subject)
            self.assertEqual(code, 200, 
                        f"Expected status 200, got {code}. "
                        f"Response: {text}")    
        
        with self.subTest("Delete object"):
            code, text = self.delete_entity(random_object)
            self.assertEqual(code, 200, 
                        f"Expected status 200, got {code}. "
                        f"Response: {text}")        
        