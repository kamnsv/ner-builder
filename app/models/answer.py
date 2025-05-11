import json
import logging
import re

from pydantic import BaseModel, field_validator
    
class AnswerModel(BaseModel):
    text: str
    
    @field_validator('text')
    @classmethod
    def text_cleaner(cls, value: str) -> str:
        text = re.sub(r'[ \r\f\v\u00A0\xa0\ufeff]+', ' ', value).strip()  
        logging.debug(f"{text=}")
        return text
    
    @property
    def json(self) -> dict:
        text = self.text.replace('```json', '')
        text = text.replace('```', '').strip()
        data = json.loads(text)
        logging.debug(f"json={data}")
        return data
    