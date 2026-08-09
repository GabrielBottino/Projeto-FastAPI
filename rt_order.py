from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session, verificar_token
from schemes import pedido_scheme
from models import Pedido, Usuario


order_rt = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

@order_rt.get("/")
async def pedidos():
    return {"mensagem": "Você acessou a rota de pedidos"}

@order_rt.post("/pedido")
async def criar_pedido(pedido_scheme: pedido_scheme, session=Depends(get_session)):
    novo_pedido = Pedido(usuario=pedido_scheme.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem" : f"Pedido criado com sucesso. ID Pedido {pedido_scheme.usuario}"}

@order_rt.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session=Depends(get_session), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado.")
    if not usuario.adm or usuario.id != pedido.usuario:
        raise HTTPException(status_code=400, detail="O usuário não tem permissão para editar esse pedido.")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido com id {pedido.id} cancelado com sucesso",
        "pedido": pedido
    }

