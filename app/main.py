from fastapi import FastAPI
from .routers import auth, user, product, cart

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(cart.router)


@app.get("/")
def root():
    return "Success"
