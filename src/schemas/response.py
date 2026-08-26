from pydantic import BaseModel


class Fonte(BaseModel):
    titulo: str
    trecho: str


class RespostaComFonte(BaseModel):
    resposta: str
    fontes: list[Fonte]
    