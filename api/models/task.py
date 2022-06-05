from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

# declarative_baseインスタンスを取得する
from api.db import Base

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(BigInteger, primary_key=True)
    title = Column(String(1024))

    # Doneテーブル間の関係性を定義し、doneとしてアクセスできるようにする
    # -> relationship(テーブル名', back_populates=別のテーブルからアクセスされる名前)
    done = relationship('Done', back_populates='task')

class Done(Base):
    __tablename__ = 'dones'

    id = Column(BigInteger, ForeignKey('tasks.id'), primary_key=True)
    # Taskテーブル間の関係性を定義し、taskとしてアクセスできるようにする
    # -> relationship(テーブル名', back_populates=別のテーブルからアクセスされる名前)
    task = relationship('Task', back_populates='done')
