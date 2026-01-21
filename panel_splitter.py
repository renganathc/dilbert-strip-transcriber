import cv2
import numpy as np
from loader import load_strips

def split(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #print(img_gray.shape)
    h, w = img_gray.shape

    empty_lines = []
    consecutive = 0

    for i in range(h):
        whites = 0
        for j in range(w):
            if img_gray[i][j] > 220:
                whites += 1
        if whites/w > 0.998:
            if len(empty_lines) > 0 and empty_lines[len(empty_lines) - 1] == i - consecutive - 1 and i != h - 1:
                consecutive += 1
                continue
            
            empty_lines.append(i)
        
        if consecutive != 0:
            empty_lines.append(i)
            consecutive = 0
        
    print(empty_lines)

    #cv2.imshow("comic strip", img_gray)
    #cv2.waitKey(0)


strips = load_strips("dilbert_1989_to_2023")

for strip in strips:
    image = strip["image"]
    split(image)