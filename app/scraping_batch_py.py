import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import numpy as np
# import chromedriver_binary
from webdriver_manager.chrome import ChromeDriverManager

def search_mercari(search_word):

    # 検索ワードが複数の場合、「+」で連結するよう整形する
    words = search_word.split(" ")
    search_words = words[0]
    for i in range(1, len(words)):
        search_words = search_words + "+" + words[i]
        
    option = Options()                          # オプションを用意
    option.add_argument('--headless')           # ヘッドレスモードの設定を付与

    # メルカリで検索するためのURL
    url = "https://www.mercari.com/jp/search/?status_trading_sold_out=1&keyword=" + search_words

    # ブラウザを開く
    # この引数にchromedriverのパスを置く
    # デプロイの方法によって書き方は違う
    # https://qiita.com/memakura/items/20a02161fa7e18d8a693 参照
    browser = webdriver.Chrome(ChromeDriverManager().install(),options=option)

    # 起動時に時間がかかるため、5秒スリープ
    time.sleep(5)

    # 表示ページ
    page = 1
    # リストを作成
    columns = ["Name", "Price", "Url"]
    # 配列名を指定する
    df = pd.DataFrame(columns=columns)

    # ブラウザで検索
    browser.get(url)
    # 商品ごとのHTMLを全取得
    posts = browser.find_elements_by_css_selector(".items-box")

    # 商品ごとに名前と値段、購入済みかどうか、URLを取得
    for post in posts[0:9]:
        # 商品名
        title = post.find_element_by_css_selector(
            "h3.items-box-name").text

        # 値段を取得
        price = post.find_element_by_css_selector(
            ".items-box-price").text
        # 余計なものが取得されてしまうので削除
        price = price.replace("¥", "")
        price = price.replace(",", "")

        # 商品のURLを取得
        Url = post.find_element_by_css_selector(
            "a").get_attribute("href")

        # スクレイピングした情報をリストに追加
        se = pd.Series([title, price, Url], columns)
        df = df.append(se, columns)

    # 一応、第3四分位数を取得することに
    df["Price"] = df["Price"].astype(float)
    arr = np.array(df[df['Price'] == df["Price"].quantile(0.75)].iloc[0])
    price_list = [arr[0], int(arr[1])]

    browser.quit()
    
    return price_list[1]


#このsearch_word_listに機械学習から受け渡す
search_word_list=[]
# print(search_mercari('concept building and discussion'))
