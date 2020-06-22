from fastapi import FastAPI
from pydantic import BaseModel


class RegisterData(BaseModel):
    name: str = None
    pwd: str = None


app = FastAPI()


@app.get("/hello")
async def hello():
    return {"message": "Hello Hessong!"}


@app.post("/register/")
async def register(reg_data: RegisterData):
    return reg_data


# async def register(name, pwd):
#     return f"The following was sent:\n{name}\t{pwd}"

