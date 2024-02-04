import shutil
import os
import cv2 as cv
import numpy as np
from collections import Counter as counter
from makeMargin import cropY, cropX, mkMarginY, mkMarginX
from resizeImage import resizeImg


#get info
root_path = input("Path: ").replace('\\', '/').replace('\"', '')
dir_folders = os.listdir(root_path)
try:
    dir_folders.pop(dir_folders.index("__Início"))
except ValueError:
    pass
try:
    dir_folders.pop(dir_folders.index("Fim"))
except ValueError:
    pass

prefix = input("File name prefix: ")
zfill_size = int(input("File name zero fill: "))
sufix = input("File name sufix: ")


# set preferences
skip_pages = input("Skip pages: ").split()
for i, element in enumerate(skip_pages):
    skip_pages[i] = int(element)
skip_chapters = input("Skip chapters: ").split()
for i, element in enumerate(skip_chapters):
    skip_chapters[i] = int(element)


# create temp folder
try:
    os.mkdir("./temp")
except FileExistsError:
    pass


best_h = 1557
best_w = 1074
x_margin = 62
y_margin = 100
final_h = best_h+2*y_margin
final_w = best_w+3*x_margin

for i, dir in enumerate(dir_folders):
    if (i+1 in skip_chapters):
        continue

    print(f"Ch. {i+1}/{len(dir_folders)}")
    path = f"{root_path}/{dir}"
    page_counter = int(os.listdir(path)[0][len(prefix):len(prefix)+zfill_size])
    last_page = int(os.listdir(path)[-1][len(prefix):len(prefix)+zfill_size])
    pages = last_page - page_counter + 1
    page_type = 1

    for page in range(pages):
        img_name = f"{prefix}{str(page_counter).zfill(zfill_size)}{sufix}"
        img_path = f"{path}/{img_name}"
        temp_img_path = f"./temp/{img_name}"

        if page_counter in skip_pages:
            page_type = 1 - page_type #change page type after skip, might be better to comment this out when skipping double page sized images
            page_counter += 1
            continue

        # <main>
        # read image
        shutil.copy(img_path, "./temp")
        img = cv.imread(temp_img_path)
        # cv.imwrite("results/__image.png", img)


        # check if img is a double page image
        img_h, img_w, ch = img.shape
        if img_w/img_h > img_h/img_w and img_w > final_w:
            #TODO: scale result to appropriate multiple of 5 before saving
            result = img.copy()
            cv.imwrite(f"results/baloes/{str(i).zfill(5)}.png", result)
            if not page_type:
                page_type = 1 - page_type
            # input("__main__")
            continue


        # creating margins
        img = resizeImg(img, best_h, best_w)

        crop, mrgn_ttb, mrgn_btt, side = cropY(img)
        resultY = mkMarginY(crop, y_margin, side, mrgn_ttb, mrgn_btt)

        crop1, mrgn_ltr, mrgn_rtl, side = cropX(resultY)
        result = mkMarginX(crop1, page_type, x_margin, side, mrgn_ltr, mrgn_rtl)


        # check if result is too small on height or width, if so, fill the missing space with white pixels
        res_h, res_w, ch = result.shape
        if res_h < best_h:
            print("Filled H")
            fill = np.full((final_h, res_w, ch), [255, 255, 255], dtype=np.uint8)
            fill[0:res_h, 0:res_w] = result
            result = fill.copy()
            # cv.imwrite("results/__fillH.png", result)
        if res_w < best_w:
            print("Filled W")
            res_h, res_w, ch = result.shape
            fill = np.full((res_h, final_w, ch), [255, 255, 255], dtype=np.uint8)
            fill[0:res_h, 0:res_w] = result
            result = fill.copy()
            # cv.imwrite("results/__fillW.png", result)


        # resize to the same size as the other pages 
        result = cv.resize(result, (final_w-final_w%5, final_h-final_h%5), interpolation=cv.INTER_CUBIC)


        # save to source
            # remember to copy this to the exception for double pages
            # save result to temp
            # copy from temp to source
            # remove from temp
        cv.imwrite(temp_img_path, result)
        shutil.copy(temp_img_path, path)
        os.remove(temp_img_path)

        page_type = 1 - page_type
        print(f"{page + 1}/{pages}")
        page_counter += 1
        # input("__main__")
        # <\main>


shutil.rmtree("./temp")