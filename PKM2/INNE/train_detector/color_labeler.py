import numpy as np
import cv2
import imutils

class ColorLabeler:
    def __init__(self, area):
        self.area = area
        self.mean = cv2.mean(self.area)
        self.sum = cv2.sumElems(self.area)
        print("MEAN!: " + str(self.mean))
        print("SUM!: " + str(self.sum))
        pass
