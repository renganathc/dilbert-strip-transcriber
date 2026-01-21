import cv2
import numpy as np
from loader import load_strips

def line_to_region(white_lines):
    regions = []
    if not white_lines:
        return []
    
    region = [white_lines[0], white_lines[0]]
    for i in range(1,len(white_lines)):
        if white_lines[i] == white_lines[i-1] + 1:
            region[1] = white_lines[i]
        else:
            regions.append(region)
            region = [white_lines[i], white_lines[i]]

    regions.append(region)
    return regions

def split(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = img_gray.shape

    white_lines = []

    for i in range(h):
        white_pixels = 0
        for j in range(w):
            if img_gray[i][j] > 220:
                white_pixels += 1
        if white_pixels/w > 0.998:
            white_lines.append(i)
        
    print("blank regions: ", line_to_region(white_lines))

    cv2.imshow("comic strip", img_gray)
    cv2.waitKey(0)


strips = load_strips("dilbert_1989_to_2023")

for strip in strips:
    image = strip["image"]
    split(image)
    # press any key to iterate through the imaegs and see blan k regions