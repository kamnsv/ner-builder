from pydantic import BaseModel
    
class AnswerModel(BaseModel):
    text: str
    
    @property
    def json(self) -> str:
        return self.text