#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""
import sys
import cv2
import numpy as np
import getpass
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QDialog, QApplication, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QSlider, QLineEdit, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



class GUI(QDialog):
    """GUI class."""

    def __init__(self):
        """GUI definition."""
        super(GUI, self).__init__()
        self.setWindowTitle("Frame visualiser")
        # self.setGeometry(200, 200, 800, 700)

        self.videoPath = '/home/fabouzz/Cours/Projet_CMI_bille/mesuresBille/'

        self.objets()
        self.layout()

    def objets(self):
        """Define visual objets to place in GUI."""
        self.filename = QLineEdit('test_cam6')
        self.load = QPushButton("Charger")
        self.load.clicked.connect(self.Load)

        # Création des objets figure
        # Figure contenant l'image de la vidéo
        self.figVid = Figure(dpi=100, tight_layout=True)
        self.Canvas = FigureCanvas(self.figVid)
        # Crétion du slider
        # self.toolbarSpec = NavigationToolbar(self.canvasSpec, self)
        self.Slider = QSlider(Qt.Horizontal)
        self.Slider.setMinimum(1)
        self.Slider.setMaximum(100)
        self.Slider.setTickInterval(1)
        self.Slider.setValue(0)
        self.Slider.valueChanged.connect(self.sliderUpdate)

    def layout(self):
        """GUI layout using previous objets."""
        MainLayout = QVBoxLayout()

        TopLayout = QHBoxLayout()
        TopLayout.addWidget(self.load)
        TopLayout.addWidget(self.filename)

        MidLayout = QHBoxLayout()
        MidLayout.addWidget(self.Canvas)

        MainLayout.addLayout(TopLayout)
        MainLayout.addLayout(MidLayout)
        MainLayout.addWidget(self.Slider)
        self.setLayout(MainLayout)

    def sliderUpdate(self):
        """Update the bottom screen slider. Updates data."""
        self.plot(pos=self.Slider.value())
        print(self.Slider.value())

    def Load(self):
        filename = self.filename.text()
        self.cvVideo = cv2.VideoCapture(self.videoPath + filename + '.avi')  # Chargement video
        with open(self.videoPath + filename + '.cih') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('Record Rate(fps) :'):
                    self.fps = int(line.split(' : ')[1])
                if line.startswith('Start Frame :'):
                    self.startFrame = int(line.split(' : ')[1])
                if line.startswith('Total Frame :'):
                    self.nFrames = int(line.split(' : ')[1])
        self.Slider.setMaximum(self.nFrames)
        self.plot()

    def plot(self, pos=0):
        self.cvVideo.set(cv2.CAP_PROP_POS_FRAMES, self.Slider.value())
        ret, self.frame = self.cvVideo.read()
        self.figVid.clear()
        ax = self.figVid.add_subplot(111)
        ax.set_title('Frame n° : ' + str(self.Slider.value()))
        ax.imshow(self.frame)
        ax.set_xticks([])
        ax.set_yticks([])
        self.Canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = GUI()
    clock.show()
    sys.exit(app.exec_())
