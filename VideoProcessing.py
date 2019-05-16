"""Video background substraction."""
import cv2
import numpy as np
import matplotlib.pyplot as plt

path = "/home/fabouzz/Cours/Projet_CMI_bille/mesuresBille/"
videoName = 'test_cam6.avi'
cap = cv2.VideoCapture(path + videoName)

# filename = "VideoTest.avi"
# cap = cv2.VideoCapture(filename)

# Background substractor MO2
# fgbg = cv2.createBackgroundSubtractorMOG2()

# Background substractor GMG
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fgbg = cv2.createBackgroundSubtractorKNN()
fig, ax = plt.subplots()
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)
    ret2, thresh = cv2.threshold(fgmask, 17, 255, cv2.THRESH_BINARY_INV)
    # Lisser l'image pour enlever du bruit
    # thresh = cv2.erode(fgmask, None, iterations=1)
    # thresh = cv2.dilate(thresh, None, iterations=4)
<<<<<<< HEAD
    cv2.imshow('frame', thresh)
=======
    cv2.imshow('frame', fgmask)
    
>>>>>>> af791babaa567eb96c1198d92f678b6058353e9d
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
