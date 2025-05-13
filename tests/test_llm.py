import unittest
import os
import json

import requests

url_api = os.getenv('TEST_API', 'http://localhost:8000/api')

class TestLargeLanguageModelAPI(unittest.TestCase):
               
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
            response = requests.post(url+'ru', headers=headers, data=test_text.encode('utf-8'))
            self.assertEqual(response.status_code, 200, 
                            f"Expected status 200, got {response.status_code}. Response: {response.text}")
            self.assertEqual({tuple(sorted(e.items())) for e in json.loads(response.text)},
                             {tuple(sorted(e.items())) for e in test_kg},
                            f"Response: {response.text}")
            
