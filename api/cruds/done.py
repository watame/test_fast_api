from typing import Tuple, Optional

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio  import AsyncSession

import api.models.task as task_model

async def get_done(db: AsyncSession, task_id: int) -> Optional[task_model.Done]:
    """
    登録したDoneの内IDに合致するインスタンスの情報を取得する

    Args:
        db:
            非同期DBセッションインスタンス
        task_id:
            タスクのID
    Return:
        task_model.Doneインスタンス or None
    """
    result: Result = await db.execute(
        select(task_model.Done).filter(task_model.Done.id == task_id)
    )
    done: Optional[Tuple[task_model.Done]] = result.first()
    # 要素が1つの場合でもtupleが戻されるので、明示的に最初の要素だけを取得する
    return done[0] if done is not None else None

async def create_done(db: AsyncSession, task_id: int) -> task_model.Done:
    """
    新たなDoneをDBに登録する

    Args:
        db:
            非同期DBセッションインスタンス
        task_id:
            doneレコードを追加するtaskのid
    Return:
        task_model.Doneのインスタンス
    """
    done = task_model.Done(id=task_id)
    # DBへ値を追加
    db.add(done)
    # 非同期処理でコミット
    await db.commit()
    # 非同期処理でtaskの情報をDBに登録した値に更新(idが自動採番されるのでそうしてる)
    await db.refresh(done)
    return done

async def delete_done(db: AsyncSession, original: task_model.Done) -> None:
    """
    Doneインスタンスと合致するデータを削除する

    Args:
        db:
            非同期DBセッションインスタンス
        original:
            task_model.Doneのインスタンス
    Return:
        None
    """
    await db.delete(original)
    await db.commit()
