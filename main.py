from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

app = FastAPI()

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

from rt_order import order_rt
from rt_auth import auth_rt

app.include_router(auth_rt)
app.include_router(order_rt)

