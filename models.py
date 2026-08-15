from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey 
from sqlalchemy.orm import declarative_base, relationship #Base do banco de dados, facilitando o ORM
from sqlalchemy_utils.types import ChoiceType

db = create_engine("sqlite:///banco.db")
base = declarative_base() 

class Usuario(base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(base):
    __tablename__ = "pedidos"

    """STATUS_PEDIDOS = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO")
    )"""

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    status = Column("status", String) # pendente, cancelado, finalizado
    usuario = Column("usuario", String, ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    itens = relationship("ItemPedido", cascade="all, delete")

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.status = status
        self.usuario = usuario
        self.preco = preco

    def calcular_preco(self):
       self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)

class ItemPedido(base):
    __tablename__ = "itens_pedido"

    """tam = (
        ("PEQUENO", "PEQUENO"),
        ("MEDIO", "MEDIO"),
        ("GRANDE", "GRANDE")
    )"""

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido