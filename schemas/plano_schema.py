from pydantic import BaseModel

class PlanoRequest(BaseModel):
    materia:  str
    nivel:    str
    conteudo: str

class PlanoResponse(BaseModel):
    id:       str
    materia:  str
    nivel:    str
    conteudo: str
    plano_ia: str

    model_config = {"from_attributes": True}
