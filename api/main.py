from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import task, done

# uvicornを通じて参照されるインスタンス
app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定義したルーティング定義を読み込み、エンドポイントを追加する
app.include_router(task.router)
app.include_router(done.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
