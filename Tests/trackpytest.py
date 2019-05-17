"""
Testing the trackpy library
"""
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pims
import trackpy as tp

datapath = "Tests/"
filename = "screen_bulles.png"

def crop(img):
    """
    Crop the image to select the region of interest
    """
    x_min = 330
    x_max = 700
    y_min = 440
    y_max = 672
    return img[y_min:y_max,x_min:x_max]

rawframes = pims.ImageSequence(datapath + filename)



