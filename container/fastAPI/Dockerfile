FROM python:3.10

# DockerのWorkdirを引数として取得
ARG SOURCE_DIR

# 環境変数の設定
ENV LANG=ja_JP.UTF-8 \
    LC_CTYPE=ja_JP.UTF-8 \
    TZ=Asia/Tokyo

# パッケージのアップデートと不要なパッケージの削除
RUN apt-get update && \
    apt-get clean all && \
    rm -rf /var/cache/apt

# 作業ディレクトリを設定
WORKDIR ${SOURCE_DIR}

# 起動時に実施する処理を定義したntrypoint.shをコピーして実行
COPY container/fastAPI/entrypoint.sh /usr/bin/
# 実行権限を付与
RUN chmod +x /usr/bin/entrypoint.sh
# エントリーポイントの処理を実行
ENTRYPOINT [ "entrypoint.sh" ]
