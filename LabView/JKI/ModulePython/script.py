import cv2
import numpy as np
from functions import *

def decode_img(img):
    img_rgb = np.array(img, dtype=np.uint8).transpose(1, 2, 0)
    img_decoded = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    return img_decoded

def encode_img(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_encoded= img_rgb.transpose(2, 0, 1).tolist()
    return img_encoded

def process_image(raw_img):
    frame = decode_img(raw_img)

    img_contour = frame.copy()

    img = color_space(frame, red_yellow_lower, red_yellow_upper)
    get_shapes(img, img_contour, "red")

    img = color_space(frame, blue_lower, blue_upper)
    get_shapes(img, img_contour, "blue")

    # img_stack = stackImages(0.8, ([frame, img, img_contour]))
    # cv.imshow("Result", img_stack) 

    res = encode_img(img_contour)
    return res