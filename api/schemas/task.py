from typing import Optional
from pydantic import BaseModel, Field

# FastAPIのスキーマモデルの元となるBaseModelを継承してスキーマを作成する
class Task(BaseModel):
    """
    TODO情報
    """
    # TypeHintとしてintを指定
    id: int
    # Noneを許容する型のOptionalを利用して、値が入らない可能性を明示する
    # 右辺のFieldは(デフォルト値, オプション設定)のようにして利用する
    # -> Field(None, example='xxx') であれば、OpenAPIのExampleの値に'xxx'が設定される
    title: Optional[str] = Field(None, example='クリーニングを取りに行く')
    done: bool = Field(False, description='完了フラグ')
