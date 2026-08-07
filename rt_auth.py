from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import get_session, verificar_token
from main import bcrypt_context, ALGORITHM, ACESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemes import usuario_scheme, login_scheme
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm


auth_rt = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario,validade=timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + validade
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

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
async def login(login_scheme: login_scheme, session=Depends(get_session)):
    usuario = autenticar_usuario(login_scheme.email, login_scheme.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, validade=timedelta(days=7))
        return {"Access-Token": access_token, "refresh_token": refresh_token,"Token-type": "Bearer"}


@auth_rt.post("/login_form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    else:
        access_token = criar_token(usuario.id)
        return {"Access-Token": access_token, "Token-type": "Bearer"}

@auth_rt.get("/refresh")
async def use_refresh_token(usuario: Usuario=Depends(verificar_token)):
    print("")