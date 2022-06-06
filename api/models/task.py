from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

# declarative_baseインスタンスを取得する
from api.db import Base

class Task(Base):
    """
    TODOタスクモデル
    """
    __tablename__ = 'tasks'

    id = Column(BigInteger, primary_key=True)
    title = Column(String(1024))

    # Doneテーブル間の関係性を定義し、Doneとしてアクセスできるようにする
    # -> relationship(テーブル名', back_populates=別のテーブルからアクセスされる名前)
    done = relationship('Done', back_populates='task')

class Done(Base):
    """
    完了・未完了モデル（TODOタスクモデルに依存）
    """
    __tablename__ = 'dones'

    id = Column(BigInteger, ForeignKey('tasks.id'), primary_key=True)
    # Taskテーブル間の関係性を定義し、Taskとしてアクセスできるようにする
    # -> relationship(テーブル名', back_populates=別のテーブルからアクセスされる名前)
    task = relationship('Task', back_populates='done')
