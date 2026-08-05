from fastapi import APIRouter, Depends
from models import Usuario
from dependencies import get_session

auth_rt = APIRouter(prefix="/auth", tags=["auth"])

@auth_rt.get("/")
async def home():
    """
    Endpoint padrão bixo
    """
    return {"mensagem": "Você está acessando a rota de autorização"}

@auth_rt.post("/criar_conta")
async def criar_conta(email: str, senha: str, nome: str, session=Depends(get_session)):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:
        return {"mensagem": "Já existe um usuário no email"}
    else:
        novo_usuario = Usuario(nome, email, senha)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "usuário cadstrado com sucesso"}