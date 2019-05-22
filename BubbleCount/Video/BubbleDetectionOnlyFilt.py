#!/usr/bin/env python

import os
import pims
import cv2
import numpy as np
from scipy import ndimage

from skimage import filters, morphology, util

import matplotlib as mpl
import matplotlib.pyplot as plt

# Optionally, tweak styles.
mpl.rc('figure',  figsize=(10, 6))
mpl.rc('image', cmap='Greys_r')

mes = "mes_haut4_bille3_1"
datapath = "/media/mathieu/EHDD/ImageSequenceVideos/{}/".format(mes)

prefix = 'frame'
id_example = 440
# on s'intéresse pour ce fichier aux bulles 
# de 440 à 650

def crop(img):
    """
    Crop the image to select the region of interest
    """
    x_min = 400
    x_max = 672
    y_min = 400
    y_max = 672 
    return img[y_min:y_max,x_min:x_max]

def preprocess_foam(img):
    """
    Apply image processing functions to return a binary image
    """
    # Crop the pictures as for raw images.
    img = crop(img)
	# Apply greyscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply thresholds
    img = filters.threshold_local(img, 3)
    threshold = 0.5
    idx = img > img.max() * threshold
    idx2 = img < img.max() * threshold
    img[idx] = 0
    img[idx2] = 255
    # Dilatate to get a continous network
    # of liquid films

    n_dilat = 1
    for _ in range(n_dilat):
        img = ndimage.binary_dilation(img)
        print(img)
    return util.img_as_int(img)

frames = pims.ImageSequence(os.path.join(datapath, prefix + '*.png'), process_func=preprocess_foam)
print(frames)

img = frames[200]
print(img)
cv2.imshow("treated image", img)
cv2.waitKey(0)
	
# fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(8, 4))
# ax.imshow(img)
# plt.show()