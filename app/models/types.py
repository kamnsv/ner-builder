from pydantic import BaseModel


class TypesModel(BaseModel):
    @classmethod
    def mapping_type(cls, value: str):
        value = value.strip().upper()
        return {
            "GPE": "LOCATION",
            "LOC": "LOCATION",
            "PER": "PERSON",
        }.get(value, value)
    
    @classmethod
    def handler_name(cls, value: str):
        value = value.strip().title().replace('_',' ')
        return value