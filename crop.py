import cv2 as cv
import numpy as np


img = cv.imread("samples/00064.jpeg")
img_h, img_w, ch = img.shape
margin = 25
x0 = img_w
x1 = 0

kernel = cv.getStructuringElement(cv.MORPH_OPEN, (5,5))
morph = cv.bitwise_not(cv.morphologyEx(cv.bitwise_not(img), cv.MORPH_OPEN, kernel))
cv.imwrite("__morph.png", morph)

for y, line in enumerate(morph):
    for x, pixel in enumerate(line):
        if pixel[0] < 200:
            if x <= x0:
                x0 = x
            break
    for i, pixel in enumerate(reversed(line)):
        if pixel[0] < 200:
            x = len(line) - i
            if x > x1:
                x1 = x
            break
crop = img[0:, x0:x1]
crop_w = x1-x0

print(x0, x1)
result = np.full((img_h, (crop_w+2*margin), ch), [255, 255, 255], dtype=np.uint8)

if x0 == 0 and x1 == img_w:
    result = img.copy()
elif x0 == 0:
    result[0:, x0:x1] = crop
elif x1 == img_w:
    result[0:, 2*margin:] = crop
else:
    result[0:, margin:crop_w+margin] = crop

print(img.shape, result.shape)
cv.imwrite("__result.png", result)
cv.imwrite("__cropped.png", crop)
