"""Video background substraction test."""
import cv2
import matplotlib.pyplot as plt

path = "/home/fabouzz/Cours/Projet_CMI_bille/mesuresBille/"
videoName = 'test_cam6.avi'
cap = cv2.VideoCapture(path + videoName)

filename = "VideoTest.avi"
cap = cv2.VideoCapture(filename)

# Background substractor MO2
fgbg = cv2.createBackgroundSubtractorMOG2()

# Background substractor GMG
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
# fgbg = cv2.createBackgroundSubtractorGMG()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(frame)
    cv2.imshow('frame', fgmask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
