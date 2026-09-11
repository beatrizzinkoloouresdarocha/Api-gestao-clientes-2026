import requests
from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException, status
import models
import schemas
from sqlalchemy.orm import Session

# Cria as tabelas no banco de dados ao iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestão de Clientes",
    description="API com integração ViaCEP e armazenamento SQLite.",
    version="1.0.0",
)


def buscar_endereco_por_cep(cep: str):
    # Remove caracteres não numéricos do CEP
    cep_limpo = "".join(filter(str.isdigit, cep))

    if len(cep_limpo) != 8:
        raise HTTPException(
            status_code=400, detail="CEP inválido. Deve conter 8 dígitos."
        )

    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        raise HTTPException(
            status_code=502, detail="Erro ao consultar o serviço ViaCEP."
        )

    dados = response.json()

    if "erro" in dados:
        raise HTTPException(status_code=404, detail="CEP não encontrado.")

    return dados


@app.post(
    "/clientes",
    response_model=schemas.ClienteResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_cliente(
    cliente_data: schemas.ClienteCreate, db: Session = Depends(get_db)
):
    # Verifica se já existe cliente com o mesmo email
    cliente_existente = (
        db.query(models.Cliente)
        .filter(models.Cliente.email == cliente_data.email)
        .first()
    )
    if cliente_existente:
        raise HTTPException(
            status_code=400, detail="E-mail já cadastrado no sistema."
        )

    # Consulta o ViaCEP
    dados_endereco = buscar_endereco_por_cep(cliente_data.cep)

    # Instancia o novo cliente no banco
    novo_cliente = models.Cliente(
        nome=cliente_data.nome,
        email=cliente_data.email,
        cep=cliente_data.cep,
        logradouro=dados_endereco.get("logradouro"),
        bairro=dados_endereco.get("bairro"),
        cidade=dados_endereco.get("localidade"),
        uf=dados_endereco.get("uf"),
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente


@app.get("/clientes", response_model=list[schemas.ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(models.Cliente).all()


@app.put("/clientes/{cliente_id}", response_model=schemas.ClienteResponse)
def atualizar_cliente(
    cliente_id: int,
    cliente_data: schemas.ClienteCreate,
    db: Session = Depends(get_db),
):
    cliente = (
        db.query(models.Cliente)
        .filter(models.Cliente.id == cliente_id)
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=404, detail="Cliente não encontrado."
        )

    # Consulta o ViaCEP para o novo CEP
    dados_endereco = buscar_endereco_por_cep(cliente_data.cep)

    cliente.nome = cliente_data.nome
    cliente.email = cliente_data.email
    cliente.cep = cliente_data.cep
    cliente.logradouro = dados_endereco.get("logradouro")
    cliente.bairro = dados_endereco.get("bairro")
    cliente.cidade = dados_endereco.get("localidade")
    cliente.uf = dados_endereco.get("uf")

    db.commit()
    db.refresh(cliente)

    return cliente