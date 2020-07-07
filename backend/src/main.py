from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

origins = [
    "http://localhost:4000",
    "https://localhost:4000",
    "http://localhost:8080",
    "https://localhost:8080",
]


class RegisterData(BaseModel):
    email: str = None
    password: str = None


class Item(BaseModel):
    name: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/items/")
async def update_item(item: Item):
    return "success"


@app.get("/hello")
async def hello():
    return {"message": "Hello Hessong!"}


@app.post("/register")
async def register(credentials: RegisterData):
    return f"Hi, {credentials.email}, thank you for providing your password {credentials.password}!"


# async def register(name, pwd):
#     return f"The following was sent:\n{name}\t{pwd}"

