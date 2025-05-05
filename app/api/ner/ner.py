import os
import logging
from typing import Annotated
import json

from fastapi import APIRouter, Body, Query
import stanza
import stanza.resources.common

from ..router import Router
from models import EntityModel

class NamedEntityRecognitionApi(Router):
    
    langs = ['en', 'ru']
    ners = {}
    for lang in langs:
        try:
            ners[lang] = stanza.Pipeline(lang, use_gpu=True, device='cuda', dir=os.environ["STANZA_RESOURCES_DIR"])
        except:
            logging.info(f'Language {lang} not found. Downloading...')
            stanza.download(lang)
            ners[lang] = stanza.Pipeline(lang, use_gpu=True, device='cuda', dir=os.environ["STANZA_RESOURCES_DIR"])
            
    def lemmatize_entity(self, entity_text, lang) -> str:
        lemmas = []
        doc = self.ners[lang].process(entity_text)
        for sent in doc.sentences:
            for word in sent.words:
                lemmas.append(word.lemma)
        return ' '.join(lemmas)          
    
    def set_routes(self, api: APIRouter):
        @api.post('/search', summary="Поиск именованных сущностей в тексте", 
                 description='''''')
        async def get_ner(text: str = Body(..., media_type="text/plain", description="Текст который нужно анализировать"),
                    lang: Annotated[str, Query(description="Язык текста", enum=self.langs)] = 'en'
                    ) -> list[EntityModel]:
            doc = self.ners[lang](text)
            entities = []
            for ent in doc.ents:
                name = self.lemmatize_entity(ent.text, lang)
                e = EntityModel(name=name, type=ent.type)
                if e not in entities:
                    entities.append(e)
            logging.debug(entities)
            return sorted(entities, key=lambda x: x.name)
                    