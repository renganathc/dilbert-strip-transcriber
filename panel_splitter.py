import cv2
import numpy as np
from loader import load_strips

def split(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #print(img_gray.shape)
    h, w = img_gray.shape

    empty_lines = []

    for i in range(h):
        whites = 0
        consecutive = 0
        for j in range(w):
            if img_gray[i][j] > 230:
                whites += 1
        if whites/w > 0.998:
            empty_lines.append(i)

    print(empty_lines)

    cv2.imshow("comic strip", img_gray)
    cv2.waitKey(0)

    if 0 in empty_lines:
        print(empty_lines)
        cv2.imshow("efh", img_gray)
        cv2.waitKey(0)
        return True

    return 0


strips = load_strips("dilbert_1989_to_2023")

for strip in strips:
    image = strip["image"]
    if split(image) is True:
        break