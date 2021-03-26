import cv2
import numpy as np

def decode_img(img):
    img_rgb = np.array(img, dtype=np.uint8).transpose(1, 2, 0)
    img_decoded = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    return img_decoded

def encode_img(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_encoded= img_rgb.transpose(2, 0, 1).tolist()
    return img_encoded

def process_image(raw_img):
    img = decode_img(raw_img)
    img = cv2.rectangle(img, (250, 100), (950, 800), (255, 255, 0), 2)
    # cv2.imwrite('test.jpg', img)
    res = encode_img(img)
    return res