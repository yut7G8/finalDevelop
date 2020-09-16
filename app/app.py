# 参考：https://qiita.com/keimoriyama/items/7c935c91e95d857714fb

import os
# request フォームから送信した情報を扱うためのモジュール
# redirect  ページの移動
# url_for アドレス遷移
# send_from_directory 画像のダウンロード
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
# ファイル名をチェックする関数
from werkzeug.utils import secure_filename
# 画像のダウンロード
from flask import send_from_directory
from scraping_batch_py import search_mercari
from pyocr_filter import extract_string
from PIL import Image


app = Flask(__name__)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # ファイルを受け取る方法の指定
# @app.route('/', methods=['GET', 'POST'])
# def uploads_file():
#     # リクエストがポストかどうかの判別
#     if request.method == 'POST':
#         # ファイルがなかった場合の処理
#         if 'file' not in request.files:
#             flash('ファイルがありません')
#             return redirect(request.url)
#         # データの取り出し
#         file = request.files['file']
#         # ファイル名がなかった時の処理
#         if file.filename == '':
#             flash('ファイルがありません')
#             return redirect(request.url)
#         # ファイルのチェック
#         if file and allwed_file(file.filename):
#             # 危険な文字を削除（サニタイズ処理）
#             filename = secure_filename(file.filename)
#             # ファイルの保存
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             # アップロード後のページに転送
#             return redirect(url_for('uploaded_file', filename=filename))
#     elif request.method == 'GET':
#         return render_template('index.html')


# # アップロードされたファイルの処理
# @app.route('/uploads/<filename>')
# # ファイルを表示する
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# 画像のアップロード先のディレクトリ
UPLOAD_FOLDER = './uploads/'
# ファイル容量上限 : 1MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

@app.route('/', methods=['GET'])
def get():
	return render_template('index.html', flag = False)


@app.route('/', methods=['POST'])
def post():	
	title_list = request.form.getlist('checkbox')
	if title_list:
		# バッチ処理
		price_lists = []
		for i in range(len(title_list)):
			# 2. スクレイピング処理
			price_list = search_mercari(title_list[i])
			price_lists.append(price_list)
		return render_template('result.html', price_lists=price_lists)

	else:
		# ファイルのリクエストパラメータを取得
		f = request.files.get('file')	
		# ファイル名を取得
		filename = secure_filename(f.filename)
		# ファイルを保存するディレクトリを指定
		filepath = './uploads/' + filename
		# ファイルを保存する
		f.save(filepath)
		# 画像から文字列を抽出する
		img = Image.open(filepath)
		extracted_str = extract_string(img)
		str_list = extract_string.split()
		# ファイルを削除する
		os.remove(filepath)

		return render_template('index.html', flag = True, image_name = filename, image_url = filepath, str_list = str_list)


if __name__ == "__main__":
    app.run()