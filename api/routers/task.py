from fastapi import APIRouter

router = APIRouter()

# @で始まるデコレーターで関数に対してパスオペレーションの処理を追加する
# @app.operation(path) の形式で定義する
# -> @app.get('/task') は/taskのパスへGETでアクセスするという意味
@router.get('/tasks')
async def list_tasks():
    """
    TODOタスクの一覧を取得する
    """
    # 後で処理を追加するのでpassを記載しておく
    # pass -> 何もしないことを明示する書き方
    pass

@router.post('/tasks')
async def create_task():
    """
    新たなTODOタスクを作成する
    """
    pass

@router.put('/tasks/{task_id}')
async def update_task():
    """
    IDが合致する既存のTODOタスクを更新する
    """
    pass

@router.delete('/tasks/{task_id}')
async def delete_task():
    """
    IDが合致する既存のTODOタスクを削除する
    """
    pass
