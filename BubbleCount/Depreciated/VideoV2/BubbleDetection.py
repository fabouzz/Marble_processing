import cv2
import numpy as np
from skimage import filters, morphology, util
from imutils import contours
from scipy import ndimage
import scipy.misc
def ImageProcessing(img):
    """
    Apply image processing functions to return a binary image
    """

    # adapt to greyscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Récupération de la taille de l'image pour crop
    height, width = img.shape
    # heightMin = 440
    # heightMax = 900
    widthMin = 450
    widthMax = 650
    # Crop image
    img = img[430:height, widthMin:widthMax]

    # Apply thresholds
    img = filters.threshold_local(img, 1)
    # limite intensité lumineuse pour noir / blanc
    threshold = 0.3
    idx = img > img.max() * threshold
    idx2 = img < img.max() * threshold
    # si le pixel est au-dessus de la limite, il est noir
    img[idx] = 0
    # si le pixel est au-dessous de la limite, il est blanc
    img[idx2] = 255
    # Au final, on veut que les bulles soient noires

    # Dilatate to get a continous network of bubbles
    n_dilat = 1
    for _ in range(n_dilat):
        img = ndimage.binary_dilation(img)

    # Sortie de la fonction
    return util.img_as_int(img)

# ===============================================================


path = "/media/mathieu/EHDD/videos_bille/"
videoName = "mes_haut4_bille3_1.avi"
cap = cv2.VideoCapture(path + videoName)

START_FRAME = 400
# Start au début 
cap.set(cv2.CAP_PROP_POS_FRAMES, START_FRAME)
font = cv2.FONT_HERSHEY_SIMPLEX

# Read until video is completed
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    thresh = frame
    thresh = ImageProcessing(frame)
    # thresh = scipy.misc.toimage(thresh)

    # thresh = cv2.threshold(thresh, 127, 255, cv2.THRESH_BINARY)[1]
    # thresh[thresh != 0] = 255
    print(thresh)

    if ret == True:
        # Display the resulting frame
        txtframe = "frame: " + str(int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
        cv2.imshow('original frame', frame)
        cv2.imshow('Frame', thresh)
        cv2.putText(frame, txtframe, (50, 50), font, 1, (50, 50, 255), 2, cv2.LINE_8)
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