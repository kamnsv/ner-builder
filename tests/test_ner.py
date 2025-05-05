import unittest
import os
import json

import requests

url_api = os.getenv('TEST_API', 'http://localhost:9001/api')


class TestNamedEntityRecognitionAPI(unittest.TestCase):
    
    def test_search_ner(self):
        url = f'{url_api}/ner/search?lang='
        headers = {
            "accept": "application/json",
            "Content-Type": "text/plain"
        }
        with self.subTest("Check not NER"):
            response = requests.post(url+'en', headers=headers, data='string')
            self.assertEqual(response.status_code, 200, 
                            f"Expected status 200, got {response.status_code}. Response: {response.text}")
            self.assertEqual(response.text, "[]", 
                            f"Response: {response.text}")
            
        with self.subTest("Check search NER for english text"):
            test_text = "Apple was founded by Steve Jobs and Steve Wozniak in Cupertino, California."
            test_ner = [
                {"name": "Apple", "type": "ORG"},
                {"name": "Steve Jobs", "type": "PERSON"},
                {"name": "Steve Wozniak", "type": "PERSON"},
                {"name": "Cupertino", "type": "LOCATION"},
                {"name": "California", "type": "LOCATION"}
            ]
            response = requests.post(url+'en', headers=headers, data=test_text)
            self.assertEqual(response.status_code, 200, 
                            f"Expected status 200, got {response.status_code}. Response: {response.text}")
            self.assertEqual({tuple(sorted(e.items())) for e in json.loads(response.text)},
                             {tuple(sorted(e.items())) for e in test_ner},
                            f"Response: {response.text}")
            
            
        with self.subTest("Check search NER for russian text"):
            test_text = "Компания Яндекс была основана Аркадием Воложем и Ильёй Сегаловичем в Москве."
            test_ner = [
                {"name": "Яндекс", "type": "ORG"},
                {"name": "Аркадий Воложи", "type": "PERSON"},
                {"name": "Илье Сегалович", "type": "PERSON"},
                {"name": "Москва", "type": "LOCATION"}
            ]
            response = requests.post(url+'ru', headers=headers, data=test_text)
            self.assertEqual(response.status_code, 200, 
                            f"Expected status 200, got {response.status_code}. Response: {response.text}")
            self.assertEqual({tuple(sorted(e.items())) for e in json.loads(response.text)},
                             {tuple(sorted(e.items())) for e in test_ner},
                            f"Response: {response.text}")
            