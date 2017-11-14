import numpy as np
import cv2
import imutils
from imutils import contours
import math
import copy


class ColorLabel:
    def __init__(self, area, w, h):
        self.area = area
        (self.width, self.height) = (w, h)
        self.bgr = [0, 0, 0]
        pass

    def label(self):
            return self.__label_square()

    def __label_square(self):
        for y in range(self.height):
            for x in range(self.width):
                self.__update_bgr(self.__max_channel(self.area[y, x]))
        return self.__color()

    def __color(self):
        index = np.argmax(self.bgr)
        if index == 0:
            return "purple"
        if index == 1:
            return "green"
        if index == 2:
            return "red"

    def __update_bgr(self, index):
        self.bgr[index] += 1
        pass

    def __max_channel(self, pixel):
        index = np.argmax(pixel)
        return index


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
        self.bounding_rect = (self.y, self.x, self.w, self.h)
        ((self.x_mnc, self.y_mnc), self.radius) = cv2.minEnclosingCircle(contour)
        self.area = cv2.contourArea(self.contour)
        # cX and cY are center of mass of contour
        self.cX, self.cY = self.__get_cx_cy()

    def __get_cx_cy(self):
        cx = 0
        cy = 0
        if self.M["m00"] > 0:
            cx = int((self.M["m10"] / self.M["m00"]) * self.ratio)
            cy = int((self.M["m01"] / self.M["m00"]) * self.ratio)
        return cx, cy


