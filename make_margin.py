import cv2 as cv
import numpy as np
from collections import Counter as counter

#TODO: create function getMargin() to get best margin size from scanning input images
#TODO: make mkMarginX() compensate for the difference between common width and width of cropped image
    # create a function to get the common width from scanning input image
#TODO: create mkMarginY(), a variation of mkMarginX() which iterates trhough the Y axis
#TODO: separate mkMarginY() into mkMarginY() and cropY()
def cropX(img):
    img_w = img.shape[1]
    crop_pos = [img_w, 0]
    markup = img.copy()

    kernel = cv.getStructuringElement(cv.MORPH_OPEN, (3,3))
    morph = cv.bitwise_not(cv.morphologyEx(cv.bitwise_not(img), cv.MORPH_OPEN, kernel))

    edges_ltr = []
    edges_rtl = []
    side = 0
    for y, line in enumerate(morph):
        for x, pixel in enumerate(line[0:len(line)//4]):
            if pixel[0] < 200:
                if x <= crop_pos[0]:
                    crop_pos[0] = x
                if x == 0 and side < 1:
                    side += 1
                markup[y][x:x+5] = [255, 20, 20]
                edges_ltr.append(x)
                break
        for i, pixel in enumerate(reversed(line[len(line)//4:len(line)])):
            if pixel[0] < 200:
                x = len(line) - i
                if x > crop_pos[1]:
                    crop_pos[1] = x
                if x == img_w and side < 2:
                    side += 2
                markup[y][x-5:x] = [255, 20, 20]
                edges_rtl.append(x)
                break

    crop = img[0:, crop_pos[0]:crop_pos[1]]

    edges_ltr = counter(edges_ltr).most_common()
    edges_rtl = counter(edges_rtl).most_common()
    mrgn_ltr = edges_ltr[0][0] - crop_pos[0]
    mrgn_rtl = crop_pos[1] - edges_rtl[0][0]
    # print(side)
    cv.imwrite("__morph.png", morph)
    cv.imwrite("__cropped.png", crop)
    cv.imwrite("__markup.png", markup)
    return crop, mrgn_ltr, mrgn_rtl, side


def mkMarginX(crop, page, best_margin, side, mrgn_ltr, mrgn_rtl, original_shape):
    img_h, img_w, ch = original_shape
    crop_w = crop.shape[1]
       
    # apply margin values
    print(mrgn_ltr, mrgn_rtl)
    mrgn_ltr = best_margin - mrgn_ltr
    mrgn_rtl = best_margin - mrgn_rtl
    if not side:
        print("NONE")
        result = np.full((img_h, (crop_w+best_margin+mrgn_ltr+mrgn_rtl), ch), [255, 255, 255], dtype=np.uint8)
        if page:
            result[0:, mrgn_ltr:crop_w+mrgn_ltr] = crop
        else:
            result[0:, best_margin+mrgn_ltr:crop_w+best_margin+mrgn_ltr] = crop
    elif side == 1:
        print("LTR")
        result = np.full((img_h, (crop_w+2*best_margin), ch), [255, 255, 255], dtype=np.uint8)
        result[0:, 0:crop_w] = crop
    elif side == 2:
        print("RTL")
        result = np.full((img_h, (crop_w+2*best_margin), ch), [255, 255, 255], dtype=np.uint8)
        result[0:, best_margin*2:crop_w+best_margin*2] = crop
    else:
        result = crop

    print(img_w, result.shape[1])
    return result


def mainA(i, path, page):
    print(i)
    name = f"kcc-{str(i).zfill(4)}-kcc.jpg"
    img = cv.imread(f"{path}{name}")
    crop, mrgn_ltr, mrgn_rtl, side = cropX(img)
    result = mkMarginX(crop, page, 62, side, mrgn_ltr, mrgn_rtl, img.shape)
    cv.imwrite(f"esculturas/{str(i).zfill(5)}.png", result)
    return img, result


path = "samples/esculturas/"
page = 1

for i in range(256, 264): #232 264
    img, result = mainA(i, path, page)
    page = 1 - page
    cv.imwrite("__result.png", result)
    cv.imwrite("__image.png", img)
    input()

