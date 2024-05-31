# ivx_test

## Usage
```shell
docker compose build
docker compose run --rm app manage.py migrate myapp
docker compose up
```

以下のURLにアクセスする。
http://localhost:8000/

APIのエンドポイントは環境変数`API_URL`で設定する。
APIリクエストにタイムアウトを設定する場合は、環境変数`API_TIMEOUT`で設定する。
