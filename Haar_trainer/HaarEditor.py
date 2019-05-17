#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""
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
        print(self.haarPath)
        self.objets()
        self.layout()

    def objets(self):
        """Define visual objets to place in GUI."""
        self.filePath = QLineEdit('/home/fabouzz/Cours/Projet_CMI_bille/mesuresBille/test_cam6')
        self.load = QPushButton("Load")
        self.load.clicked.connect(self.Load)

        self.addNeg = QPushButton('Add neg frames')
        self.addNeg.clicked.connect(self.addNegSample)
        self.negSlice = QLineEdit()

        self.addPos = QPushButton('Add pos frames')
        self.posSlice = QLineEdit()

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

        MainLayout.addLayout(LoadLayout)
        # MainLayout.addLayout(NegLayout)
        MainLayout.addLayout(AddLayout)
        MainLayout.addLayout(VidLayout)
        MainLayout.addWidget(self.Slider)
        MainLayout.addWidget(self.statusLabel)
        self.setLayout(MainLayout)

    def sliderUpdate(self):
        """Update the bottom screen slider. Updates data."""
        self.plot(pos=self.Slider.value())
        # print(self.Slider.value())

    def Load(self):
        """."""
        filename = self.filePath.text()
        self.cvVideo = cv2.VideoCapture(filename + '.avi')  # Chargement video
        with open(filename + '.cih') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('Total Frame :'):
                    self.nFrames = int(line.split(' : ')[1])
        self.Slider.setMaximum(self.nFrames)
        self.plot()

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
        filename = path.split('/')[-1]
        cap = cv2.VideoCapture(path + '.avi')
        fgbg = cv2.createBackgroundSubtractorKNN()
        count = int(slice.split(':')[0])
        while count <= int(slice.split(':')[-1]):
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            fgmask = fgbg.apply(gray)
            thresh = cv2.threshold(fgmask, 17, 255, cv2.THRESH_BINARY_INV)[-1]
            cv2.imwrite(self.haarPath + '/neg/{}_{}.png'.format(filename, count), thresh)
            count += 1
        self.statusLabel.clear()
        self.statusLabel.setText('Added {} frames'.format(int(slice.split(':')[-1]) - int(slice.split(':')[0]) + 1))


if __name__ == '__main__':
    if args.create:
        createHaar(args.create)
        app = QApplication(sys.argv)
        clock = GUI()
        clock.show()
        sys.exit(app.exec_())
