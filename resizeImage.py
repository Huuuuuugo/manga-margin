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
    result = img.copy()

    scale_h = best_h - dim_h
    scale_w = best_w - dim_w

    # print("H: ", img_h, dim_h, best_h, scale_h)
    # print("W: ", img_w, dim_w, best_w, scale_w)
    # if scale_h and scale_w:
    #     prop = abs(abs(img_h/best_h)/abs(img_w/best_w))
    #     if prop > 1.1 or prop < 0.9:
    #         pass
    #     print("h/h: ", img_h/best_h)
    #     print("w/w: ", img_w/best_w)
    #     print("dif: ", abs(abs(img_h/best_h)/abs(img_w/best_w)))

    result = cv.resize(img, (img_w, img_h+scale_h)) 
    result = cv.resize(img, (img_w+scale_w, img_h))
    return result