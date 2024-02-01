import cv2 as cv
import numbers as np
from collections import Counter as counter


def crop(img):
    img_w = img.shape[1]
    img_h = img.shape[0]
    crop_pos = [img_h, 0]
    markup = img.copy() 

    kernel = cv.getStructuringElement(cv.MORPH_OPEN, (3,3))
    morph = cv.bitwise_not(cv.morphologyEx(cv.bitwise_not(img), cv.MORPH_OPEN, kernel))
    cv.imwrite("__morph.png", morph)

    side = 0
    edges_ttb = []
    edges_btt = []
    for x in range(len(morph[0])):
        if x%5:
            continue
        for y in range(0, len(morph//6)):
            if morph[y][x][0] < 200:
                if y < crop_pos[0]:
                    crop_pos[0] = y
                if y == 0 and side in [0, 2]:
                    print(y)
                    side += 1
                for y in range(y, y+5):
                    markup[y][x-2:x] = [255, 20, 20]
                edges_ttb.append(y)
                break
        for y in reversed(range(5*(len(morph)//6), len(morph)+1)):
            # print(y)
            if morph[y-1][x][0] < 200:
                if y > crop_pos[1]:
                    crop_pos[1] = y
                if y == img_h and side < 2:
                    side += 2
                for y in range(y-5, y):
                    markup[y][x-2:x] = [255, 20, 20]
                edges_btt.append(y)
                break
        
    edges_ttb = counter(edges_ttb).most_common()
    edges_btt = counter(edges_btt).most_common()
    mrgn_ttb = edges_ttb[0][0] - crop_pos[0]
    mrgn_btt = crop_pos[1] - edges_btt[0][0]

    print(mrgn_ttb, mrgn_btt)
    
    # print(edges_ttb, edges_btt)
    print(crop_pos)
    print(edges_ttb[2])
    print(side)
            
    crop = img[crop_pos[0]:crop_pos[1], 0:]
    cv.imwrite("__cropped.png", crop)
    cv.imwrite("__markup.png", markup)
    # print(max(edges_ltr) - min(edges_ltr))
    # print(max(edges_rtl) - min(edges_rtl))
    return crop

path = "samples/esculturas/"
page = 1

for i in range(258, 264): #232
    print("PAGE: ", i)
    name = f"kcc-{str(i).zfill(4)}-kcc.jpg"
    img = cv.imread(f"{path}{name}")
    # img = cv.imread("__cropped.png")
    result = crop(img)
    # cv.imwrite(f"esculturas/{str(i).zfill(5)}.png", result)
    page = 1 - page
    cv.imwrite("__result.png", result)
    cv.imwrite("__image.png", img)
    input()