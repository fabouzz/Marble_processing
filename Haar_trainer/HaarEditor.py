#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Haar Editor."""
import sys
import cv2
import os
import numpy as np
import getpass
import argparse
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QDialog, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QSlider, QLineEdit, QPushButton, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--create', help='Create a new Haar cascade in current directory.')
# parser.add_argument('-m', '--modify', help='Modify an existing Haar cascade.', action='store_true')
parser.add_argument('-d', '--delete', type=str, help='Delete an existing Haar cascade')
args = parser.parse_args()


# Création de la cascade
def createHaar(haarName):
    """Create a new haar cascade file."""
    try:
        currentDir = os.getcwd()
        os.mkdir(currentDir + '/' + haarName)
        os.system('touch {}/{}/annotations.vec'.format(currentDir, haarName))
        os.makedirs(currentDir + '/' + haarName + '/neg')
        os.makedirs(currentDir + '/' + haarName + '/pos')
    except FileExistsError:
        print('This file already exists')
# def deleteHaar():


class GUI(QDialog):
    """GUI class."""

    def __init__(self):
        """GUI definition."""
        super(GUI, self).__init__()
        self.setWindowTitle("Haar Editor - " + args.create)
        # self.setGeometry(200, 200, 800, 700)
        self.haarPath = os.getcwd() + '/' + args.create
        self.scalePercent = 50
        self.objets()
        self.layout()

    def objets(self):
        """Define visual objets to place in GUI."""
        # Création de la zone de texte fichier
        self.filePath = QLineEdit('/home/fabouzz/Cours/Projet_CMI_bille/mesuresBille/test_cam6')

        # Crétion du bouton chargement
        self.load = QPushButton("Load video")
        self.load.clicked.connect(self.Load)

        # Création du bouton addNeg
        self.addNeg = QPushButton('Add neg frames')
        self.addNeg.clicked.connect(self.addNegSample)
        self.negSlice = QLineEdit('Start:End')

        # Création du bouton addPos
        self.addPos = QPushButton('Add pos frames')
        self.addPos.clicked.connect(self.addPosSample)
        self.posSlice = QLineEdit('Start:End')

        # Création du bouton Anotate vec file
        self.anotateVec = QPushButton('Anotate Vec file')
        self.anotateVec.clicked.connect(self.anotateVecFile)

        # Création du bouton train cascade
        self.trainButton = QPushButton('Train cascade')
        self.trainButton.clicked.connect(self.trainCascade)

        # Figure contenant l'image de la vidéo
        self.figVid = Figure(dpi=100, tight_layout=True)
        self.Canvas = FigureCanvas(self.figVid)

        # Crétion du slider
        self.Slider = QSlider(Qt.Horizontal)
        self.Slider.setMinimum(1)
        self.Slider.setMaximum(100)
        self.Slider.setTickInterval(1)
        self.Slider.setValue(0)
        self.Slider.valueChanged.connect(self.sliderUpdate)

        # Création du label
        self.statusLabel = QLabel(self)
        self.statusLabel.setText('Wilkommen, please load a video file before adding samples')

    def layout(self):
        """GUI layout using previous objets."""
        MainLayout = QVBoxLayout()

        LoadLayout = QHBoxLayout()
        LoadLayout.addWidget(self.load)
        LoadLayout.addWidget(self.filePath)

        AddLayout = QHBoxLayout()
        AddLayout.addWidget(self.addPos)
        AddLayout.addWidget(self.posSlice)
        AddLayout.addWidget(self.addNeg)
        AddLayout.addWidget(self.negSlice)

        VidLayout = QHBoxLayout()
        VidLayout.addWidget(self.Canvas)

        BottomLayout = QHBoxLayout()
        BottomLayout.addWidget(self.statusLabel)
        BottomLayout.addWidget(self.anotateVec)
        BottomLayout.addWidget(self.trainButton)

        MainLayout.addLayout(LoadLayout)
        # MainLayout.addLayout(NegLayout)
        MainLayout.addLayout(AddLayout)
        MainLayout.addLayout(VidLayout)
        MainLayout.addWidget(self.Slider)
        MainLayout.addLayout(BottomLayout)
        self.setLayout(MainLayout)

    def sliderUpdate(self):
        """Update the bottom screen slider. Updates data."""
        self.plot(pos=self.Slider.value())
        # print(self.Slider.value())

    def keyPressEvent(self, event):
        """Keyboard navigation."""
        if event.key() == Qt.Key_Right:
            self.slider.setValue(self.slider.value() + 1)
        elif event.key() == Qt.Key_Left:
            self.slider.setValue(self.slider.value() - 1)
        else:
            # Eviter le crash de l'interface dans le cas d'un spam de touche
            try:
                self.keyPressEvent(self, event)
            except TypeError:
                pass

    def Load(self):
        """."""
        fileName = self.filePath.text()
        self.cvVideo = cv2.VideoCapture(fileName + '.avi')  # Chargement video
        with open(fileName + '.cih') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('Total Frame :'):
                    self.nFrames = int(line.split(' : ')[1])
                if line.startswith('Image Width : '):
                    self.imWidth = int(line.split(' : ')[1])
                if line.startswith('Image Height :'):
                    self.imHeight = int(line.split(': ')[1])
        self.Slider.setMaximum(self.nFrames)
        self.plot()
        self.statusLabel.clear()
        self.statusLabel.setText('Loaded video {}.avi'.format(fileName.split('/')[-1]))

    def plot(self, pos=0):
        """."""
        self.cvVideo.set(cv2.CAP_PROP_POS_FRAMES, self.Slider.value())
        ret, self.frame = self.cvVideo.read()
        self.figVid.clear()
        ax = self.figVid.add_subplot(111)
        ax.set_title('Frame n° : ' + str(self.Slider.value()))
        ax.imshow(self.frame)
        ax.set_xticks([])
        ax.set_yticks([])
        self.Canvas.draw()

    def addNegSample(self):
        """."""
        slice = self.negSlice.text()
        path = self.filePath.text()
        fileName = path.split('/')[-1]
        cap = cv2.VideoCapture(path + '.avi')
        # fgbg = cv2.createBackgroundSubtractorKNN()
        count = int(slice.split(':')[0])
        with open(self.haarPath + '/bg.txt', "a") as writer:
            while count <= int(slice.split(':')[-1]):
                cap.set(cv2.CAP_PROP_POS_FRAMES, count)
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # fgmask = fgbg.apply(gray)
                # thresh = cv2.threshold(fgmask, 17, 255, cv2.THRESH_BINARY_INV)[-1]
                # width = int(gray.shape[1] * self.scalePercent / 100)
                # height = int(gray.shape[0] * self.scalePercent / 100)
                # dim = (width, height)
                # # resize image
                # resized = cv2.resize(gray, dim, interpolation=cv2.INTER_AREA)
                cv2.imwrite(self.haarPath + '/neg/{}_{}.png'.format(fileName, count), gray)
                count += 1
                writer.write('{}/neg/{}_{}.png\n'.format(self.haarPath, fileName, count - 1))

            self.statusLabel.clear()
            self.statusLabel.setText('Added {} neg frames'.format(int(slice.split(':')[-1]) - int(slice.split(':')[0]) + 1))

    def addPosSample(self):
        """."""
        slice = self.posSlice.text()
        path = self.filePath.text()
        fileName = path.split('/')[-1]
        cap = cv2.VideoCapture(path + '.avi')
        # fgbg = cv2.createBackgroundSubtractorKNN()
        count = int(slice.split(':')[0])
        while count <= int(slice.split(':')[-1]):
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # fgmask = fgbg.apply(gray)
            # thresh = cv2.threshold(fgmask, 17, 255, cv2.THRESH_BINARY_INV)[-1]
            # width = int(gray.shape[1] * self.scalePercent / 100)
            # height = int(gray.shape[0] * self.scalePercent / 100)
            # dim = (width, height)
            # # resize image
            # resized = cv2.resize(gray, dim, interpolation=cv2.INTER_AREA)
            cv2.imwrite(self.haarPath + '/pos/{}_{}.png'.format(fileName, count), gray)
            count += 1

            self.statusLabel.clear()
            self.statusLabel.setText('Added {} pos frames'.format(int(slice.split(':')[-1]) - int(slice.split(':')[0]) + 1))

    def anotateVecFile(self):
        """."""
        os.system('opencv_annotation -a={0}/annotations.vec -i={0}/pos/ ----maxWindowHeight=300 --resizeFactor=0.25'.format(self.haarPath))

    def trainCascade(self):
        """."""
        data = self.haarPath
        vecFile = data + '/annotations.vec'
        bgFile = data + '/bg.txt'
        numPos = len(os.listdir(data + '/pos/'))
        numNeg = len(os.listdir(data + '/neg/'))
        numStages = '10'
        minHitRate = '0.999'
        maxFalseAlarmRate = '0.5'
        width = self.imWidth
        height = self.imHeight
        os.system('opencv_traincascade -data {} -vec {} -bg {} -numPos {} -numNeg {} -numStages {} -minHitRate {} -maxFalseAlarmRate {} -featureType HAAR -w {} -h {}'.format(data, vecFile, bgFile, numPos, numNeg, numStages, minHitRate, maxFalseAlarmRate, width, height))


if __name__ == '__main__':
    if args.create:
        createHaar(args.create)
        app = QApplication(sys.argv)
        clock = GUI()
        clock.show()
        sys.exit(app.exec_())
