from pydantic import BaseModel, ConfigDict, EmailStr


class ClienteCreate(BaseModel):
    nome: str
    email: EmailStr
    cep: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "Fernando Souza",
                "email": "fernando.souza@email.com",
                "cep": "01001000",
            }
        }
    )


class ClienteResponse(ClienteCreate):
    id: int
    logradouro: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    uf: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nome": "Fernando Souza",
                "email": "fernando.souza@email.com",
                "cep": "01001000",
                "logradouro": "Praça da Sé",
                "bairro": "Sé",
                "cidade": "São Paulo",
                "uf": "SP",
            }
        },
    )