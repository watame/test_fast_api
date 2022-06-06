from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.done as done_schema
import api.cruds.done as done_crud
from api.db import get_db

router = APIRouter()

# @で始まるデコレーターで関数に対してパスオペレーションの処理を追加する
# @app.operation(path) の形式で定義する
# -> @app.get('/tasks/{task_id}/done') は/task/1/done のようなパスへGETでアクセスするという意味
@router.put('/tasks/{task_id}/done', response_model=done_schema.DoneResponse)
async def check_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    IDが合致する既存のTODOタスクを完了状態にする

    Args:
        task_id:
            URIに含まれるタスクインスタンスのID
        db:
            DB接続先を決める関数（Dependency Injection、依存性注入）
    """
    done = await done_crud.get_done(db, task_id)
    # データが既に存在している = 既に完了済みとなっている
    if done is not None:
        raise HTTPException(status_code=400, detail='Done already exists')

    return await done_crud.create_done(db, task_id)

@router.delete('/tasks/{task_id}/done', response_model=None)
async def uncheck_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    IDが合致する既存のTODOタスクを未完了状態にする

    Args:
        task_id:
            URIに含まれるタスクインスタンスのID
        db:
            DB接続先を決める関数（Dependency Injection、依存性注入）
    """
    done = await done_crud.get_done(db, task_id)
    # データが既に存在していない = まだ完了済みになっていない
    if done is None:
        raise HTTPException(status_code=404, detail='Done not found')

    return await done_crud.delete_done(db, done)
