import json
import logging
import re

from pydantic import BaseModel, field_validator
    
class AnswerModel(BaseModel):
    text: str
    
    @field_validator('text')
    @classmethod
    def text_cleaner(cls, value: str) -> str:
        value = re.sub(r'[ \r\f\v\u00A0\xa0\ufeff]+', ' ', value)
        return value.strip()  
    
    @property
    def json(self) -> dict:
        text = self.text.replace('```json', '')
        text = text.replace('```', '').strip()
        data = json.loads(text)
        logging.debug(data)
        return data
    