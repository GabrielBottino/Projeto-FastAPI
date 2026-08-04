from fastapi import APIRouter

auth_rt = APIRouter(prefix="/auth", tags=["auth"])

@auth_rt.get("/")
async def autorizacao():
    """
    Endpoint padrão bixo
    """
    return {"mensagem": "Você está acessando a rota de autorização"}