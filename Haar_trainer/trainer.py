#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import argparse
import frame_visualiser

# Création de la cascade
def createHaar():
    """Create a new haar cascade file."""
    haarName = input('Enter new cascade name : ')
    try:
        currentDir = os.getcwd()
        os.mkdir(currentDir + '/' + haarName)
        os.makedirs(currentDir + '/' + haarName + '/neg')
        os.makedirs(currentDir + '/' + haarName + '/pos')
    except FileExistsError:
        print('This file already exists')




parser = argparse.ArgumentParser()
parser.add_argument('-c', '--create', help='Create a new Haar cascade in current directory.', action='store_true')
parser.add_argument('-m', '--modify', help='Modify an existing Haar cascade.', action='store_true')
args = parser.parse_args()

if args.create:
    createHaar()
elif args.modify:
    modifyHaar()
