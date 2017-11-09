<<<<<<< HEAD
<<<<<<< HEAD
=======
import matplotlib.pyplot as plt
from collections import OrderedDict
>>>>>>> ea1d704... inital algorithm
=======
>>>>>>> 2f2e5fc... fixed square detection. started new colorlaber
import numpy as np
import cv2
import imutils

class ColorLabeler:
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 2f2e5fc... fixed square detection. started new colorlaber
    def __init__(self, area):
        self.area = area
        self.mean = cv2.mean(self.area)
        self.sum = cv2.sumElems(self.area)
        print("MEAN!: " + str(self.mean))
        print("SUM!: " + str(self.sum))
<<<<<<< HEAD
        pass
=======
    def __init__(self):
        colors = OrderedDict({
              "red"    : (255, 0, 0)
            , "green"  : (0, 255, 0)
            , "blue"   : (0, 0, 255)
            , "gray"   : (128, 128, 128)
            , "white"  : (255, 255, 255)
            , "black"  : (0, 0, 0)
        })

        #array self.lab = L*a*b color space
        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
        self.colorNames = []

        for (i, (name, rgb)) in enumerate(colors.items()):
            self.lab[i] = rgb
            self.colorNames.append(name)

        #convert L*a*b array from rgb to lab
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

        self.mask = None
        self.mean = None
        self.minDist = None
        pass

    def label(self, image, c):
        self.mask = np.zeros(image.shape[:2], dtype="uint8")
        #cv2.drawContours(self.mask, [c], -1, 255, -1)
        self.mask = cv2.erode(self.mask, None, iterations=2)
        self.mean = cv2.mean(image, mask=self.mask)[:3]
        self.minDist = (np.inf, None)

        for (i, row) in enumerate(self.lab):
            d = plt.mlab.dist(row[0], self.mean)
            if d < self.minDist[0]:
                self.minDist = (d, i)
        return self.colorNames[self.minDist[1]]
>>>>>>> ea1d704... inital algorithm
=======
        pass
>>>>>>> 2f2e5fc... fixed square detection. started new colorlaber
