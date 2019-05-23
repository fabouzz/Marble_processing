import cv2
import os
import imutils
import numpy as np
from skimage import filters, morphology, util
from scipy import ndimage

from BubbleDetection import *

datapath = "/media/mathieu/EHDD/videos_bille/"
filename = "mes_haut4_bille3_1.avi"
video = Bubble(datapath, filename, beginFrame=500)

while True:
    ret, frame = video.cap.read()

    if ret:
        crop_frame = video.ImageProcessing(frame)
        # treated_frame = video.CustomFilter(crop_frame)
        # treated_frame = video.BGFilterThreshold(crop_frame)
        treated_frame = video.SmoothFiltering(crop_frame)
        # treated_frame = video.ManualThreshold(crop_frame)
        xpos, ypos, txtframe, txtbulle = video.BubbleFinding(treated_frame)
        
        for c in range(len(xpos)):
            cX = xpos[c]
            cY = ypos[c]
            cv2.circle(frame, (cX, cY), 3, (0, 0, 255), -1)
        cv2.putText(frame, txtbulle, (50, 100), video.font, 1, (50, 50, 255), 2, cv2.LINE_8)
        cv2.putText(frame, txtframe, (50, 50), video.font, 1, (50, 50, 255), 2, cv2.LINE_8)

        cv2.imshow("original frame", frame)
        cv2.imshow("filtered image", treated_frame)
    
        if cv2.waitKey(200) & 0xFF == ord('q'):
            break
    else:
        break

# When everything done, release the capture
video.cap.release()
cv2.destroyAllWindows()