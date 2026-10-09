from pydantic import BaseModel, EmailStr

class CadastroSchema(BaseModel):
    nome:  str
    email: EmailStr
    senha: str

class LoginSchema(BaseModel):
    email: EmailStr
    senha: str

class UsuarioPublico(BaseModel):
    id:    str
    nome:  str
    email: str

    model_config = {"from_attributes": True}  # ✅ Pydantic v2
