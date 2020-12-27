# 本の価格相場予測アプリ
開発期間8月1日~9月19日

**[HAIT_Lab_Primaryコース](https://hait-lab.com/)修了案件**

**[HAIT_Lab_Primaryコース](https://hait-lab.com/)4期 Gチームメンバー**

yut7G8, leouch37, shinnosuke-matsuo

## 開発背景
本処分の手段として、フリマアプリで売ることは主流になりつつあり、そのような場合、毎度Amazonやメルカリで適正価格を調べなければならない。

その際、出品数が多量だと手間がかかる。

## 課題に対する技術的解決策
1. **OCR(Optional Character Recognition/Reader, 光学文字認識)**

画像中の文字を検出し、文字データに変換する技術

今回は**Tesseract OCR**(Googleが公開したオープンソースの文字認識エンジン)を使用

インストール方法は[ここから](https://gammasoft.jp/blog/tesseract-ocr-install-on-windows/)

2. **メルカリをスクレイピング**

検索ワードを渡せば、書籍名・値段・URLのリストが作成されるようにする。

各検索ワードに対する売却済み商品上位9件の価格を抽出し、それらの第1四分位数を取得。

3. **フロントとバックエンドの連携**

画像、文字列一覧、選択したタイトル、値段とお互いでやり取りするものが多かったのでリストや辞書型を駆使。
