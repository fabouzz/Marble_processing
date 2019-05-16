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
IMAGE = cv2.cvtColor(IMAGE, cv2.COLOR_BGR2GRAY)

height, width = IMAGE.shape
print(height, width)
IMAGE = IMAGE[430:height, 0:width]

thresh = cv2.erode(IMAGE, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=4)

for x in range(thresh.shape[1]):
    for y in range(thresh.shape[0]):
        if thresh[y, x] > 100:
            thresh[y, x] = 255

#thresh = cv2.adaptiveThreshold(thresh, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#            cv2.THRESH_BINARY, 11, 2)

cv2.imshow("original image", IMAGE)
cv2.imshow("treated image", thresh)

cv2.waitKey(0)