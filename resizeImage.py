import cv2 as cv
import numpy as np
from collections import Counter as counter
from makeMargin import cropY, cropX


def getYMargin(img):
    kernel = np.ones((3,5),np.uint8)
    erode = cv.bitwise_not(cv.erode(cv.bitwise_not(img),kernel,iterations = 1))
    kernel = cv.getStructuringElement(cv.MORPH_OPEN, (4,4))
    morph = cv.bitwise_not(cv.morphologyEx(cv.bitwise_not(erode), cv.MORPH_OPEN, kernel))
    cv.imwrite("results/__erode.png", erode)

    _, ttb, btt, _ = cropY(morph)

    return ttb, btt


def resizeImg(img, best_h, best_w):
    dim_h, dim_w = 0, 0

    crop_imgY, ttb, btt, sideY = cropY(img)
    if not sideY:
        dim_h = crop_imgY.shape[0] - ttb - btt
    elif sideY == 1:
        dim_h = crop_imgY.shape[0] - btt
    elif sideY == 2:
        dim_h = crop_imgY.shape[0] - ttb
    elif sideY == 3:
        dim_h = crop_imgY.shape[0]

    crop_imgX, ltr, rtl, sideX = cropX(img)
    if not sideX:
        dim_w = crop_imgX.shape[1] - ltr - rtl
    elif sideX == 1:
        dim_w = crop_imgX.shape[1] - rtl
    elif sideX == 2:
        dim_w = crop_imgX.shape[1] - ltr
    elif sideX == 3:
        dim_w = crop_imgX.shape[1]

    img_h, img_w, ch = img.shape
    result = img.copy()

    scale_h = best_h - dim_h
    scale_w = best_w - dim_w
    dif_h = best_h/100
    dif_w = best_w/100

    if best_h < 1.25*img_h:
        result = cv.resize(img, (img_w, img_h+scale_h)) 
    if best_w < 1.25*img_w:
        result = cv.resize(img, (img_w+scale_w, img_h))
    return result