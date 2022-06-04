from typing import List
from fastapi import APIRouter

import api.schemas.task as task_schema

router = APIRouter()

# @で始まるデコレーターで関数に対してパスオペレーションの処理を追加する
# @app.operation(path) の形式で定義する
# -> @app.get('/task') は/taskのパスへGETでアクセスするという意味
# -> @app.get('/task', response_model=List[task_schema.Task]) のように設定し、Taskをリストに詰め込んで戻すことを明示している
@router.get('/tasks', response_model=List[task_schema.Task])
async def list_tasks():
    """
    TODOタスクの一覧を取得する
    """
    # とりあえずはダミーの値を常に戻すようにする
    # デフォルト値が入っているdoneは指定しなくてもOK
    return [task_schema.Task(id=1, title='1つ目のTODOタスク')]

# response_modelにレスポンスとして戻したい値の定義を設定
@router.post('/tasks', response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate):
    """
    新たなTODOタスクを作成する

    Args:
        task_body:
            task_schema.TaskCreateのインスタンス
    """
    return task_schema.TaskCreateResponse(id=1, **task_body.dict())
    # dictインスタンスに対して先頭に**を付けることでdictをキーワード引数として展開できる
    # つまり、以下の挙動と同義になる
    # -> return task_schema.TaskCreateResponse(id=1, title=task_body.title, done=task_body.done)


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
