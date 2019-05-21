import cv2
import numpy as np
import os

path = "/media/mathieu/EHDD/videos_bille/"
videoName = "mes_haut4_bille3_1.avi"

# Playing video from file:
cap = cv2.VideoCapture(path + videoName)
print(cap)

try:
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    print ('Error: Creating directory of data')

currentFrame = 0
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret == False:
        break

    # Saves image of the current frame in jpg file
    name = './data/frame' + str(currentFrame) + '.jpg'
    print ('Creating...' + name)
    cv2.imwrite(name, frame)

    # To stop duplicate images
    currentFrame += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()