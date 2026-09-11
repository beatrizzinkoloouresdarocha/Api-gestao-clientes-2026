from database import Base
from sqlalchemy import Column, Integer, String


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    cep = Column(String, nullable=False)
    logradouro = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    uf = Column(String)