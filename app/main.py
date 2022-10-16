from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.product import product
from .routers import auth, user, cart

app = FastAPI()


origins = ["http://localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(cart.router)


@app.get("/")
def root():
    return "Success"
