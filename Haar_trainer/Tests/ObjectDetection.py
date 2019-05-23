#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
os.system("clear")


def detectFaces(faceCascade, coloredImg, scaleFactor=1.1, minNeighbors=5):
    """Detect eyes function."""
    # Copying de original image so that it won't be modified :
    imgCopy = coloredImg.copy()
    # Converting the copy to grayscale :
    gray = cv2.cvtColor(imgCopy, cv2.COLOR_BGR2GRAY)
    # Detecting faces :
    faces = faceCascade.detectMultiScale(imgCopy, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
    # Drawing rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(imgCopy, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return imgCopy


if __name__ == '__main__':
    # Loading Haar cascade :
    # faceCascade = cv2.CascadeClassifier('/home/fabouzz/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
    faceCascade = cv2.CascadeClassifier('/home/fabouzz/opencv/data/lbpcascades/lbpcascade_frontalface_improved.xml')

    # scalePercent = 30
    # img = cv2.imread('MultiFaces.jpg')
    # faces = detectFaces(faceCascade, img, scaleFactor=1.2, minNeighbors=5)
    # width = int(faces.shape[1] * scalePercent / 100)
    # height = int(faces.shape[0] * scalePercent / 100)
    # dim = (width, height)
    # # resize image
    # resized = cv2.resize(faces, dim, interpolation=cv2.INTER_AREA)
    # cv2.imshow('Images', resized)
    # if cv2.waitKey(0) & 0xFF == ord('q'):
    #     cv2.destroyAllWindows()

    # Capturing the webcam :
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        eyes = detectFaces(faceCascade, frame, scaleFactor=1.2, minNeighbors=5)
        cv2.imshow('eyes', eyes)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
