from pydantic import BaseModel, field_validator

from .types import TypesModel


class RelationshipModel(TypesModel):
    subject: str
    subject_type: str
    action: str
    object: str
    object_type: str
    
    @field_validator('action')
    @classmethod
    def strip_and_lower(cls, value: str) -> str:
        return value.strip().lower().replace("_", " ")    
    
    @field_validator('subject', 'object')
    @classmethod
    def strip_and_title(cls, value: str):
        return cls.handler_name(value)
    
    @field_validator('subject_type', 'object_type')
    @classmethod
    def strip_and_upper(cls, value: str):
        return cls.mapping_type(value)
    