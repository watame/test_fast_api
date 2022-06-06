from typing import List, Tuple, Optional
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

# Model定義とSchema定義を結合させてCRUD処理を作る
import api.models.task as task_model
import api.schemas.task as task_schema

async def create_task(
    db: AsyncSession, task_create: task_schema.TaskCreate
    ) -> task_model.Task:
    """
    新たなTODOタスクをDBに登録する

    Args:
        db:
            非同期DBセッションインスタンス
        task_create:
            task_schema.TaskCreateのインスタンス
    Return:
        TaskModelインスタンス
    """
    # スキーマをDBモデルに変換
    # dictインスタンスに対して先頭に**を付けることでdictをキーワード引数として展開できる
    # つまり、以下の挙動と同義になる
    # -> task_model.Task(title=task_body.title, done=task_body.done)
    task = task_model.Task(**task_create.dict())
    # DBへ値を追加
    db.add(task)
    # 非同期処理でコミット
    await db.commit()
    # 非同期処理でtaskの情報をDBに登録した値に更新(idが自動採番されるのでそうしてる)
    await db.refresh(task)
    # 作成したDBモデルを戻す
    return task

async def get_tasks_with_done(db: AsyncSession) -> List[Tuple[int, str, bool]]:
    """
    登録したTODOタスク一覧を取得する

    Args:
        db:
            非同期DBセッションインスタンス
    Return:
        (id, title, done)が入ったリスト
    """
    # Resultインスタンスとして、非同期のDB実行処理を定義
    result: Result = await (
        db.execute(
            # select内容を定義
            select(
                task_model.Task.id,
                task_model.Task.title,
                # donesテーブルにはTODOタスクが完了している場合のみレコードが追加される
                # -> isnot(None)の真偽値を'done'というカラムの値として取得
                # https://qiita.com/TamaiHideaki/items/346bf843ee6ee1aa6e93#label
                task_model.Done.id.isnot(None).label('done'),
            ).outerjoin(task_model.Done)
        )
    )
    return result.all()

async def get_task(db: AsyncSession, task_id: int) -> Optional[task_model.Task]:
    """
    登録したTODOタスクの内IDに合致するインスタンスの情報を取得する

    Args:
        db:
            非同期DBセッションインスタンス
        task_id:
            タスクのID
    Return:
        task_model.Taskインスタンス or None
    """
    result: Result = await db.execute(
        # filterを用いてwhere条件での絞り込みを実施
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )
    task: Optional[Tuple[task_model.Task]] = result.first()
    # 要素が1つの場合でもtupleが戻されるので、明示的に最初の要素だけを取得する
    return task[0] if task is not None else None

async def update_task(db: AsyncSession, task_create: task_schema.TaskCreate, original: task_model.Task) -> task_model.Task:
    """
    登録したタスクのタイトルを変更する

    Args:
        db:
            非同期DBセッションインスタンス
        task_create:
            task_schema.TaskCreateのインスタンス
        original:
            task_model.Taskのインスタンス
    Return:
        task_model.Taskインスタンス
    """
    # 受け取ったDBモデルのタイトルをスキーマのタイトルに変更するだけ
    original.title = task_create.title
    db.add(original)
    await db.commit()
    # 非同期処理でoriginalの情報をDBに登録した値に更新
    await db.refresh(original)
    return original
