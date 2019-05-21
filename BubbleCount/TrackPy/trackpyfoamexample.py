import os
import pims
import numpy as np
import pandas as pd
import trackpy as tp
from scipy import ndimage
import skimage
import matplotlib.patches as mpatches
from skimage import filters, morphology, util
import matplotlib as mpl
import matplotlib.pyplot as plt

# Optionally, tweak styles.
mpl.rc('figure',  figsize=(10, 6))
mpl.rc('image', cmap='gray')
datapath = ''
prefix = ''
id_example = 0

def crop(img):
    """
    Crop the image to select the region of interest
    """
    x_min = 45
    x_max = -35
    y_min = 100
    y_max = -300 
    return img[y_min:y_max,x_min:x_max]

def preprocess_foam(img):
    """
    Apply image processing functions to return a binary image
    """
    # Crop the pictures as for raw images.
    img = crop(img)
    # Apply thresholds
    img = filters.threshold_adaptive(img, 300)
    threshold = 0.15
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

frames = pims.ImageSequence(os.path.join(datapath, prefix + '*.tif'), process_func=preprocess_foam)
img_example = frames[id_example]

# Label elements on the picture
label_image = skimage.measure.label(img_example)
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(12, 12))
ax.imshow(img_example)


features = pd.DataFrame()
for num, img in enumerate(frames):
    label_image = skimage.measure.label(img)
    for region in skimage.measure.regionprops(label_image, intensity_image=img):
        # Everywhere, skip small and large areas
        if region.area < 5 or region.area > 800:
            continue
        # Only black areas
        if region.mean_intensity > 1:
            continue
        # On the top, skip small area with a second threshold
        if region.centroid[0] < 260 and region.area < 80: 
            continue
        # Store features which survived to the criterions
        features = features.append([{'y': region.centroid[0],
                                     'x': region.centroid[1],
                                     'frame': num,
                                     },])
                                     
tp.annotate(features[features.frame==id_example], img_example);


plt.show()
