import numpy as np
import matplotlib.pyplot as plt 
import cv2
import sys

videoPath = "VideoTest.avi"
IMG_START = 65 # numéro de l'image de départ
# Create a video capture object to read videos
cap = cv2.VideoCapture(videoPath)
# récupération de la première frame
FIRST_FRAME = cap.read()[1]
cap.set(cv2.CAP_PROP_POS_FRAMES, 150)
print(type(FIRST_FRAME), FIRST_FRAME.shape)

cap.set(cv2.CAP_PROP_POS_FRAMES, IMG_START)
frametest = cap.read()[1]
thresh = cv2.threshold(frametest, 127, 255, cv2.THRESH_BINARY)[1]

# opération sur l'image
frametest = frametest - FIRST_FRAME

fig, ax = plt.subplots()
ax.imshow(thresh)

plt.show()

