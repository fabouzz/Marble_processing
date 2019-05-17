from imutils import contours
from skimage import measure
import numpy as np
import imutils
import cv2

path = "/media/mathieu/EHDD/videos_bille/"
videoName = "mes_haut5_bille3_1.avi"
cap = cv2.VideoCapture(path + videoName)
cap.set(cv2.CAP_PROP_POS_FRAMES, 240)

fgbg = cv2.createBackgroundSubtractorKNN()
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        IMAGE = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Récupération de la taille de l'image pour crop
        height, width = IMAGE.shape
        heightMin = 440
        heightMax = height
        widthMin = 300
        widthMax = 860

        IMAGE_NEW = IMAGE[heightMin:heightMax, widthMin:widthMax]
        thresh = IMAGE_NEW
        # Lissage de l'image
        # thresh = cv2.erode(IMAGE_NEW, None, iterations=2)
        # thresh = cv2.dilate(thresh, None, iterations=4)
        fgmask = fgbg.apply(thresh)
        thresh = cv2.adaptiveThreshold(fgmask, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, 5, 2)
        
        # Identification des contours
        contours = cv2.findContours(thresh, 1, 2)
        cnts = imutils.grab_contours(contours)
        nb_bulles = len(cnts)
        print(nb_bulles)
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