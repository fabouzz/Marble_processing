import cv2
import imutils
import numpy as np
from imutils import contours
from skimage import measure

filtrage = 1
path = "/media/mathieu/EHDD/videos_bille/"
videoName = "mes_haut4_bille3_1.avi"
cap = cv2.VideoCapture(path + videoName)
cap.set(cv2.CAP_PROP_POS_FRAMES, 450)

# fgbg = cv2.createBackgroundSubtractorKNN()
fgbg = cv2.createBackgroundSubtractorMOG2(history=15, varThreshold=3, detectShadows=True)
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        IMAGE = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Récupération de la taille de l'image pour crop
        height, width = IMAGE.shape
        heightMin = 440
        heightMax = 900
        widthMin = 350
        widthMax = 700

        IMAGE_NEW = IMAGE[heightMin:heightMax, widthMin:widthMax]
        thresh = IMAGE_NEW
        if filtrage == 1:
        # Lissage de l'image
            thresh = cv2.erode(IMAGE_NEW, None, iterations=2)
            thresh = cv2.dilate(thresh, None, iterations=4)
            fgmask = fgbg.apply(thresh)
            thresh = cv2.threshold(fgmask, 17, 255, cv2.THRESH_BINARY_INV)[1]
            thresh = cv2.adaptiveThreshold(fgmask, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, 15, 2)

            thresh = cv2.threshold(fgmask, 2, 255, cv2.THRESH_BINARY_INV)[1]


        elif filtrage == 2:
            # Autre traitement de l'image
            # Lissage de l'image
            thresh = cv2.erode(IMAGE_NEW, None, iterations=2)
            thresh = cv2.dilate(thresh, None, iterations=4)

            # Limite de coupure pour binariser l'image 
            LimThresh = 90
            # Traitement du seuil pour toute l'image
            for x in range(thresh.shape[0]):
                for y in range(thresh.shape[1]):
                    # Si pixel trop clair, il devient blanc
                    if thresh[x, y] > LimThresh:
                        thresh[x, y] = 255
                    elif thresh[x, y] <= LimThresh:
                        thresh[x, y] = 0
    # =======================================================

        # Identification des contours
        contours = cv2.findContours(thresh, 1, 2)
        cnts = imutils.grab_contours(contours)
        nb_bulles = len(cnts)
        txtframe = "frame: " + str(int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
        txtbulle = "bulles: " + str(nb_bulles)
        font = cv2.FONT_HERSHEY_SIMPLEX
        # creating empty lists to save centers of each bubble
        xpos = []
        ypos = []


        # loop over the contours
        for c in cnts:
            # compute the center of the contour
            M = cv2.moments(c)
            # resize centers of the bubbles to fit original image
            try:
                cX = int(M["m10"] / M["m00"]) + widthMin
                cY = int(M["m01"] / M["m00"]) + heightMin
                # Place a circle on the center of the bubble
                cv2.circle(frame, (cX, cY), 3, (0, 0, 255), -1)
                cv2.putText(frame, txtbulle, (50, 100), font, 1, (50, 50, 255), 2, cv2.LINE_8)
                cv2.putText(frame, txtframe, (50, 50), font, 1, (50, 50, 255), 2, cv2.LINE_8)
            except ZeroDivisionError:
                pass
        
        cv2.imshow("output", frame)
        cv2.imshow("output2", thresh)

        if cv2.waitKey(200) & 0xFF == ord('q'):
            break
    else:
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
