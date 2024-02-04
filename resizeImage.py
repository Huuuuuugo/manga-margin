import cv2 as cv
import numpy as np
from collections import Counter as counter
from makeMargin import cropY, cropX


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
    scale_h = best_h - dim_h
    scale_w = best_w - dim_w
    scaled = img.copy()

    if abs(scale_h) < 200:
        scaled = cv.resize(img, (img_w, img_h+scale_h), interpolation=cv.INTER_LINEAR) 
    if abs(scale_w) < 200:
        scaled = cv.resize(img, (img_w+scale_w, img_h), interpolation=cv.INTER_LINEAR)
    # cv.imwrite("results/__scaled.png", scaled)

    return scaled