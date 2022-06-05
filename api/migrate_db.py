from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from api.models.task import Base

DB_URL = URL.create(
    drivername='mysql+pymysql',
    username='root',
    host='db',
    port='3306',
    database='demo',
    query={'charset': 'utf8'}
)

engine = create_engine(DB_URL, echo=True)

def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# このファイルが「直接呼び出された場合のみ」マイグレーションを行う
# つまり、以下のように直接呼び出された場合のみDBマイグレーションを行う
# -> poetry run python -m api.migrate_db
if __name__ == '__main__':
    reset_database()
