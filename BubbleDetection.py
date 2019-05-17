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
heightMin = 440
heightMax = height
widthMin = 330
widthMax = 700

IMAGE = IMAGE[heightMin:heightMax, widthMin:widthMax]

# Lissage de l'image
thresh = cv2.erode(IMAGE, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=4)

# Limite coupure pour binariser l'image 
LimThresh = 75
for x in range(thresh.shape[0]):
    for y in range(thresh.shape[1]):
        # Si pixel trop clair, il devient blanc
        if thresh[x, y] > LimThresh:
            thresh[x, y] = 255
        elif thresh[x, y] <= LimThresh:
            thresh[x, y] = 0
# =======
# Fin du traitement de l'image

contours, h = cv2.findContours(thresh, 1, 2)
nb_bulles = len(contours)
print(nb_bulles)

thresh_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
for cnt in contours:
  cv2.drawContours(thresh_rgb, [cnt], 0, (0, 0, 255), 2)

if __name__ == "__main__":
    cv2.imshow("treated image", thresh_rgb)
    cv2.waitKey(0)