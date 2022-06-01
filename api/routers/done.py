from fastapi import APIRouter

router = APIRouter()

# @で始まるデコレーターで関数に対してパスオペレーションの処理を追加する
# @app.operation(path) の形式で定義する
# -> @app.get('/tasks/{task_id}/done') は/task/1/done のようなパスへGETでアクセスするという意味
@router.put('/tasks/{task_id}/done')
async def check_task_as_done():
    """
    IDが合致する既存のTODOタスクを完了状態にする
    """
    # 後で処理を追加するのでpassを記載しておく
    # pass -> 何もしないことを明示する書き方
    pass

@router.delete('/tasks/{task_id}/done')
async def uncheck_task_as_done():
    """
    IDが合致する既存のTODOタスクを未完了状態にする
    """
    pass
