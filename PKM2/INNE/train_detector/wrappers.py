import cv2
from imutils import contours

from color_labeler import ColorLabeler
import imutils
import copy


class ImageWrapper:
    def __init__(self, image, ratio=1):
        self.image = image
        self.output_image = copy.deepcopy(image)
        self.ratio = ratio
        self.height, self.width = self.image.shape[:2]
        self.resized = cv2.resize(self.image, (int(self.height * ratio), int(self.width * ratio)))
        self.blurred = cv2.GaussianBlur(self.image, (5, 5), 0)
        self.hsv = cv2.cvtColor(cv2.GaussianBlur(self.image, (11, 11), 0), cv2.COLOR_BGR2HSV)
        self.gray = cv2.cvtColor(self.blurred, cv2.COLOR_BGR2GRAY)
        self.edged = cv2.Canny(self.blurred, 50, 150)
        self.lab = cv2.cvtColor(self.blurred, cv2.COLOR_BGR2LAB)
        self.thresh = cv2.threshold(self.gray, 60, 255, cv2.THRESH_BINARY)[1]
        self.cnts = None


    def __contours(self, image):
        self.cnts = cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.cnts = self.cnts[0] if imutils.is_cv2() else self.cnts[1]

    def contours_shape(self):
        self.__contours(self.edged)
        return self.cnts

    def contours_color(self):
        self.__contours(self.thresh)
        return self.cnts


class ContourWrapper:
    def __init__(self, contour, ratio=1):
        self.contour = contour
        self.ratio = ratio
        self.peri = cv2.arcLength(self.contour, True)
        self.approx = cv2.approxPolyDP(self.contour, 0.04 * self.peri, True)
        self.M = cv2.moments(self.contour)
        (self.x, self.y, self.w, self.h) = cv2.boundingRect(self.approx)
        self.bounding_rect = (self.x, self.y, self.w, self.h)
        ((self.x_mnc, self.y_mnc), self.radius) = cv2.minEnclosingCircle(contour)
        self.area = cv2.contourArea(self.contour)
        # cX and cY are center of mass of contour
        self.cX, self.cY = self.__get_cx_cy()

    def __get_cx_cy(self):
        cx = 0
        cy = 0
        if self.M["m00"] > 0:
            cx = int((self.M["m10"] / self.M["m00"]) * self.ratio)  # TODO CHECK IF THIS WORKS
            cy = int((self.M["m01"] / self.M["m00"]) * self.ratio)  # TODO CHECK IF THIS WORKS
        return cx, cy
