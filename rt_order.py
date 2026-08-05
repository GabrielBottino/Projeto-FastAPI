from fastapi import APIRouter, Depends
#from sqlalchemy.orm import Session
from dependencies import get_session
from schemes import pedido_scheme
from models import Pedido

order_rt = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_rt.get("/")
async def pedidos():
    return {"mensagem": "Você acessou a rota de pedidos"}

@order_rt.post("/pedido")
async def criar_pedido(pedido_scheme: pedido_scheme, session=Depends(get_session)):
    novo_pedido = Pedido(usuario=pedido_scheme.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem" : f"Pedido criado com sucesso. ID Pedido {pedido_scheme.usuario}"}