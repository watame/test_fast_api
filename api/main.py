from fastapi import FastAPI
from api.routers import task

# uvicornを通じて参照されるインスタンス
app = FastAPI()

# 定義したルーティング定義を読み込む
app.include_router(task.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
