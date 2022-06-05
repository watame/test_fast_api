from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine.url import URL

# sqlalchemyのURLジェネレーターを利用し、安全なURLパスを作成
# https://qiita.com/takkeybook/items/e34afdba936f2062590e
ASYNC_DB_URL = URL.create(
    drivername='mysql+aiomysql',
    username='root',
    host='db',
    port='3306',
    database='demo',
    query={'charset': 'utf8'}
)
#ASYNC_DB_URL = 'mysql+aiomysql://root@db:3306/demo?charset=utf8'

print(ASYNC_DB_URL)
# DB接続先を引数にDBインスタンスを作成
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
# DBトランザクションを管理するSessionインスタンスを作成
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session
