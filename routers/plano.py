from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from groq import Groq
from dotenv import load_dotenv
import httpx
import os

load_dotenv()  # ← carrega o .env ANTES de inicializar o Groq

from models.database import get_db
from models.plano import Plano
from schemas.plano_schema import PlanoRequest, PlanoResponse
from routers.auth import SECRET_KEY, ALGORITHM

router = APIRouter()
bearer = HTTPBearer()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    http_client=httpx.Client(verify=False)  # ← ignora SSL do proxy corporativo
)

# ── Pega o usuário pelo token ──────────────────────────────────
def get_usuario_id(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido.")

# ── Gerar plano com IA ─────────────────────────────────────────
@router.post("/gerar", response_model=PlanoResponse)
def gerar_plano(
    dados: PlanoRequest,
    usuario_id: str = Depends(get_usuario_id),
    db: Session = Depends(get_db),
):
    prompt = f"""
Você é um professor especialista. Crie um plano de estudo completo e didático.

Matéria:  {dados.materia}
Nível:    {dados.nivel}
Conteúdo: {dados.conteudo}

O plano deve conter:
1. Visão geral do conteúdo (2-3 parágrafos)
2. Cronograma semanal detalhado (5 dias)
3. Tópicos principais a estudar
4. Recursos recomendados (livros, sites, vídeos)
5. Dicas de estudo para fixar o conteúdo
6. Mini-teste com 5 questões de múltipla escolha com gabarito

Responda em português, de forma clara e organizada usando Markdown.
"""

    try:
        resposta = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
        )
        plano_ia = resposta.choices[0].message.content

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na IA: {str(e)}")

    plano = Plano(
        usuario_id=usuario_id,
        materia=dados.materia,
        nivel=dados.nivel,
        conteudo=dados.conteudo,
        plano_ia=plano_ia,
    )
    db.add(plano)
    db.commit()
    db.refresh(plano)

    return plano
