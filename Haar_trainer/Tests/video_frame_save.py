#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
os.system("clear")

slice = '1:10'
path = '/home/fabouzz/Cours/Projet_CMI_bille/mesuresBille/'
video = 'mes_cam_bille1_2'

with open(path + video + '.cih') as cih:
    lines = cih.readlines()
    for line in lines:
        if line.startswith('Total Frame :'):
            frame_count = int(line.split(' : ')[1])

cap = cv2.VideoCapture(path + video + '.avi')

fgbg = cv2.createBackgroundSubtractorKNN()
fig, ax = plt.subplots()

count = 1
while count <= 10:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)
    ret2, thresh = cv2.threshold(fgmask, 17, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite('imfold/{}.png'.format(count), frame)
    count += 1

with open('test.txt', 'a') as writefile:
    for ligne in range(3):
        writefile.write('ligne{}\n'.format(ligne))
