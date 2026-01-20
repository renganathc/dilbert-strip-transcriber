import cv2
import numpy as np
from pathlib import Path
from PIL import Image

def load_strips(folder_path):
    folder_path = Path(folder_path)

    for sub_dir in folder_path.iterdir():
        year = sub_dir.name
        if not sub_dir.is_dir():
            continue
        for strip in sub_dir.iterdir():
            date = strip.stem[:10]
            name = strip.stem[11:]
            print(name, date)

load_strips("dilbert_1989_to_2023")