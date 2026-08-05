from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import get_session
from main import bcrypt_context
from schemes import usuario_scheme, login_scheme


auth_rt = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario):
    token = f"advasvafvafv{id_usuario}"
    return token

@auth_rt.get("/")
async def home():
    """
    Endpoint padrão bixo
    """
    return {"mensagem": "Você está acessando a rota de autorização"}

@auth_rt.post("/criar_conta")
async def criar_conta(Usuario_scheme: usuario_scheme, session=Depends(get_session)):
    usuario = session.query(Usuario).filter(Usuario.email==Usuario_scheme.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="E-mail usuário já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(Usuario_scheme.senha)
        novo_usuario = Usuario(Usuario_scheme.nome, Usuario_scheme.email, senha_criptografada, Usuario_scheme.ativo, Usuario_scheme.admin)
        session.add(novo_usuario)
        session.commit()
        raise HTTPException(status_code=200, detail="Novo usuário cadstrado com sucesso")

@auth_rt.post("/login")
async def login(login_scheme: login_scheme ,session=Depends(get_session)):
    usuario = session.query(Usuario).filter(Usuario.email==login_scheme.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    else:
        access_token = criar_token(usuario.id)
        return {"Access-Token": access_token, "Token-type": "Bearer"}