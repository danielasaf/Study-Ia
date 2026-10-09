from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from models.database import Base
import uuid

class Usuario(Base):
    __tablename__ = "usuarios"

    id         = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nome       = Column(String, nullable=False)
    email      = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    criado_em  = Column(DateTime(timezone=True), server_default=func.now())
