from imutils import contours
from skimage import measure
import numpy as np
import scipy.ndimage
import argparse
import imutils
import cv2
path = "/home/mathieu/Documents/S4/ProjetBille/VideoProcessing/"
videoName = "VideoTest.avi"
cap = cv2.VideoCapture(path + videoName)
cap.set(cv2.CAP_PROP_POS_FRAMES, 200)
while cap.isOpened():
    ret, frame = cap.read()

# Pour éviter d'avoir 3 channels RGB identiques
    IMAGE = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Récupération de la taille de l'image pour crop
    height, width = IMAGE.shape
    # IMAGE = IMAGE[440:height, 330:700]

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


    cv2.imshow("treated image", thresh_rgb)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()