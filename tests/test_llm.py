import unittest
import os
import json

import requests

url_api = os.getenv('TEST_API', 'http://localhost:9000/api')

class TestLargeLanguageModelAPI(unittest.TestCase):
    
    def test_llm_instructions(self):
        url = f'{url_api}/llm/instructions?return_type='
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

        with self.subTest("Check determinate text answer"):
            response = requests.post(url + 'text', headers=headers, json={
                    "system_prompt": "Ты простой парень",
                    "user_query": "Привет!"
                })
        
            self.assertEqual(response.status_code, 200, 
                                f"Expected status 200, got {response.status_code}. Response: {response.text}")
            self.assertEqual(response.text.strip(),
                                '"Привет! Да, я простой парень, всегда готов помочь с вопросами или просто поболтать. Как я могу помочь тебе сегодня?"',
                                f"Response: {response.text}")
        
        with self.subTest("Check determinate json answer"):
            response = requests.post(url + 'json', headers=headers, json={
                "system_prompt": "You're a simple guy. Reply in JSON format",
                "user_query": "Hello!"
            })
        
            self.assertEqual(response.status_code, 200, 
                                f"Expected status 200, got {response.status_code}. Response: {response.text}")
            self.assertEqual(json.loads(response.text),
                            {"message": "Hello!"},
                            f"Response: {response.text}")
            
    def test_llm_build_kg(self):
        url = f'{url_api}/llm/knowledge_graph?lang='
        headers = {
            "accept": "application/json",
            "Content-Type": "text/plain"
        }
        with self.subTest("Build knowledge graph for english text"):
            test_text = "Apple was founded by Steve Jobs and Steve Wozniak in Cupertino, California."
            test_kg = [
                {
                    "subject": "Steve Jobs",
                    "subject_type": "PERSON",
                    "action": "founder",
                    "object": "Apple",
                    "object_type": "ORG"
                },
                {
                    "subject": "Steve Wozniak",
                    "subject_type": "PERSON",
                    "action": "founder",
                    "object": "Apple",
                    "object_type": "ORG"
                },
                {
                    "subject": "Apple",
                    "subject_type": "ORG",
                    "action": "founded in",
                    "object": "Cupertino",
                    "object_type": "LOCATION"
                },
                {
                    "subject": "Apple",
                    "subject_type": "ORG",
                    "action": "founded in",
                    "object": "California",
                    "object_type": "LOCATION"
                }
            ]            
            
            response = requests.post(url+'en', headers=headers, data=test_text)
            self.assertEqual(response.status_code, 200, 
                            f"Expected status 200, got {response.status_code}. Response: {response.text}")
            self.assertEqual({tuple(sorted(e.items())) for e in json.loads(response.text)},
                             {tuple(sorted(e.items())) for e in test_kg},
                            f"Response: {response.text}")
            
            
        with self.subTest("Check knowledge graph for russian text"):
            test_text = "Компания Яндекс была основана Аркадием Воложем и Ильёй Сегаловичем в Москве."
            test_kg = [
                {
                    "subject": "Яндекс",
                    "subject_type": "ORG",
                    "action": "была основана",
                    "object": "Аркадий Волож",
                    "object_type": "PERSON"
                },
                {
                    "subject": "Яндекс",
                    "subject_type": "ORG",
                    "action": "была основана",
                    "object": "Илья Сегалович",
                    "object_type": "PERSON"
                },
                {
                    "subject": "Аркадий Волож",
                    "subject_type": "PERSON",
                    "action": "основал",
                    "object": "Яндекс",
                    "object_type": "ORG"
                },
                {
                    "subject": "Илья Сегалович",
                    "subject_type": "PERSON",
                    "action": "основал",
                    "object": "Яндекс",
                    "object_type": "ORG"
                },
                {
                    "subject": "Яндекс",
                    "subject_type": "ORG",
                    "action": "была основана",
                    "object": "Москва",
                    "object_type": "LOCATION"
                }
            ]
            response = requests.post(url+'ru', headers=headers, data=test_text)
            self.assertEqual(response.status_code, 200, 
                            f"Expected status 200, got {response.status_code}. Response: {response.text}")
            self.assertEqual({tuple(sorted(e.items())) for e in json.loads(response.text)},
                             {tuple(sorted(e.items())) for e in test_kg},
                            f"Response: {response.text}")
            