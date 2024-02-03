import cv2 as cv
import numpy as np
from collections import Counter as counter


def isntPageNumber(img, y, x):
    img_w = img.shape[1]

    if x < img_w//2:
        if x > 30:
            pnum = img[y-50:y-49, x-30:x+30]
        else:
            pnum = img[y-50:y-49, 0:x+30]
    else:
        if x < img_w - 30:
            pnum = img[y-50:y-49, x-30:x+30]
        else:
            pnum = img[y-50:y-49, x-30:]
    # cv.imwrite("results/__PageNumber.png", pnum)
            
    for pixel in pnum[0]:
        if pixel[0] < 200:
            return True
    return False


def cropY(img):
    img_h, img_w = img.shape[0:2]
    crop_pos = [img_h, 0]
    # markup = img.copy()

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
                    side += 1
                # for y in range(y, y+5):
                #     markup[y][x-2:x] = [255, 20, 20]
                edges_ttb.append(y)
                break
        for y in reversed(range(3*(len(img)//4), len(img)+1)):
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
    # cv.imwrite("results/__cropped.png", crop)
    # cv.imwrite("results/__markup.png", markup)

    return crop, mrgn_ttb, mrgn_btt, side


def mkMarginY(crop, best_y_margin, side, mrgn_ttb, mrgn_btt):
    crop_h, crop_w, ch = crop.shape

    # validade 'side' provided by cropY()


    # calculate and apply margin values
    if best_y_margin > mrgn_ttb:
        mrgn_ttb = best_y_margin - mrgn_ttb
    if best_y_margin > mrgn_btt:
        mrgn_btt = best_y_margin - mrgn_btt
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
    # markup = img.copy()

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
                # markup[y][x:x+5] = [255, 20, 20]
                edges_ltr.append(x)
                break
        for i, pixel in enumerate(reversed(line[3*(len(line)//4):len(line)])):
            if pixel[0] < 200:
                x = len(line) - i
                if x > crop_pos[1]:
                    crop_pos[1] = x
                if x == img_w and side < 2:
                    side += 2
                # markup[y][x-5:x] = [255, 20, 20]
                edges_rtl.append(x)
                break
    edges_ltr = counter(edges_ltr).most_common()
    edges_rtl = counter(edges_rtl).most_common()
    mrgn_ltr = edges_ltr[0][0] - crop_pos[0]
    mrgn_rtl = crop_pos[1] - edges_rtl[0][0]

    crop = img[0:, crop_pos[0]:crop_pos[1]]
    # cv.imwrite("results/__cropped.png", crop)
    # cv.imwrite("results/__markup.png", markup)

    return crop, mrgn_ltr, mrgn_rtl, side


def mkMarginX(crop, page, best_x_margin, side, mrgn_ltr, mrgn_rtl):
    crop_h, crop_w, ch = crop.shape

    # validade 'side' provided by cropX()
    if side in [1, 3] and mrgn_ltr:
        have_line = False
        # whites = np.count_nonzero(crop[0:, 0:mrgn_ltr] > 200)//mrgn_ltr//3
        print("mrgn: ", mrgn_ltr)
        print("crop_h: ", crop_h)
        if mrgn_ltr > best_x_margin - 20:
            for y in range(crop_h):
                if crop[y][0][0] < 100:
                    line_check = np.count_nonzero(crop[y-1:y, 0:mrgn_ltr] > 200)//3//2
                    if not line_check:
                        # crop[y-1:y][0:mrgn_ltr] = [50, 50, 255]
                        have_line = True
                        break
            if not have_line:
                print("FAKE LTR (line)")
                side -= 1
        else:
            print("FAKE LTR")
            side -= 1

        # print("nonzero: ", crop_h, whites)
        cv.imwrite("results/__nonzero.png", crop[0:, 0:mrgn_ltr])
        # input("__nonzeroLTR__")

    if side in [2, 3] and mrgn_rtl:
        have_line = False
        # whites = np.count_nonzero(crop[0:, crop_w-mrgn_rtl:] > 250)//mrgn_rtl//3
        print("mrgn: ", mrgn_rtl)
        print("crop_h: ", crop_h)
        if mrgn_rtl > best_x_margin - 20:
            for y in range(crop_h):
                if crop[y][crop_w-1][0] < 100:
                    line_check = np.count_nonzero(crop[y-1:y, crop_w-mrgn_rtl:])//3//2
                    if not line_check:
                        # crop[y-1:y][crop_w-1-mrgn_rtl:0] = [50, 50, 255]
                        have_line = True
                        break
            if not have_line:
                print("FAKE RTL (line)")
                side -= 2
        else:
            print("FAKE RTL")
            side -= 2


        # print("nonzero: ", crop_h, whites)
        cv.imwrite("results/__nonzero.png", crop[0:, crop_w-mrgn_rtl:])
        # input("__nonzeroRTL__")

    # calculate and apply margin values
    if best_x_margin > mrgn_ltr:
        mrgn_ltr = best_x_margin - mrgn_ltr
    else:
        mrgn_ltr -= best_x_margin
    if best_x_margin > mrgn_rtl:
        mrgn_rtl = best_x_margin - mrgn_rtl
    else:
        mrgn_rtl -= best_x_margin
    print(mrgn_ltr, mrgn_rtl)
    if not side:
        print("NONE")
        result = np.full((crop_h, (crop_w+best_x_margin+mrgn_ltr+mrgn_rtl), ch), [255, 255, 255], dtype=np.uint8)
        if page:
            result[0:, mrgn_ltr:crop_w+mrgn_ltr] = crop
        else:
            result[0:, best_x_margin+mrgn_ltr:crop_w+best_x_margin+mrgn_ltr] = crop
    elif side == 1:
        print("LTR")
        result = np.full((crop_h, (crop_w+best_x_margin+mrgn_rtl), ch), [255, 255, 255], dtype=np.uint8)
        result[0:, 0:crop_w] = crop
    elif side == 2:
        print("RTL")
        result = np.full((crop_h, (crop_w+best_x_margin+mrgn_ltr), ch), [255, 255, 255], dtype=np.uint8)
        result[0:, best_x_margin+mrgn_ltr:crop_w+best_x_margin+mrgn_ltr] = crop
    else:
        print("BOTH")
        result = crop

    return result