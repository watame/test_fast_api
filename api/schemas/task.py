from typing import Optional
from pydantic import BaseModel, Field

# FastAPIのスキーマモデルの元となるBaseModelを継承してスキーマを作成する
class TaskBase(BaseModel):
    """
    TODO基底スキーマ
    共通で利用するフィールド定義を設定し、個別のTODOスキーマはこのクラスを継承して定義する
    """
    # Noneを許容する型のOptionalを利用して、値が入らない可能性を明示する
    # 右辺のFieldは(デフォルト値, オプション設定)のようにして利用する
    # -> Field(None, example='xxx') であれば、OpenAPIのExampleの値に'xxx'が設定される
    title: Optional[str] = Field(None, example='クリーニングを取りに行く')

class TaskCreate(TaskBase):
    """
    TODO作成スキーマ
    """
    # 作成時は「IDは自動採番」「完了フラグも作成時は常にFalse」なので明示的に定義せず、継承した情報のみを利用する
    pass

class TaskCreateResponse(TaskCreate):
    """
    TODO作成リクエストのレスポンススキーマ
    """
    id: int

    # DB接続の際に利用するクラス
    class Config:
        # 暗黙的にORMを受け取ってレスポンススキーマに変換する事を意味する
        # -> task_model.Taskの各フィールドを使って初期化してくれる
        orm_mode = True


class Task(TaskBase):
    """
    TODO詳細スキーマ
    """
    # TypeHintとしてintを指定
    id: int
    done: bool = Field(False, description='完了フラグ')

    # DB接続の際に利用するクラス
    class Config:
        orm_mode = True
