import cv2  # OpenCVはcv2という名称で扱われる
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import pyocr
import pyocr.builders


# インストール済みのTesseractのパスを通す
path_tesseract = "C:\\Program Files\\Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract

# OCRエンジンの取得
tools = pyocr.get_available_tools()
tool = tools[0]

# 原稿画像の読み込み
# img_org = Image.open("./img/our_war.jpg")
# img_rgb = img_org.convert("RGB")
# pixels = img_rgb.load()
img = cv2.imread('./img/CBD.jpg')
grayed = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
th, binary = cv2.threshold(grayed, 125, 255, cv2.THRESH_BINARY)
new_img = Image.fromarray(img)
plt.imshow(binary), plt.show()

# ＯＣＲ実行
builder = pyocr.builders.TextBuilder()
result = tool.image_to_string(new_img,  builder=builder)

print(len(result), result)