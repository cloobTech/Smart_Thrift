from fastapi import FastAPI, APIRouter, Depends
from typing import Union
from .routes import user, user_profile

app = FastAPI()

app.include_router(user.router)
app.include_router(user_profile.router)




@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
