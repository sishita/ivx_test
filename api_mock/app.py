import random
import re
import time

from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=['POST'])
def index():
    """
    特定の画像ファイルへのPathを与えると、AIで分析し、その画像が所属するClassを返却するAPIのモック

    パラメータimage_pathに一定のパターンを含めることで、レスポンスを変更できる。
    1. http_XXX -> HTTPのステータスコードXXXを返す。
       例) /sample/http_500/test.jpg -> ステータスコード500を返す。
    2. error_XXX -> エラーコードXXXを返す。
       例) /sample/error_E123/test.jpg -> リクエスト失敗レスポンスを返し、メッセージは「Error:E123」となる。
    3. sleep_XXX -> XXX秒間スリープする。
       例) /sample/sleep_30/test.jpg -> 30秒間スリープしたあと、リクエスト成功を返す。
    """
    try:
        image_path = request.form['image_path']
    except KeyError:
        return 'image_path is empty', 400

    m = re.search('http_(\\d{3})', image_path)
    if m is not None:
        return 'Error', int(m.group(1))

    m = re.search('error_(\\w+)', image_path)
    if m is not None:
        return failure_response(m.group(1))

    m = re.search('sleep_(\\d+)', image_path)
    if m is not None:
        sleep_seconds = int(m.group(1))
        print('Sleep {} seconds.'.format(sleep_seconds))
        time.sleep(sleep_seconds)

    return success_response(random.randint(-2 ** 31, 2 ** 31 - 1), random.uniform(0, 1))


def success_response(clazz: int, confidence: float) -> dict:
    return {
        'success': True,
        'message': 'success',
        'estimated_data': {
            'class': clazz,
            'confidence': confidence,
        }
    }


def failure_response(error_code: str) -> dict:
    return {
        'success': False,
        'message': 'Error:' + error_code,
        'estimated_data': {},
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
