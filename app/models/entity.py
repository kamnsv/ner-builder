from pydantic import field_validator

from .types import TypesModel


class EntityModel(TypesModel):
    name: str = ""
    type: str = ""

    @field_validator('name', 'type')
    @classmethod
    def fix_properties(cls, value: str, info):
        if info.field_name == 'name':
            return cls.handler_name(value)
        elif info.field_name == 'type':
            return cls.mapping_type(value)
        return value