from models import db
from sqlalchemy.orm import sessionmaker, session
from models import Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_scheme

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_scheme), session=Depends(get_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado. Verifique a validade do token.")
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso negado.")

