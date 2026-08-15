from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session, verificar_token
from schemes import pedido_scheme, item_pedido_scheme
from models import Pedido, Usuario, ItemPedido


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

@order_rt.get("/listar")
async def listar_pedidos(session= Depends(get_session), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Usuario não autorizado.")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }

@order_rt.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item(id_pedido: int, item_pedido_scheme: item_pedido_scheme,session= Depends(get_session), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=401, detail="Pedido não encontrado.")
    elif usuario.id != pedido.usuario and not usuario.admin:
        raise HTTPException(status_code=401, detail="Usuário não tem permissão de editar pedido.")
    item_pedido = ItemPedido(
        item_pedido_scheme.quantidade,
        item_pedido_scheme.sabor,
        item_pedido_scheme.tamanho,
        item_pedido_scheme.preco_unitario,
        id_pedido
    )
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {"mensagem": "Item criado",
            "id_item": item_pedido.id,
            "preco_pedido": pedido.preco}