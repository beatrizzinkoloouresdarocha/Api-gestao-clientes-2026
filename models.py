from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    cep: Mapped[str] = mapped_column(nullable=False)
    logradouro: Mapped[str | None] = mapped_column(default=None)
    bairro: Mapped[str | None] = mapped_column(default=None)
    cidade: Mapped[str | None] = mapped_column(default=None)
    uf: Mapped[str | None] = mapped_column(default=None)