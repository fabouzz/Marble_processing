import cv2
import numpy as np
from matplotlib import pyplot as plt
# Read image
I = cv2.imread('../images/screen_bulles.png', 0)
I = I[400:620, 320:540]
# Threshold
IThresh = (I >= 118).astype(np.uint8)*255

# Remove from the image the biggest conneced componnet

# Find the area of each connected component
connectedComponentProps = cv2.connectedComponentsWithStats(IThresh, 8, cv2.CV_32S)
# print(connectedComponentProps)
IThreshOnlyInsideDrops = np.zeros_like(connectedComponentProps[1])
IThreshOnlyInsideDrops = connectedComponentProps[1]
stat = connectedComponentProps[2]
maxArea = 0
for label in range(connectedComponentProps[0]):
    cc = stat[label, :]
    if cc[cv2.CC_STAT_AREA] > maxArea:
        maxArea = cc[cv2.CC_STAT_AREA]
        maxIndex = label
        # print(maxIndex)

# Convert the background value to the foreground value
for label in range(connectedComponentProps[0]):
    cc = stat[label,:]
    if cc[cv2.CC_STAT_AREA] == maxArea:
        IThreshOnlyInsideDrops[IThreshOnlyInsideDrops==label] = 0
    else:
        IThreshOnlyInsideDrops[IThreshOnlyInsideDrops == label] = 255

# Fill in all the IThreshOnlyInsideDrops as 0 in original IThresh
IThreshFill = IThresh
IThreshFill[IThreshOnlyInsideDrops==255] = 0
IThreshFill = np.logical_not(IThreshFill/255).astype(np.uint8)*255

# Get numberof drops and cover precntage
connectedComponentPropsFinal = cv2.connectedComponentsWithStats(IThreshFill, 8, cv2.CV_32S)
NumberOfDrops = connectedComponentPropsFinal[0]

print("Number of drops = " + str(NumberOfDrops))


cv2.imshow("original", I)
cv2.imshow("treated", IThreshFill)
cv2.waitKey(0)
# Print
