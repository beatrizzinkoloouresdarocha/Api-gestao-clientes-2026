from pydantic import BaseModel, EmailStr


class ClienteCreate(BaseModel):
    nome: str
    email: EmailStr
    cep: str


class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: str
    cep: str
    logradouro: str | None
    bairro: str | None
    cidade: str | None
    uf: str | None

    class Config:
        from_attributes = True