import pytest
import starlette.status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from api.db import get_db, Base
from api.main import app

# テストDBへ接続するためのURL
# -> sqliteを利用しオンメモリーモードで起動する（非同期で問い合わせ処理を行うため、aiosqliteを利用する）
TEST_DB_URL = URL.create(
    # 非同期読み書きを実施するためaiomysqlアダプターを指定
    drivername='mysql+aiomysql',
    username='root',
    host='db',
    port='3306',
    database='test',
    query={'charset': 'utf8mb4'}
)

# スコープ
# https://qiita.com/_akiyama_/items/9ead227227d669b0564e#%E3%82%B9%E3%82%B3%E3%83%BC%E3%83%97
@pytest.fixture
async def async_client() -> AsyncClient:
    """
    テスト関数の前処理
    """

    # Async用のengineとsessionを作成
    # 非同期1DBインスタンス作成
    async_engine = create_async_engine(TEST_DB_URL, echo=True)
    # 非同期DBセッションインスタンスを作成
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )

    # テスト用のオンメモリSQLiteテーブルを初期化（関数ごとにリセット）
    async with async_engine.begin() as conn:
        # テーブルを全削除
        await conn.run_sync(Base.metadata.drop_all)
        # テーブルを全作成
        await conn.run_sync(Base.metadata.create_all)

    print(TEST_DB_URL)

    # テストDBのセッションを取得する
    async def get_test_db():
        async with async_session() as session:
            # sessionに格納されたデータを都度戻す
            # http://ailaby.com/yield/
            yield session

    # Dependsで利用しているget_db関数の内容をget_test_dbに置き換える
    app.dependency_overrides[get_db] = get_test_db

    # テスト用に非同期HTTPクライアントを返却
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client

    # テストが終わったのちに接続を終了する
    # https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Engine.dispose
    # -> 接続を終了しないと「RuntimeError: Event loop is closed」が発出される
    #    https://stackoverflow.com/questions/40420243/event-loop-is-closed-error-in-aiomysql
    # TODO: 最初セッションを作成するようにして、毎回コネクションを作成しないようにする
    await async_engine.dispose()

# asyncioデコレーターで非同期関数のPytest
@pytest.mark.asyncio
async def test_create_and_read(async_client):
    """
    POSTによるデータ登録、および、Getによるデータ取得のテスト
    """
    # async_clientフィクスチャを利用する事で、HTTPリクエストのタイミングで定義した初期化処理などが走る
    response = await async_client.post('/tasks', json={'title': 'テストタスク'})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj['title'] == 'テストタスク'

    response = await async_client.get('/tasks')
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]['title'] == 'テストタスク'
    assert response_obj[0]['done'] is False

@pytest.mark.asyncio
async def test_done_flag(async_client):
    """
    POSTによるデータ登録、および、Getによるデータ取得のテスト
    """
    # 1. 完了フラグを立てる対象となるTaskインスタンスを登録
    # async_clientフィクスチャを利用する事で、HTTPリクエストのタイミングで定義した初期化処理などが走る
    response = await async_client.post('/tasks', json={'title': 'テストタスク2'})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj['title'] == 'テストタスク2'

    # 完了フラグを立てる
    response = await async_client.put('/tasks/1/done')
    assert response.status_code == starlette.status.HTTP_200_OK

    # 既に完了フラグが立っているので400エラーとなる
    response = await async_client.put('/tasks/1/done')
    assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST

    # 完了フラグを外す
    response = await async_client.delete('/tasks/1/done')
    assert response.status_code == starlette.status.HTTP_200_OK

    # 完了フラグが外れているので404エラーとなる
    response = await async_client.delete('/tasks/1/done')
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
