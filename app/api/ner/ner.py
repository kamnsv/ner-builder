import os
import logging
from typing import Annotated
import json

from fastapi import APIRouter, Body, Query
import stanza
import stanza.resources.common

from ..router import Router
from models import EntityModel

def list_all_languages(model_dir=stanza.resources.common.DEFAULT_MODEL_DIR):
    path = os.path.join(model_dir, 'resources.json')
    if os.path.exists(path):
        try:
            stanza.download('en')
        except Exception as e:
            logging.error(f'Language {lang} download was failed: {e}')
            raise Exception(e)
        
    with open(os.path.join(model_dir, 'resources.json')) as fin:
        resources = json.load(fin)
    languages = [lang for lang in resources if 'alias' not in resources[lang]]
    return sorted(languages)

class NamedEntityRecognitionApi(Router):
    def set_routes(self, api: APIRouter):
        @api.post('/search', summary="Поиск именованных сущностей в тексте", 
                 description='''''')
        async def get_ner(text: str = Body(..., media_type="text/plain", description="Текст который нужно анализировать"),
                    lang: Annotated[str, Query(description="Язык текста", enum=list_all_languages())] = 'en'
                    ) -> list[EntityModel]:
            try:
                nlp = stanza.Pipeline(lang)
            except:
                logging.info(f'Language {lang} not found. Downloading...')
                stanza.download(lang)
                nlp = stanza.Pipeline(lang)

            doc = nlp(text)
            entities = []
            for ent in doc.ents:
                e = (ent.type, ent.text)
                if e not in entities:
                    entities.append(EntityModel(name=str(e[1]), type=str(e[0])))
            logging.debug(entities)
            return sorted(entities, key=lambda x: x.name)
                    