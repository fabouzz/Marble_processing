import cv2 as cv
import os
import imutils
import numpy as np
from skimage import filters, morphology, util
from scipy import ndimage
from BubbleDetection import *

datapath = "/media/mathieu/EHDD/videos_bille/"
filename = "mes_haut4_bille3_1.avi"
# filename = 'mes_haut3_bille3_1.avi'
video = Bubble(datapath, filename, beginFrame=20)

while True:
    ret, frame = video.cap.read()

    if ret:
        heightMin = 400
        heightMax = 900
        widthMin = 350
        widthMax = 700
        crop_frame = video.ImageProcessing(frame, heightMin, heightMax, widthMin, widthMax)
        # treated_frame = video.CustomFilter(crop_frame)
        # treated_frame = video.BGFilterThreshold(crop_frame)
        treated_frame = video.SmoothFiltering(crop_frame, blockSize=11, threshold=0.25)
        # treated_frame = video.ManualThreshold(crop_frame)
        xpos, ypos, txtframe, txtbulle = video.BubbleFinding(treated_frame)
        # xpos, ypos, txtframe, txtbulle = video.TrackpyFinding(treated_frame)
      
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