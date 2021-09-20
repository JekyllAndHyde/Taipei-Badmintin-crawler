import numpy as np
import mnist
import cv2
import cnn
from Conv import Conv3x3
from maxpool import MaxPool2
from softmax import Softmax
import pytesseract as pt
from PIL import Image

def pre(img):
    # binary
    threshold = 130
    h, w = img.shape
    for i in range(h):
        for j in range(w):
            if img[i, j] < threshold:
                img[i, j] = 255
            else:
                img[i, j] = 0

    # 降噪
    for i in range(1, h-1):
        for j in range(1, w-1):
            cnt = 0
            if img[i, j-1] > 245:
                cnt = cnt+1
            if img[i, j+1] > 245:
                cnt = cnt+1
            if img[i-1, j] > 245:
                cnt = cnt+1
            if img[i+1, j] > 245:
                cnt = cnt+1
            if img[i-1, j-1] > 245:
                cnt = cnt+1
            if img[i+1, j-1] > 245:
                cnt = cnt+1
            if img[i-1, j+1] > 245:
                cnt = cnt+1
            if img[i+1, j+1] > 245:
                cnt = cnt+1

            if cnt > 5:
                img[i, j] = 255

    return img

def inverse(img):
    h, w = img.shape
    for i in range(h):
        for j in range(w):
            if img[i, j] > 245:
                img[i, j] = 0
            else:
                img[i, j] = 255

    return img
def get_predict(img):
    """
    img = cv2.GaussianBlur(img, (5, 5), 1.5)
    img = pre(img)
    img = inverse(img)

    # cv2.imshow("img", cv2.resize(img[5:33, 5:28], (28, 28)))
    # cv2.imshow("img", cv2.resize(img[5:33, 24:40], (28, 28)))
    # cv2.imshow("img", cv2.resize(img[5:33, 37:52], (28, 28)))
    # cv2.imshow("img", cv2.resize(img[5:33, 52:67], (28, 28)))
    # cv2.imshow("img", cv2.resize(img[5:33, 67:82], (28, 28)))
    """
    test_message = Image.fromarray(img)
    text = pt.image_to_string(test_message)
    return text
    """
    out, loss, acc = cnn.forward(cv2.resize(img[5:33, 5:28], (28, 28)), 6)
    print(acc)
    out, loss, acc = cnn.forward(cv2.resize(img[5:33, 24:40], (28, 28)), 7)
    print(acc)
    out, loss, acc = cnn.forward(cv2.resize(img[5:33, 37:52], (28, 28)), 2)
    print(acc)
    out, loss, acc = cnn.forward(cv2.resize(img[5:33, 52:67], (28, 28)), 4)
    print(acc)
    out, loss, acc = cnn.forward(cv2.resize(img[5:33, 67:82], (28, 28)), 4)
    print(acc)
    cv2.waitKey(0)
    """
"""
# The mnist package handles the MNIST dataset for us!
train_images = mnist.train_images()[:2000]
train_labels = mnist.train_labels()[:2000]
print(train_labels[0])
for i in range(2000):
    train_images[i] = pre(train_images[i])
conv = Conv3x3(8)
pool = MaxPool2()
softmax = Softmax(13 * 13 * 8, 10)
cnn.cnn(train_images, train_labels)

get_predict(cv2.imread("valid.PNG", cv2.IMREAD_GRAYSCALE))
"""
# pt.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# img = cv2.imread('valid.PNG', cv2.IMREAD_GRAYSCALE)
# get_predict(img)
