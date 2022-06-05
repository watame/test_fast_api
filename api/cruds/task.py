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
