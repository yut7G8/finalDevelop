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

# 画像のアップロード先のディレクトリ
UPLOAD_FOLDER = './uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ファイル容量上限 : 1MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

@app.route('/', methods=['GET'])
def get():
	return render_template('index.html', flag = False)


@app.route('/', methods=['POST'])
def post():
	# ファイルのリクエストパラメータを取得
	f = request.files['file']	
	# ファイル名を取得
	filename = secure_filename(f.filename)
	# ファイルを保存するディレクトリを指定
	filepath = './uploads/' + filename
	# ファイルを保存する
	f.save(filepath)
	
	# 画像から文字列を抽出する
	img = Image.open(filepath)
	extracted_str = extract_string(img)
	# 改行区切りにする
	str_list = extracted_str.split('\n')
	# 余分な文字を削除
	
	# # ファイルを削除する
	# os.remove(filepath)

	return render_template('selection.html', flag = True, image_name = filename, image_url = filepath, str_list = str_list)

@app.route('/selection', methods=['POST'])
def select():
	title_list = request.form.getlist('checkbox')
	# バッチ処理
	price_lists = []
	for i in range(len(title_list)):
		# 2. スクレイピング処理
		price_list = search_mercari(title_list[i])
		price_lists.append(price_list)
	book_dict = { title:price for title,price in zip(title_list,price_lists) }
	return render_template('result.html', book_dict = book_dict)

@app.route('/uploads/<filename>')
# ファイルを表示する
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)