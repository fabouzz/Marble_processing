"""
Testing the trackpy library
"""
import os
import cv2

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import pims
import trackpy as tp
from scipy import ndimage
from skimage import filters, morphology, util
from pims import pipeline

@pipeline
def as_grey(frame):
    red = frame[:, :, 0]
    green = frame[:, :, 1]
    blue = frame[:, :, 2]
    return 0.2125 * red + 0.7154 * green + 0.0721 * blue

def crop(img):
    """
    Crop the image to select the region of interest
    """
    x_min = 300
    x_max = 600
    y_min = 440
    y_max = 672
    return img[y_min:y_max,x_min:x_max]

def preprocess_foam(img):
    """
    Apply image processing functions to return a binary image
    """
    # Crop the pictures as for raw images.
    img = crop(img)
    # Apply thresholds
    block_size = 5
    img = filters.threshold_local(img, block_size)
    threshold = 0.30
    idx = img > img.max() * threshold
    idx2 = img < img.max() * threshold
    img[idx] = 0
    img[idx2] = 255
    # Dilatate to get a continous network
    # of liquid films
    img = ndimage.binary_dilation(img)
    img = ndimage.binary_dilation(img)
    return util.img_as_int(img)

IMAGE_PATH = "../images/screen_bulles.png"
ORIG_IMAGE = cv2.imread(IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
# Pour éviter d'avoir 3 channels RGB identiques
IMAGE = preprocess_foam(ORIG_IMAGE)
ORIG_IMAGE = crop(ORIG_IMAGE)

fig, ax = plt.subplots(1, 2)
ax[0].imshow(ORIG_IMAGE, cmap='Greys_r')
ax[1].imshow(IMAGE, cmap='Greys')
plt.show()
# ==========================================================

# fig, ax = plt.subplots()
# id_example = 200
# filepath = "/media/mathieu/EHDD/videos_bille/mes_haut5_bille2_2.avi"

# frames = pims.Video(filepath)
# frame_n = frames[id_example]
# frame = as_grey(frame_n)
# print(frame)
# ax.imshow(frame, cmap='Greys_r')

# plt.show()