class GraphicsUtils:
    def __init__(self):
        pass

    def draw_station_status(self, image, text):
        string = "Station: " + text
        cv2.putText(image, string, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        pass

    def draw_train_status(self, image, idx):
        string = "Train: " + str(idx)
        cv2.putText(image, string, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        pass

    def draw_crosshair(self, image, shape):
        (startX, endX) = (int(shape.centerX - (shape.w * 0.15)), int(shape.centerX + (shape.w * 0.15)))
        (startY, endY) = (int(shape.centerY - (shape.h * 0.15)), int(shape.centerY + (shape.h * 0.15)))
        cv2.line(image, (startX, shape.centerY), (endX, shape.centerY), (0, 0, 255), 3)
        cv2.line(image, (shape.centerX, startY), (shape.centerX, endY), (0, 0, 255), 3)
        pass

    def draw_contour(self, image, approx):
        cv2.drawContours(image, [approx], -1, (0, 255, 255), 4)
        pass


square_str = "square"
triangle_str = "triangle"


class Shape:
    def __init__(self, type="", area=0, center_x=0, center_y=0, x=0, y=0, w=0, h=0):
        self.type = type
        self.contour = None
        self.area = area
        self.centerX = center_x
        self.centerY = center_y
        (self.x, self.y, self.w, self.h) = (x, y, w, h)
        pass

    def __if_type(self, type1, type2):
        return type1 == type2

    def set_contour(self, contour):
        self.contour = contour
        pass

    def set_center(self, c_x, c_y):
        self.centerX = c_x
        self.centerY = c_y

    def set_type(self, approx):
        if 4 <= approx <= 4:
            self.type = square_str
        elif approx == 3:
            self.type = triangle_str
        else:
            self.type = "unknown"
        pass

    def set_size(self, x, y, w, h):
        (self.x, self.y, self.w, self.h) = (x, y, w, h)
        pass

    def is_square(self):
        if self.__if_type(self.type, square_str):
            return True
        return False

    def is_triangle(self):
        if self.__if_type(self.type, triangle_str):
            return True
        return False

    def is_area_higer_than(self, value):
        return self.area >= value

    def is_area_lower_than(self, value):
        return self.area <= value

    def __str__(self):
        str = "Type: %s, color: %s, area: %d, center(x,y): %d, %d, size(x,y,w,h): %d, %d, %d, %d" % (self.type, self.color, self.area, self.centerX, self.centerY, self.x, self.y, self.w, self.h)
        return str


class ShapeDetector:
    def __init__(self, image):
        self.IW = ImageWrapper(image)
        self.shape = Shape()
        self.detected = False
        self.stations = {'red': 'zajezdnia', 'green': 'strzyza', 'purple': 'kieplinek'}
        self.trains = {'red': 6, 'green': 2, 'purple': 1}
        pass

    def detect_trains(self):
        self.__detect(trains=True)
        pass

    def detect_platforms(self):
        self.__detect(platforms=True)
        pass

    def detect_depot(self):
        self.__detect(depot=True)
        pass

    def __detect(self, platforms=False, depot=False, trains=False):
        self.detected = False
        array_of_contours = []
        GU = GraphicsUtils()
        for c in self.IW.contours_shape():
            CW = ContourWrapper(c)
            self.shape.set_type(len(CW.approx))
            self.shape.area = CW.area
            self.shape.set_contour(CW.contour)
            if self.shape.is_square():
                if self.shape.is_area_higer_than(500):
                    array_of_contours = self.add_cw_to_similarity_array(array_of_contours, CW)

            if self.shape.is_triangle():
                if self.shape.is_area_higer_than(300):
                    array_of_contours = self.add_cw_to_similarity_array(array_of_contours, CW)

        if len(array_of_contours) >= 2:
            if trains is True:
                #check squres
                a, b = self.check_cws_array_ratios(array_of_contours, 4.5, 0.5)
                if a is None and b is None:
                    pass
                else:
                    self.shape.set_center(b.cX, b.cY)
                    self.shape.set_size(b.x, b.y, b.w, b.h)
                    GU.draw_contour(self.IW.output_image, a.approx)
                    GU.draw_contour(self.IW.output_image, b.approx)
                    GU.draw_crosshair(self.IW.output_image, self.shape)
                    cl2 = ColorLabel(self.IW.image[b.y:b.y + b.h, b.x:b.x + b.w], b.w, b.h)
                    color2 = cl2.label()
                    GU.draw_train_status(self.IW.output_image, str(self.trains[color2]) + ", " + color2)

            if platforms is True or depot is True:
                #check triangles
                a, b = self.check_cws_array_ratios(array_of_contours, 8.5, 0.5)
                if a is None and b is None:
                    pass
                else:
                    self.shape.set_center(b.cX, b.cY)
                    self.shape.set_size(b.x, b.y, b.w, b.h)
                    cl2 = ColorLabel(self.IW.image[b.y:b.y + b.h, b.x:b.x + b.w], b.w, b.h)
                    color2 = cl2.label()
                    if platforms is True:
                        if color2 is "green" or color2 is "purple":
                            GU.draw_station_status(self.IW.output_image, self.stations[color2] + ", " + color2)
                            GU.draw_contour(self.IW.output_image, a.approx)
                            GU.draw_contour(self.IW.output_image, b.approx)
                            GU.draw_crosshair(self.IW.output_image, self.shape)
                    if depot is True:
                        if color2 is "red":
                            GU.draw_station_status(self.IW.output_image, self.stations[color2] + ", " + color2)
                            GU.draw_contour(self.IW.output_image, a.approx)
                            GU.draw_contour(self.IW.output_image, b.approx)
                            GU.draw_crosshair(self.IW.output_image, self.shape)
        pass

    def add_cw_to_similarity_array(self, cnts_array, CW):
        for cnt in cnts_array:
            if cnt.cX == CW.cX and cnt.cY == CW.cY:
                if 0.95 <= (cnt.area/CW.area) <= 1.05:
                    return cnts_array
        cnts_array.append(CW)
        return cnts_array

    def check_cws_array_ratios(self, cnts_array, exp_ratio, error):
        expected_ratio = exp_ratio
        err = error
        ratio = 0
        for i in range(0, len(cnts_array)):
            for j in range(0, len(cnts_array)):
                if cnts_array[j].area != 0:
                    ratio = cnts_array[i].area / cnts_array[j].area
                    if abs(ratio-expected_ratio) <= err and self.check_similarity_of_two_cw(cnts_array[i], cnts_array[j]):
                        return cnts_array[i], cnts_array[j]
        return None, None

    def check_similarity_of_two_cw(self, cw_1, cw_2):
        err = 50
        if abs(cw_1.cX - cw_2.cX) <= err:
            if abs(cw_1.cY - cw_2.cY) <= err:
                return True
        return False



##################################################################
##################################################################
##################################################################
#EXAMPLE OF USAGE BELOW, DELETE WHILE INTERGRATING WITH WHOLE PROJECT

def video():
    cap = cv2.VideoCapture('../shapes/biale_przejazd_z_znacznikami.avi')#('../shapes/biale_przejazd_bez_pociagow.avi')#('../shapes/biale_przejazd_z_znacznikami.avi')
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break


        #example of usage
        shape = ShapeDetector(frame)
        shape.detect_depot()
        #shape.detect_trains()
        shape.detect_platforms()



        cv2.imshow('frameOUT', shape.IW.output_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    pass


def main():
    video()
    pass

if __name__ == "__main__":
    main()