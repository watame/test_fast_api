FROM python:3.10

# 環境変数の設定
ENV LANG=ja_JP.UTF-8 \
    LC_CTYPE=ja_JP.UTF-8 \
    TZ=Asia/Tokyo

# パッケージのアップデート
RUN apt-get update && \
    apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

# fastApiのインストール
RUN pip install fastapi && \
    pip install uvicorn[standard]
