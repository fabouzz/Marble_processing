import os
import pims
import cv2
import numpy as np
import pandas as pd
import trackpy as tp
from scipy import ndimage

import skimage
from skimage import filters, morphology, util

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# Optionally, tweak styles.
mpl.rc('figure',  figsize=(10, 6))
mpl.rc('image', cmap='gray')

datapath = 'data/'
prefix = 'frame'
id_example = 440
# on s'intéresse pour ce fichier aux bulles 
# de 440 à 650

def crop(img):
    """
    Crop the image to select the region of interest
    """
    x_min = 0
    x_max = 1024
    y_min = 0
    y_max = 672 
    return img[y_min:y_max,x_min:x_max]

def preprocess_foam(img):
    """
    Apply image processing functions to return a binary image
    """
    # Crop the pictures as for raw images.
    img = crop(img)
    # adapt to greyscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply thresholds
    img = filters.threshold_local(img, 299)
    threshold = 0.30
    idx = img > img.max() * threshold
    idx2 = img < img.max() * threshold
    img[idx] = 0
    img[idx2] = 255
    # Dilatate to get a continous network
    # of liquid films
    n_dilat = 2
    for _ in range(n_dilat):
        img = ndimage.binary_dilation(img)
    return util.img_as_int(img)

frames = pims.ImageSequence(os.path.join(datapath, prefix + '*.jpg'), process_func=crop)
print(frames)

img_example = frames[id_example]

# Label elements on the picture
# label_image = skimage.measure.label(img_example)
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(8, 4))
ax.imshow(img_example, cmap='jet')
plt.show()
