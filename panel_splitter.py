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

def horizontal_split(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = img_gray.shape
    white_lines = []

    for i in range(h):
        white_pixels = 0
        for j in range(w):
            if img_gray[i][j] > 220:
                white_pixels += 1
        if white_pixels/w > 0.997:
            white_lines.append(i)
        
    print("blank regions (horizontal): ", line_to_region(white_lines))
    return line_to_region(white_lines)
    
def vertical_split(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = img_gray.shape
    white_lines = []

    for j in range(w):
        white_pixels = 0
        for i in list(range(3*h//20)) + list(range(19*h//20, h)):
            if img_gray[i][j] > 230:
                white_pixels += 1
        if white_pixels/(0.20*h) > 0.99:
            white_lines.append(j)
        
    print("blank regions (vertical): ", line_to_region(white_lines))
    return line_to_region(white_lines)


strips = load_strips("dilbert_1989_to_2023")

for strip in strips:
    image = strip["image"]
    horizontal_split(image)
    vertical_split(image)
    cv2.imshow("comic strip", image)
    cv2.waitKey(0)
    # press any key to iterate through the imaegs and see blan k regions