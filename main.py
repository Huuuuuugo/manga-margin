import cv2 as cv
import numpy as np
from collections import Counter as counter
from makeMargin import cropY, cropX, mkMarginY, mkMarginX
from resizeImage import resizeImg


best_h = 1557
best_w = 1074
x_margin = 62
y_margin = 100
if __name__ == "__main__":
    path = "samples/baloes/"
    page = 1
    # 21, 59
    for i in range(187+0, 249): #232
        print("PAGE: ", i)
        name = f"{str(i).zfill(5)}.jpeg"
        img = cv.imread(f"{path}{name}")
        # cv.imwrite("results/__image.png", img)

        img = resizeImg(img, best_h, best_w)
        # cv.imwrite("results/__resized.png", img)

        crop, mrgn_ttb, mrgn_btt, side = cropY(img)
        resultY = mkMarginY(crop, y_margin, side, mrgn_ttb, mrgn_btt)


        crop1, mrgn_ltr, mrgn_rtl, side = cropX(resultY)
        result = mkMarginX(crop1, page, x_margin, side, mrgn_ltr, mrgn_rtl)

        final_h = best_w+2*y_margin
        final_w = best_h+3*x_margin
        # cv.imwrite("results/__resultPrescale.png", result)

        result = cv.resize(result, (final_h-final_h%5, final_w-final_w%5))

        cv.imwrite(f"results/baloes/{str(i).zfill(5)}.png", result)
        cv.imwrite("results/__result.png", result)
        # cv.imwrite("results/__resultY.png", resultY)
        page = 1 - page
        # input("__main__")