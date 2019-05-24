import cv2 as cv
from BubbleDetection import *
import matplotlib.pyplot as plt 

datapath = "/media/mathieu/EHDD/videos_bille/"
filename = "mes_haut4_bille3_1.avi"
# filename = 'mes_haut3_bille3_1.avi'
video = Bubble(datapath, filename, beginFrame=500)
f, t, t1 = video.Trajectory()

plt.figure()
tp.mass_size(t1.groupby('particle').mean()); # convenience function -- just plots size vs. mass