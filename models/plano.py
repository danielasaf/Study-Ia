import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from models.database import Base

class Plano(Base):
    __tablename__ = "planos"

    id         = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario_id = Column(String, ForeignKey("usuarios.id"), nullable=False)
    materia    = Column(String, nullable=False)
    nivel      = Column(String, nullable=False)
    conteudo   = Column(String, nullable=False)
    plano_ia   = Column(Text, nullable=False)
    criado_em  = Column(DateTime(timezone=True), server_default=func.now())
