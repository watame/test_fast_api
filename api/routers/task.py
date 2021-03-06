from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.task as task_schema
# ルーターはMVCのCの部分、肥大化しやすいのでCRUDモジュールとして切り出す
import api.cruds.task as task_crud
from api.db import get_db

router = APIRouter()

# @で始まるデコレーターで関数に対してパスオペレーションの処理を追加する
# @app.operation(path) の形式で定義する
# -> @app.get('/task') は/taskのパスへGETでアクセスするという意味
# -> @app.get('/task', response_model=List[task_schema.Task]) のように設定し、Taskをリストに詰め込んで戻すことを明示している
@router.get('/tasks', response_model=List[task_schema.Task])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    """
    TODOタスクの一覧を取得する
    """
    return await task_crud.get_tasks_with_done(db)

# response_modelにレスポンスとして戻したい値の定義を設定
@router.post('/tasks', response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)):
    """
    新たなTODOタスクを作成する

    Args:
        task_body:
            task_schema.TaskCreateのインスタンス
        db:
            DB接続先を決める関数（Dependency Injection、依存性注入）
    """
    return await task_crud.create_task(db, task_body)

@router.get('/tasks/{task_id}', response_model=task_schema.TaskCreateResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    IDが合致する既存のTODOタスクを取得する

    Args:
        task_id:
            URIに含まれるTaskインスタンスのID
        db:
            DB接続先を決める関数（Dependency Injection、依存性注入）
    """
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')

    return task

@router.put('/tasks/{task_id}', response_model=task_schema.TaskCreateResponse)
async def update_task(task_id: int, task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)):
    """
    IDが合致する既存のTODOタスクを更新する

    Args:
        task_id:
            URIに含まれるTaskインスタンスのID
        task_body:
            task_schema.TaskCreateのインスタンス
        db:
            DB接続先を決める関数（Dependency Injection、依存性注入）
    """
    # task_id に合致するTaskインスタンスを取得
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')

    return await task_crud.update_task(db, task_body, task)

@router.delete('/tasks/{task_id}', response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    IDが合致する既存のTODOタスクを削除する

    Args:
        task_id:
            URIに含まれるTaskインスタンスのID
        db:
            DB接続先を決める関数（Dependency Injection、依存性注入）
    """
    task = await task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')

    return await task_crud.delete_task(db, task)
