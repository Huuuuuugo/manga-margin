import cv2 as cv
import numpy as np
from collections import Counter as counter
from make_margin import cropY, cropX, mkMarginY, mkMarginX
from isPageNumber import isntPageNumber


def getDim(img):
    h, w = 0, 0

    crop_imgY, ttb, btt, sideY = cropY(img)
    if not sideY:
        h = crop_imgY.shape[0] - ttb - btt
    elif sideY == 1:
        h = crop_imgY.shape[0] - btt
    elif sideY == 2:
        h = crop_imgY.shape[0] - ttb
    elif sideY == 3:
        h = crop_imgY.shape[0]

    crop_imgX, ltr, rtl, sideX = cropX(img)
    if not sideX:
        w = crop_imgX.shape[1] - ltr - rtl
    elif sideX == 1:
        w = crop_imgX.shape[1] - rtl
    elif sideX == 2:
        w = crop_imgX.shape[1] - ltr
    elif sideX == 3:
        w = crop_imgX.shape[1]


    return h, w

def getYMargin(img):
    kernel = np.ones((3,5),np.uint8)
    erode = cv.bitwise_not(cv.erode(cv.bitwise_not(img),kernel,iterations = 1))
    kernel = cv.getStructuringElement(cv.MORPH_OPEN, (4,4))
    morph = cv.bitwise_not(cv.morphologyEx(cv.bitwise_not(erode), cv.MORPH_OPEN, kernel))
    cv.imwrite("__erode.png", erode)

    crop_imgY, ttb, btt, sideY = cropY(morph)

    return ttb, btt


def resizeImg(img, best_h, best_w, dim_h, dim_w):
    img_h, img_w, ch = img.shape
    result = img.copy()

    scale_h = best_h - dim_h
    scale_w = best_w - dim_w
    dif_h = best_h/100
    dif_w = best_w/100

    # if abs(scale_h) > dif_h and abs(scale_w) > dif_w:
    if best_h < 1.25*img_h: #15.57 #3.72    #10.74 #2.08
        print("H: ", scale_h, img_h)
        result = cv.resize(img, (img_w, img_h+scale_h)) 
# else:
    if best_w < 1.25*img_w:
        print("W: ", scale_w, img_w)
        result = cv.resize(img, (img_w+scale_w, img_h))
    # result = cv.resize(img, (img_w - img_w%5, img_h - img_h%5))
    print("shape: ", img.shape, result.shape)
    return result

best_h = 1557
best_w = 1074
x_margin = 62
y_margin = 100
if __name__ == "__main__":
    path = "samples/baloes/"
    page = 1
    # 21, 59
    for i in range(231, 249): #232
        print("PAGE: ", i)
        name = f"{str(i).zfill(5)}.jpeg"
        img = cv.imread(f"{path}{name}")

        dim_h, dim_w = getDim(img)
        img = resizeImg(img, best_h, best_w, dim_h, dim_w)

        crop, mrgn_ttb, mrgn_btt, side = cropY(img)
        resultY = mkMarginY(crop, y_margin, side, mrgn_ttb, mrgn_btt)
        mrgn_ttb, mrgn_btt = getYMargin(img)

        crop1, mrgn_ltr, mrgn_rtl, side = cropX(resultY)
        result = mkMarginX(crop1, page, x_margin, side, mrgn_ltr, mrgn_rtl)

        final_h = best_w+2*y_margin
        final_w = best_h+3*x_margin
        result = cv.resize(result, (final_h-final_h%5, final_w-final_w%5))

        cv.imwrite(f"baloes/{str(i).zfill(5)}.png", result)
        cv.imwrite("__image.png", img)
        cv.imwrite("__result.png", result)
        cv.imwrite("__resultY.png", resultY)
        page = 1 - page
        # input()