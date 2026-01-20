import cv2
import numpy as np
from pathlib import Path
from PIL import Image

def load_image(path):
    pillow_img = Image.open(path).convert("RGB")
    np_img = np.array(pillow_img)
    cv_bgr_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
    return cv_bgr_img

def load_strips(folder_path):
    folder_path = Path(folder_path)

    for sub_dir in sorted(folder_path.iterdir()):
        if not sub_dir.is_dir():
            continue
        for strip in sorted(sub_dir.iterdir()):
            date = strip.stem[:10]
            name = strip.stem[11:]
            #print(name, date)

            yield {
                "date": date,
                "name": name,
                "image": load_image(strip)
            }

# strips = load_strips("dilbert_1989_to_2023")

# for strip in strips:
#     print(strip)
#     break