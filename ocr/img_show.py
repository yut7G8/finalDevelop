import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image 

#OpenCVまたはPILで読み込み
CV_im = cv2.imread("./img/lena.png")
PIL_im= np.array(Image.open("./img/lena.png"))

#BGRからRGBへ変換
CV_im_RGB = CV_im[:, :, ::-1].copy()

#変換
PIL2CV=np.asarray(PIL_im)
CV2PIL=Image.fromarray(CV_im)
CV2PIL_normalize=Image.fromarray(CV_im_RGB)

#描画
plt.subplot(1, 3, 1), plt.imshow(PIL2CV)
plt.title(u"PIL⇒CV")
plt.subplot(1, 3, 2), plt.imshow(CV2PIL)
plt.title(u"CV(BGR)⇒PIL")
plt.subplot(1, 3, 3), plt.imshow(CV2PIL_normalize)
plt.title(u"CV(RGB⇒PIL")
plt.show()

# ----------------------------------

img = cv2.imread('./img/our_war.jpg')
plt.subplot(2, 2, 1), plt.imshow(img)
plt.title("our_war")
print(img.shape)

grayed = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
plt.subplot(2, 2, 2), plt.imshow(grayed)
plt.title("our_war_grayed")
print(grayed.shape)

th, binary = cv2.threshold(grayed, 125, 255, cv2.THRESH_BINARY)
plt.subplot(2, 2, 3), plt.imshow(binary)
plt.title("our_war_binary")
print(binary.shape)

plt.show()