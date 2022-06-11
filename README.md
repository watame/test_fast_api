# このレポジトリの目的
1. FastAPIの機能をざっくり理解する
2. FastAPIで把握するべきPythonの構文を把握する
3. FastAPIのハマりそうなところを説明できるレベルまで理解する
4. FastAPIをDockerコンテナ上で動作させる

# 初期設定
1. Dockerイメージの作成
    - `docker-compose build`
2. Dockerイメージの起動
    - `docker-compose build`
3. DBマイグレーション
    - `docker-compose exec app poetry run python -m api.migrate_db`

# APIドキュメント
- `localhost:8000/docs`

# テスト
- `docker-compose run --entrypoint "poetry run pytest" app`

# 参考にするサイト
- [FastAPI入門](https://zenn.dev/sh0nk/books/537bb028709ab9/viewer/f1b6fc)
