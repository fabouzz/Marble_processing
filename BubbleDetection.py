# USAGE
# python detect_bright_spots.py --image images/lights_01.png

# import the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
import scipy.ndimage
import argparse
import imutils
import cv2

IMAGE_PATH = "screen_bulles.png"
IMAGE = cv2.imread(IMAGE_PATH)
# Pour éviter d'avoir 3 channels RGB identiques
IMAGE = cv2.cvtColor(IMAGE, cv2.COLOR_BGR2GRAY)

# Récupération de la taille de l'image pour crop
height, width = IMAGE.shape
print(height, width)
IMAGE = IMAGE[430:height, 0:width]

thresh = cv2.erode(IMAGE, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=4)

for x in range(thresh.shape[1]):
    for y in range(thresh.shape[0]):
        # Si pixel trop clair, il devient blanc
        if thresh[y, x] > 60:
            thresh[y, x] = 255

cv2.imshow("original image", IMAGE)
cv2.imshow("treated image", thresh)
cv2.waitKey(0)