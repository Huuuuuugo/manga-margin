import cv2 as cv
import numpy as np
from collections import Counter as counter

#TODO: get best margin size from scanning input images
def cropImgW(img, page, best_margin):
    img_h, img_w, ch = img.shape
    crop_pos = [img_w, 0] 

    kernel = cv.getStructuringElement(cv.MORPH_OPEN, (3,3))
    morph = cv.bitwise_not(cv.morphologyEx(cv.bitwise_not(img), cv.MORPH_OPEN, kernel))
    cv.imwrite("__morph.png", morph)

    get_edge_ltr = []
    get_edge_rtl = []
    edges_ltr = []
    edges_rtl = []
    for y, line in enumerate(morph):
        for x, pixel in enumerate(line):
            if pixel[0] < 200:
                if x <= crop_pos[0]:
                    crop_pos[0] = x
                get_edge_ltr.append(x)
                break
        for i, pixel in enumerate(reversed(line)):
            if pixel[0] < 200:
                x = len(line) - i
                if x > crop_pos[1]:
                    crop_pos[1] = x
                get_edge_rtl.append(x)
                break
        if not (y+1)%10 and len(get_edge_ltr):
            edges_ltr.append(min(get_edge_ltr))
            edges_rtl.append(max(get_edge_rtl))
            get_edge_ltr = []
            get_edge_rtl = []

    crop = img[0:, crop_pos[0]:crop_pos[1]]
    crop_w = crop_pos[1]-crop_pos[0]
    cv.imwrite("__cropped.png", crop)

    edges_ltr = counter(edges_ltr).most_common(5)
    edges_rtl = counter(edges_rtl).most_common(5)
    # print(edges_ltr, '\n', edges_rtl)
    # print(img_w*0.04, img_w*0.2)

    # gets propper sizes for left and right margin
    mrgn_ltr = 0
    mrgn_rtl = 0
    margin = 0
    for mrgn in edges_ltr:
        mrgn_size = mrgn[0]
        if mrgn[1] > 2 and img_w*0.2 > mrgn_size and img_w*0.04 < mrgn_size:
            mrgn_ltr = mrgn_size
            break
    for mrgn in edges_rtl:
        mrgn_size = img_w-mrgn[0]
        if mrgn[1] > 2 and img_w*0.2 > mrgn_size and img_w*0.04 < mrgn_size:
            mrgn_rtl = mrgn_size
            break

    # gets if page is touching left, right or no edge of the page
    side = 0
    if mrgn_ltr > mrgn_rtl:
        for edge in edges_ltr:
            if edge[0] == crop_pos[0] and edge[1] > 2:
                side = 1
    elif mrgn_rtl > mrgn_ltr:
        for edge in edges_rtl:
            if edge[0] == crop_pos[1] and edge[1] > 2:
                side = 2
                
    # apply margin values
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
        result = np.full((img_h, (crop_w+2*best_margin+margin), ch), [255, 255, 255], dtype=np.uint8)
        result[0:, 0+margin:crop_w+margin] = crop
    else:
        print("RTL")
        result = np.full((img_h, (crop_w+2*best_margin+margin), ch), [255, 255, 255], dtype=np.uint8)
        result[0:, best_margin*2:crop_w+best_margin*2] = crop

    return result


def mainA(i, path, page):
    print(i)
    name = f"kcc-{str(i).zfill(4)}-kcc.jpg"
    img = cv.imread(f"{path}{name}")
    result = cropImgW(img, page, 62)
    cv.imwrite(f"esculturas/{str(i).zfill(5)}.png", result)

    return img, result


path = "samples/esculturas/"
page = 1

for i in range(232, 264): #232
    img, result = mainA(i, path, page)
    page = 1 - page
    cv.imwrite("__result.png", result)
    cv.imwrite("__image.png", img)
    input()

