from fastapi import FastAPI
from .routers import auth, user, product

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(product.router)


@app.get("/")
def root():
    return "Success"
