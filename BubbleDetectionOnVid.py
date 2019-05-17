from imutils import contours
from skimage import measure
import numpy as np
import imutils
import cv2

path = "/media/mathieu/EHDD/videos_bille/"
videoName = "mes_haut5_bille3_1.avi"
cap = cv2.VideoCapture(path + videoName)
cap.set(cv2.CAP_PROP_POS_FRAMES, 150)
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        IMAGE = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Récupération de la taille de l'image pour crop
        height, width = IMAGE.shape
        heightMin = 370
        heightMax = height
        widthMin = 300
        widthMax = 860

        IMAGE_NEW = IMAGE[heightMin:heightMax, widthMin:widthMax]

        # Lissage de l'image
        thresh = cv2.erode(IMAGE_NEW, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=4)

        # Limite de coupure pour binariser l'image 
        # Traitement et application du filtre
        # LimThresh = 90
        # # Traitement du seuil pour toute l'image
        # for x in range(thresh.shape[0]):
        #     for y in range(thresh.shape[1]):
        #         # Si pixel trop clair, il devient blanc
        #         if thresh[x, y] > LimThresh:
        #             thresh[x, y] = 255
        #         elif thresh[x, y] <= LimThresh:
        #             thresh[x, y] = 0
        # =======
        # Fin du traitement de l'image

        # Identification des contours
        contours= cv2.findContours(thresh, 1, 2)
        cnts = imutils.grab_contours(contours)
        nb_bulles = len(cnts)

        # creating empty lists to save centers of each bubble
        xpos = []
        ypos = []
        # loop over the contours
        for c in cnts:
            # compute the center of the contour
            M = cv2.moments(c)
            # resize centers of the bubbles to fit original image
            cX = int(M["m10"] / M["m00"]) + widthMin
            cY = int(M["m01"] / M["m00"]) + heightMin
            # Place a circle on the center of the bubble
            cv2.circle(frame, (cX, cY), 3, (0, 0, 255), -1)
        
        cv2.imshow("output", frame)
        cv2.imshow("output2", thresh)
        if cv2.waitKey(200) & 0xFF == ord('q'):
            break

    else:
        break



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()