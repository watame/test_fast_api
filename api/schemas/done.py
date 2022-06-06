from pydantic import BaseModel


class DoneResponse(BaseModel):
    """
    Doneスキーマ
    """
    id: int

    # DB接続の際に利用するクラス
    class Config:
        # 暗黙的にORMを受け取ってレスポンススキーマに変換する事を意味する
        # -> task_model.Taskの各フィールドを使って初期化してくれる
        orm_mode = True
