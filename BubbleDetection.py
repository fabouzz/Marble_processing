# USAGE
# python detect_bright_spots.py --image images/lights_01.png

# import the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
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
        if thresh[y, x] > 70:
            thresh[y, x] = 255

thresh = cv2.adaptiveThreshold(thresh, 255, 
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 3, 0)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
 		cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
center = None

if len(cnts) > 0:
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
    c = max(cnts, key=cv2.contourArea)
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    print(center)

cv2.imshow("original image", IMAGE)
cv2.imshow("treated image", thresh)

cv2.waitKey(0)