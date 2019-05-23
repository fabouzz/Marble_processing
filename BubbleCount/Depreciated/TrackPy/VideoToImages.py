import cv2
import numpy as np
import os

path = "/media/mathieu/EHDD/videos_bille/"
videoName = "mes_haut4_bille3_1"
writing_path = "/media/mathieu/EHDD/ImageSequenceVideos/" + videoName + "/"

# Playing video from file:
cap = cv2.VideoCapture(path + videoName + ".avi")

try:
    if not os.path.exists(writing_path):
        os.makedirs(writing_path)
except OSError:
    print ('Error: Creating directory of data')

sec = 0
frameRate = 0.05
# it will capture 1 image in each n second
count = 1

def getFrame(sec):
    cap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
    hasFrames, image = cap.read()
    if hasFrames:
        cv2.imwrite(writing_path + "frame" + str(count) + ".png", image)     # save frame as JPG file
        print(count)
    return hasFrames

success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)


# currentFrame = 0
# while cap.isOpened():
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     if ret == False:
#         break

#     # Saves image of the current frame in jpg file
#     name = './data/frame' + str(currentFrame) + '.jpg'
#     print ('Creating...' + name)
#     cv2.imwrite(name, frame)

#     # To stop duplicate images
#     currentFrame += 1

# When everything done, release the capture

cap.release()
cv2.destroyAllWindows()
