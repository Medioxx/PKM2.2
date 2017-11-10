import cv2
from wrappers import ImageWrapper, ContourWrapper
import graphics_utils
import numpy as np
import imutils

square_str = "square"
triangle_str = "triangle"


class Shape:
    def __init__(self, type="", color="", area=0, center_x=0, center_y=0, x=0, y=0, w=0, h=0):
        self.type = type
        self.color = color
        self.area = area
        self.centerX = center_x
        self.centerY = center_y
        (self.x, self.y, self.w, self.h) = (x, y, w, h)
        pass

    def __if_type(self, type1, type2):
        return type1 == type2

    def __if_color(self, color1, color2):
        return color1 == color2

    def set_color(self, color):
        self.color = color
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

    def is_red(self):
        if self.__if_color(self.color, "red"):
            return True
        return False

    def is_blue(self):
        if self.__if_color(self.color, "blue"):
            return True
        return False

    def is_green(self):
        if self.__if_color(self.color, "green"):
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
        self.run()
        pass

    def run(self):
        self.detected = False
        array_of_contours = []
        #Next, Previous, First_Child, Parent]
        for c in self.IW.contours_shape():

            CW = ContourWrapper(c)
            self.shape.set_type(len(CW.approx))
            self.shape.area = CW.area
            if self.shape.is_square():
                if self.shape.is_area_higer_than(500):
                    #cv2.drawContours(self.IW.output_image, [CW.approx], -1, (0, 255, 255), 4)
                    array_of_contours = self.add_cw_to_similarity_array(array_of_contours, CW)
                    #self.shape.set_color(CW.get_color(self.IW.lab))
                    #if self.shape.is_blue():

            if self.shape.is_triangle():
                if self.shape.is_area_higer_than(300):
                    array_of_contours = self.add_cw_to_similarity_array(array_of_contours, CW)
                    #cv2.drawContours(self.IW.output_image, [CW.approx], -1, (0, 255, 255), 4)
                    #graphics_utils.draw_contour(self.IW.output_image, CW.approx)

        #for cont in array_of_contours:
            #print(str(cont.cX) + ", " + str(cont.cX) + ", " + str(cont.area))


        #POTEM TU ZMIENIC, NARAZIE TESTOWO W TAKI BRZYDKI SPOSOB
        # shape a jest wiekszy od shape b, czyli b to figury z ktorej bedzie wyciagany kolor
        if len(array_of_contours) >= 2:
            #check squres
            a, b = self.check_cws_array_ratios(array_of_contours, 4.5, 0.5)
            if a is None and b is None:
                pass
            else:
                #print("podejrzane kontury: " + str(a.area) + ", " + str(b.area))
                #print("cX_1: " + str(a.cX) + ", cY_1: " + str(a.cY))
                #print("cX_2: " + str(b.cX) + ", cY_2: " + str(b.cY))
                self.shape.set_center(b.cX, b.cY)
                self.shape.set_size(b.x, b.y, b.w, b.h)
                graphics_utils.draw_contour(self.IW.output_image, a.approx)
                graphics_utils.draw_contour(self.IW.output_image, b.approx)
                graphics_utils.draw_crosshair(self.IW.output_image, self.shape)
                print("wykryto pociag + (kolor)")

            #check triangles
            a, b = self.check_cws_array_ratios(array_of_contours, 8.5, 0.5)
            if a is None and b is None:
                pass
            else:
                #print("podejrzane kontury: " + str(a.area) + ", " + str(b.area))
                #print("cX_1: " + str(a.cX) + ", cY_1: " + str(a.cY))
                #print("cX_2: " + str(b.cX) + ", cY_2: " + str(b.cY))
                self.shape.set_center(b.cX, b.cY)
                self.shape.set_size(b.x, b.y, b.w, b.h)
                graphics_utils.draw_contour(self.IW.output_image, a.approx)
                graphics_utils.draw_contour(self.IW.output_image, b.approx)
                graphics_utils.draw_crosshair(self.IW.output_image, self.shape)
                print("wykryto zajezednie + (kolor)")
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
                        #print("abs ratio" + str(abs(ratio-expected_ratio)))
                        return cnts_array[i], cnts_array[j]
        return None, None

    def check_similarity_of_two_cw(self, cw_1, cw_2):
        err = 50
        if abs(cw_1.cX - cw_2.cX) <= err:
            if abs(cw_1.cY - cw_2.cY) <= err:
                return True
        return False

    def temp_is_red(self, mean):
        if mean[2] > 100 and mean[1] < 100 and mean[0] < 100:
            return True
        return False
# hullArea = cv2.contourArea(cv2.convexHull(c))
# solidity = self.shape.area / float(hullArea)
# print solidity
# aspectRatio = self.shape.w / float(self.shape.h)
# print aspectRatio
