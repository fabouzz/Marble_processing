import cv2
import numpy as np

"""
Affichage de la vidéo avec des modifications
"""
 
# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('VideoTest.avi')
# FIRST_FRAME = cap.read()[1]
# FIRST_FRAME = cv2.threshold(FIRST_FRAME, 127, 255, cv2.THRESH_BINARY)[1]

# Start au début 
cap.set(cv2.CAP_PROP_POS_FRAMES, 75)

# Read until video is completed
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    # thresh = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)[1]
    # frame = FIRST_FRAME - frame

    if ret == True:
        # Display the resulting frame
        cv2.imshow('Frame', frame)
    # Press Q on keyboard to  exit
        if cv2.waitKey(200) & 0xFF == ord('q'):
            break
    # Break the loop
    else:
        break
# When everything done, release the video capture object
cap.release()
# Closes all the frames
cv2.destroyAllWindows()