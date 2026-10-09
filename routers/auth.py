from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta
import bcrypt

from models.database import get_db
from models.usuario import Usuario
from schemas.auth_schema import CadastroSchema, LoginSchema, UsuarioPublico

router = APIRouter()

SECRET_KEY         = "chave-secreta-troque-em-producao"
ALGORITHM          = "HS256"
TOKEN_EXPIRE_HORAS = 24


def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha: str, hash: str) -> bool:
    return bcrypt.checkpw(senha.encode("utf-8"), hash.encode("utf-8"))


def criar_token(dados: dict) -> str:
    payload = dados.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HORAS)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/cadastro", status_code=status.HTTP_201_CREATED)
def cadastro(dados: CadastroSchema, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == dados.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    if len(dados.senha) < 6:
        raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 6 caracteres.")

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_senha(dados.senha),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return {"mensagem": "Conta criada com sucesso!"}


@router.post("/login")
def login(dados: LoginSchema, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")

    token = criar_token({"sub": usuario.id, "email": usuario.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": UsuarioPublico.model_validate(usuario),
    }
