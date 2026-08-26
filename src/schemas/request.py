from pydantic import BaseModel


class RequestModel(BaseModel):
    pergunta: str
