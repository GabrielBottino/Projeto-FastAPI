from fastapi import FastAPI

app = FastAPI()

from rt_order import order_rt
from rt_auth import auth_rt

app.include_router(auth_rt)
app.include_router(order_rt)

