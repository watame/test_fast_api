FROM --platform=linux/x86_64 mysql:8.0

# 初期設定SQLのコピー
# /docker-entrypoint-initdb.d にSQLを格納することで最初に行いたいSQLを設定できる
# https://stackoverflow.com/questions/43322033/create-database-on-docker-compose-startup
COPY container/mysql/init.sql /docker-entrypoint-initdb.d
