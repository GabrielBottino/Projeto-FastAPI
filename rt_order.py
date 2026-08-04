from fastapi import APIRouter

order_rt = APIRouter(prefix="/order", tags=["order"])

@order_rt.get("/")
async def pedidos():
    return {"mensagem": "Você acessou a rota de pedidos"}