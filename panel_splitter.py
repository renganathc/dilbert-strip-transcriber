import cv2
import numpy as np
from loader import load_strips

def lines_to_spaces(white_lines):
    spaces = []
    if not white_lines:
        return []
    
    space = [white_lines[0], white_lines[0]]
    for i in range(1,len(white_lines)):
        if white_lines[i] == white_lines[i-1] + 1:
            space[1] = white_lines[i]
        else:
            spaces.append(space)
            space = [white_lines[i], white_lines[i]]

    spaces.append(space)
    return spaces

def strip_cropper(spaces, dim_length):
    splits = [0]
    for space in spaces:
        splits.append((space[0] + space[1])//2)
    splits.append(dim_length - 1)
    
    sub_strips = []
    max_dim = max([splits[i] - splits[i-1] for i in range(1, len(splits))])
    for i in range(1, len(splits)):
        if splits[i] - splits[i-1] > 0.3*max_dim:
            sub_strips.append([splits[i-1], splits[i]])

    return sub_strips

def horizontal_splitter(img):
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
        
    blank_regions = lines_to_spaces(white_lines)
    sub_strips = strip_cropper(blank_regions, h)

    return [img[x[0]:x[1],:] for x in sub_strips]

    
def vertical_splitter(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = img_gray.shape
    white_lines = []

    for j in range(w):
        white_pixels = 0
        for i in list(range(3*h//20+1)) + list(range(19*h//20, h)):
            if img_gray[i][j] > 230:
                white_pixels += 1
        if white_pixels/(0.20*h) > 0.98:
            white_lines.append(j)     
    blank_regions = lines_to_spaces(white_lines)
    panels = strip_cropper(blank_regions, w)

    return [img[:,x[0]:x[1]] for x in panels]


def panelizer(strip):
    panels = []
    image = strip["image"]
    sub_strips = horizontal_splitter(image)

    for sub_strip in sub_strips:
        panels = panels + vertical_splitter(sub_strip)
        
    return panels



# strips = load_strips("dilbert_1989_to_2023")

# for strip in strips:
#     print(strip["date"])
#     panels = panelizer(strip)
#     for i in range(len(panels)):
#         cv2.imshow(str(i), panels[i])
#         cv2.waitKey(300)
#     cv2.waitKey(0)