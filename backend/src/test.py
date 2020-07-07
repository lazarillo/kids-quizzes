from typing import Optional, Union

from pydantic import BaseModel
from starlette.testclient import TestClient

from fastapi import FastAPI


class SimpleData(BaseModel):
    foo: Optional[str] = None


class ExtendedData(SimpleData):
    bar: str # Note that this is required


PostData = Union[ExtendedData, SimpleData]


app = FastAPI()
client = TestClient(app)
@app.post("/testunion")
async def testunion(data: PostData):
    print(data)
    return "ok"


def test_union():
    data = PostData(foo="test1", bar="test2")
    response = client.post("/testunion", json=data.dict())
    assert response.status_code == 200
    assert response.json() == "ok"
    data = {"foo": "test1", "bar": "test2"}
    response = client.post("/testunion", json=data)
    assert response.status_code == 200
    assert response.json() == "ok"
