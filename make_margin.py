import cv2 as cv
import numpy as np
from collections import Counter as counter
# from isPageNumber import isntPageNumber

#TODO: create function getMargin() to get best margin size from scanning input images
#TODO: create function to scale cropped images to a consistant value before making margin
#TODO: make mkMarginX() compensate for the difference between common width and width of cropped image
    # create a function to get the common width from scanning input image
def isntPageNumber(img, y, x):
    print(y, x)
    print("__pnum__")
    img_w = img.shape[1]
    if x < img_w//2:
        print("Left")
        if x > 30:
            pnum = img[y-50:y-49, x-30:x+30]
        else:
            pnum = img[y-50:y-49, 0:x+30]
    else:
        print("Right")
        if x < img_w - 30:
            pnum = img[y-50:y-49, x-30:x+30]
        else:
            pnum = img[y-50:y-49, x-30:]
    cv.imwrite("__PageNumber.png", pnum)
    for pixel in pnum[0]:
        if pixel[0] < 200:
            return True
    return False


def cropY(img):
    img_w = img.shape[1]
    img_h = img.shape[0]
    crop_pos = [img_h, 0]
    markup = img.copy() 


    side = 0
    edges_ttb = []
    edges_btt = []
    for x in range(len(img[0])):
        if x%5:
            continue
        for y in range(0, len(img//4)):
            if img[y][x][0] < 80:
                if y < crop_pos[0]:
                    crop_pos[0] = y
                if side in [0, 2] and y == 0:
                    print(y)
                    side += 1
                # for y in range(y, y+5):
                #     markup[y][x-2:x] = [255, 20, 20]
                edges_ttb.append(y)
                break
        for y in reversed(range(3*(len(img)//4), len(img)+1)):
            # print(y)
            if img[y-1][x][0] < 80:
                if y > crop_pos[1]:
                    crop_pos[1] = y
                if side < 2 and y == img_h and isntPageNumber(img, y, x):
                    side += 2
                # for y in range(y-5, y):
                #     markup[y][x-2:x] = [255, 20, 20]
                edges_btt.append(y)
                break
    edges_ttb = counter(edges_ttb).most_common()
    edges_btt = counter(edges_btt).most_common()
    mrgn_ttb = edges_ttb[0][0] - crop_pos[0]
    mrgn_btt = crop_pos[1] - edges_btt[0][0]

    crop = img[crop_pos[0]:crop_pos[1], 0:]
    cv.imwrite("__cropped.png", crop)
    cv.imwrite("__markup.png", markup)
    # print(max(edges_ltr) - min(edges_ltr))
    # print(max(edges_rtl) - min(edges_rtl))
    return crop, mrgn_ttb, mrgn_btt, side


def mkMarginY(crop, best_y_margin, side, mrgn_ttb, mrgn_btt):
    crop_h, crop_w, ch = crop.shape
    #check if the top margin of image touching the top is too small
    # if side in [1, 3] and mrgn_ttb < 0.6*best_y_margin:
    #     if np.count_nonzero(crop[0:10] > 200) > 20000:
    #         side -= 1
       
    # apply margin values
    mrgn_ttb = best_y_margin - mrgn_ttb
    mrgn_btt = best_y_margin - mrgn_btt
    # if mrgn_ttb < 0:
    #     mrgn_ttb = best_y_margin - mrgn_ttb
    # if mrgn_btt < 0:
    #     mrgn_btt = best_y_margin - mrgn_btt
    # # if mrgn_ttb > best_y_margin:
    #     mrgn_ttb = best_y_margin
    # if mrgn_btt > best_y_margin:
    #     mrgn_btt = best_y_margin
    print("mrgn: ", mrgn_ttb, mrgn_btt)
    if not side:
        print("NONE")
        result = np.full((crop_h+mrgn_ttb+mrgn_btt, crop_w, ch), [255, 255, 255], dtype=np.uint8)
        result[mrgn_ttb:crop_h+mrgn_ttb, 0:] = crop
    elif side == 1:
        print("TOP")
        result = np.full((crop_h-mrgn_btt+best_y_margin, crop_w, ch), [255, 255, 255], dtype=np.uint8)
        result[0:crop_h, 0:] = crop
    elif side == 2:
        print("BTM")
        result = np.full((crop_h+mrgn_ttb, crop_w, ch), [255, 255, 255], dtype=np.uint8)
        result[mrgn_ttb:crop_h+mrgn_ttb, 0:] = crop
    else:
        print("BOTH")
        result = crop

    return result


def cropX(img):
    img_w = img.shape[1]
    crop_pos = [img_w, 0]
    markup = img.copy()


    edges_ltr = []
    edges_rtl = []
    side = 0
    for y, line in enumerate(img):
        for x, pixel in enumerate(line[0:len(line)//4]):
            if pixel[0] < 200:
                if x <= crop_pos[0]:
                    crop_pos[0] = x
                if x == 0 and side in [0, 2]:
                    side += 1
                markup[y][x:x+5] = [255, 20, 20]
                edges_ltr.append(x)
                break
        for i, pixel in enumerate(reversed(line[3*(len(line)//4):len(line)])):
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
    # cv.imwrite("__morph.png", morph)
    # cv.imwrite("__cropped.png", crop)
    # cv.imwrite("__markup.png", markup)
    return crop, mrgn_ltr, mrgn_rtl, side


def mkMarginX(crop, page, best_x_margin, side, mrgn_ltr, mrgn_rtl):
    crop_h, crop_w, ch = crop.shape
    # validade 'side' provided by cropX()
    if side in [1, 3] and mrgn_ltr:
        whites = np.count_nonzero(crop[0:, 0:mrgn_ltr] > 200)//mrgn_ltr//3
        for x in range(len(crop[0][0:mrgn_ltr])):
            wt = np.count_nonzero(crop[0:, x:x+1] > 200)//3
            print("wt: ", x, wt)
        print("nonzero: ", crop_h, whites)
        if crop_h - whites < 500:
            side -= 1
    if side in [2, 3] and mrgn_rtl:
        whites = np.count_nonzero(crop[0:, crop_w-mrgn_rtl:] > 250)//mrgn_rtl//3
        if crop_h - whites < 500:
            side -= 2

    # if mrgn_rtl:
    #     print("nonzero: ", crop_h, np.count_nonzero(crop[0:, crop_w-mrgn_rtl:] > 250)//mrgn_rtl//3)
    #     cv.imwrite("__test.png", crop[0:, crop_w-mrgn_rtl:])
    # else:
    #     print("nonzero: ", crop_h, np.count_nonzero(crop[0:, crop_w-1:] > 250)//1//3)
    #     cv.imwrite("__test.png", crop[0:, crop_w-1:])
    # if side in [2, 3] and np.count_nonzero(crop[0:10] > 200) > 20000:
    #     if np.count_nonzero(crop[0:, crop_w-mrgn_rtl:] > 200)//(mrgn_rtl) > 20000:
    #         side -= 1
    # apply margin values
    print("side: ", side)
    print("mrgn: ", mrgn_ltr, mrgn_rtl)
    if best_x_margin > mrgn_ltr:
        mrgn_ltr = best_x_margin - mrgn_ltr
    if best_x_margin > mrgn_rtl:
        mrgn_rtl = best_x_margin - mrgn_rtl
    if not side:
        print("NONE")
        result = np.full((crop_h, (crop_w+best_x_margin+mrgn_ltr+mrgn_rtl), ch), [255, 255, 255], dtype=np.uint8)
        if page:
            result[0:, mrgn_ltr:crop_w+mrgn_ltr] = crop
        else:
            result[0:, best_x_margin+mrgn_ltr:crop_w+best_x_margin+mrgn_ltr] = crop
    elif side == 1:
        print("LTR")
        result = np.full((crop_h, (crop_w+2*best_x_margin), ch), [255, 255, 255], dtype=np.uint8)
        result[0:, 0:crop_w] = crop
    elif side == 2:
        print("RTL")
        result = np.full((crop_h, (crop_w+2*best_x_margin), ch), [255, 255, 255], dtype=np.uint8)
        result[0:, best_x_margin*2:crop_w+best_x_margin*2] = crop
    else:
        print("BOTH")
        result = crop

    print(crop_w, result.shape[1])
    return result


def mainA(i, path, page):
    print(i)
    name = f"kcc-{str(i).zfill(4)}-kcc.jpg"
    img = cv.imread(f"{path}{name}")

    crop, mrgn_ttb, mrgn_btt, side = cropY(img)
    resultY = mkMarginY(crop, 100, side, mrgn_ttb, mrgn_btt)

    crop1, mrgn_ltr, mrgn_rtl, side = cropX(resultY)
    result = mkMarginX(crop1, page, 62, side, mrgn_ltr, mrgn_rtl)
    cv.imwrite(f"esculturas/{str(i).zfill(5)}.png", result)
    return img, result

if __name__ == "__main__":
    path = "samples/esculturas/"
    page = 1

    for i in range(187, 264): #232 264
        img, result = mainA(i, path, page)
        page = 1 - page
        cv.imwrite("__result.png", result)
        cv.imwrite("__image.png", img)
        input()

