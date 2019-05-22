import cv2
import imutils
import numpy as np
from imutils import contours
from scipy import ndimage
from skimage import filters, morphology, util


def preprocess_foam(img):
    """
    Apply image processing functions to return a binary image
    """
    # adapt to greyscale
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply thresholds
    img = filters.threshold_local(img, 299)
    threshold = 0.80
    idx = img > img.max() * threshold
    idx2 = img < img.max() * threshold
    img[idx] = 0
    img[idx2] = 255
    # Dilatate to get a continous network
    # of liquid films
    n_dilat = 1
    for _ in range(n_dilat):
        img = ndimage.binary_dilation(img)
    return util.img_as_int(img)


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
    # ======================================================= #
    #                       FILTRAGE                          # 
    # ======================================================= #
        thresh = preprocess_foam(thresh)
        # thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
        # thresh = cv2.threshold(thresh, 127, 255, cv2.THRESH_BINARY)
        # thresh = (np.asarray(thresh) / 128.498)
        # thresh = np.asarray(thresh, dtype='int16')
    # =========================================================
        # Identification des contours
        contours = cv2.findContours(thresh, 1, 2)
        cnts = imutils.grab_contours(contours)
        nb_bulles = len(cnts)
        txtframe = "frame: " + str(int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
        txtbulle = "bulles: " + str(nb_bulles)
        font = cv2.FONT_HERSHEY_SIMPLEX
        # creating empty lists to save centers of each bubble

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