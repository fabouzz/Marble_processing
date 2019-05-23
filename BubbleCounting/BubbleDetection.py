import cv2 as cv
import os
import imutils
import numpy as np
from skimage import filters, morphology, util
from scipy import ndimage


class Bubble:
    """
    Classe permettant la détection de bulle sur une mesure vidéo
        - Plusieurs méthodes de filtrage sont proposés
        - Plusieurs méthodes de tracking pourront être développées par la suite
    """
    def __init__(self, datapath, videoName, beginFrame=0):
        self.datapath = datapath
        self.videoName = videoName
        self.font = cv.FONT_HERSHEY_SIMPLEX
        self.beginFrame = beginFrame
        
        self.ImportVideo()

    def ImportVideo(self):
        if os.path.exists(self.datapath):
            self.cap = cv.VideoCapture(self.datapath + self.videoName)
            self.cap.set(cv.CAP_PROP_POS_FRAMES, self.beginFrame)
        else: 
            print("Directory not found")
        # fgbg = cv.createBackgroundSubtractorKNN()
        self.fgbg = cv.createBackgroundSubtractorMOG2(history=1, varThreshold=30, detectShadows=False)

    def ImageProcessing(self, frame):
        # getting the image as greyscale
        IMAGE = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Récupération de la taille de l'image pour crop
        # height, width = IMAGE.shape
        heightMin = 440
        heightMax = 900
        widthMin = 350
        widthMax = 700
        self.heightMin = heightMin
        self.widthMin = widthMin

        IMAGE = IMAGE[heightMin:heightMax, widthMin:widthMax]
        return IMAGE

####################################################################
#                           FILTERS                                # 
####################################################################
    def BGFilterThreshold(self, frame, blockSize=15):
        frame = self.fgbg.apply(frame)
        thresh = cv.adaptiveThreshold(frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                           cv.THRESH_BINARY_INV, blockSize, 2)
        # Lissage de l'image
        thresh = cv.erode(thresh, None, iterations=2)
        thresh = cv.dilate(thresh, None, iterations=4)
        return thresh

    def CVFilter(self, frame, blockSize=15):
        thresh = cv.erode(frame, None, iterations=2)
        thresh = cv.dilate(thresh, None, iterations=4)
        fgmask = self.fgbg.apply(thresh)
        thresh = cv.threshold(fgmask, 17, 255, cv.THRESH_BINARY_INV)[1]
        thresh = cv.adaptiveThreshold(fgmask, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv.THRESH_BINARY, blockSize, 2)
        thresh = cv.threshold(fgmask, 2, 255, cv.THRESH_BINARY_INV)[1]
        return thresh

    def ManualThreshold(self, frame, LimThresh=90):
        # Autre traitement de l'image
        # Lissage de l'image
        thresh = cv.erode(frame, None, iterations=2)
        thresh = cv.dilate(thresh, None, iterations=4)

        # Traitement du seuil pour toute l'image
        for x in range(thresh.shape[0]):
            for y in range(thresh.shape[1]):
                # Limite de coupure pour binariser l'image 
                # Si pixel trop clair, il devient blanc
                if thresh[x, y] > LimThresh:
                    thresh[x, y] = 255
                elif thresh[x, y] <= LimThresh:
                    thresh[x, y] = 0
        return thresh

    def SmoothFiltering(self, frame, blockSize=11, threshold=0.3, n_dilat=1):
        """
        Apply image processing functions to return a binary image
        """
        # adapt to greyscale
        # img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Apply thresholds
        frame = filters.threshold_local(frame, blockSize)
        idx = frame > frame.max() * threshold
        idx2 = frame < frame.max() * threshold
        frame[idx] = 0
        frame[idx2] = 255
        # Dilatate to get a continous network of bubbles
        for _ in range(n_dilat):
            frame = ndimage.binary_dilation(frame)
        frame = util.img_as_ubyte(frame)
        # print(frame)
        return frame

# ====================================================

    def BubbleFinding(self, img):
        contours = cv.findContours(img, 1, 2)
        cnts = imutils.grab_contours(contours)
        nb_bulles = len(cnts)
        txtframe = "frame: " + str(int(self.cap.get(cv.CAP_PROP_POS_FRAMES)))
        txtbulle = "bulles: " + str(nb_bulles)
        # creating empty lists to save centers of each bubble
        xpos = []
        ypos = []
        # loop over the contours
        for c in cnts:
            # compute the center of the contour
            M = cv.moments(c)
            # resize centers of the bubbles to fit original image
            try:
                cX = int(M["m10"] / M["m00"]) + self.widthMin
                cY = int(M["m01"] / M["m00"]) + self.heightMin
                # Place a circle on the center of the bubble
                xpos.append(cX)
                ypos.append(cY)
            except ZeroDivisionError:
                pass
        return xpos, ypos, txtframe, txtbulle


if __name__ == '__main__':
    datapath = "/media/mathieu/EHDD/videos_bille/"
    filename = "mes_haut4_bille3_1.avi"
    video = Bubble(datapath, filename, beginFrame=400)

    while True:
        ret, frame = video.cap.read()

        if ret:
            crop_frame = video.ImageProcessing(frame)
            # treated_frame = video.CustomFilter(crop_frame)
            # treated_frame = video.BGFilterThreshold(crop_frame)
            treated_frame = video.ManualThreshold(crop_frame)
            xpos, ypos, txtframe, txtbulle = video.BubbleFinding(treated_frame)
            
            for c in range(len(xpos)):
                cX = xpos[c]
                cY = ypos[c]
                cv.circle(frame, (cX, cY), 3, (0, 0, 255), -1)
            cv.putText(frame, txtbulle, (50, 100), video.font, 1, (50, 50, 255), 2, cv.LINE_8)
            cv.putText(frame, txtframe, (50, 50), video.font, 1, (50, 50, 255), 2, cv.LINE_8)

            cv.imshow("original frame", frame)
            cv.imshow("filtered image", treated_frame)
        
            if cv.waitKey(200) & 0xFF == ord('q'):
                break
        else:
            break

    # When everything done, release the capture
    video.cap.release()
    cv.destroyAllWindows()