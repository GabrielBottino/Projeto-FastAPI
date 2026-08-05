from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

from rt_order import order_rt
from rt_auth import auth_rt

app.include_router(auth_rt)
app.include_router(order_rt)

