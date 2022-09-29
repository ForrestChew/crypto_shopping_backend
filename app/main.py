from fastapi import FastAPI
from .routers import auth, user

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return "Success"
