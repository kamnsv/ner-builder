from pydantic import BaseModel
    
class EntityModel(BaseModel):
    name: str
    type: str