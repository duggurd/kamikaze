from fastapi import FastAPI
from pydantic import BaseModel


class E(BaseModel):
    name: str

app = FastAPI()


@app.get("/")
def home():
    return {"sdad":"sasdsa"}


@app.post("/")
def pst(e: E):
    print(e)
    return {"test":"testing"}

