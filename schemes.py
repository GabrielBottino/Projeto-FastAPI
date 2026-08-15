from pydantic import BaseModel
from typing import Optional

class usuario_scheme(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True

class pedido_scheme(BaseModel):
    usuario: int

    class Config:
        from_attributes = True

class login_scheme(BaseModel):
    email: str
    senha: str

    class Config():
        from_attributes = True

class item_pedido_scheme(BaseModel):
        quantidade: int
        sabor: str
        tamanho: str
        preco_unitario: float

        class Config():
            from_attributes = True