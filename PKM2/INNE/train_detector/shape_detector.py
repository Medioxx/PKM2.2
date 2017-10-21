import cv2
from wrappers import ImageWrapper, ContourWrapper
import graphics_utils
import numpy as np

square_str = "square"
triangle_str = "triangle"


class Shape:
    def __init__(self, type="", color="", area=0, center_x=0, center_y=0, (x, y, w, h)=(0, 0, 0, 0)):
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

    def set_size(self, (x, y, w, h)):
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

        for c in self.IW.contours_shape():
            CW = ContourWrapper(c)
            if self.is_similiar_to_previous_shape(CW):
                continue
            self.shape.set_type(len(CW.approx))
            self.shape.area = CW.area
            if self.shape.is_square():
                if self.shape.is_area_higer_than(1000):
                    self.shape.set_color(CW.get_color(self.IW.lab))
                    #if self.shape.is_blue():
                    self.detected = True
                    self.shape.set_center(CW.cX, CW.cY)
                    self.shape.set_size((CW.x, CW.y, CW.w, CW.h))

                    print self.shape
                    print CW.CL.mean
                    self.check_possible_shapes()

                    graphics_utils.draw_contour(self.IW.output_image, CW.approx)
                    graphics_utils.draw_crosshair(self.IW.output_image, self.shape)



        graphics_utils.draw_status(self.IW.output_image, self.shape, self.detected)

        pass

    def check_possible_shapes(self):
        crop_img = self.IW.image[self.shape.y:(self.shape.y + self.shape.h), self.shape.x:(self.shape.x + self.shape.w)]
        temp_IW = ImageWrapper(crop_img)

        mean = cv2.mean(temp_IW.image)[:3]
        print mean
        # if self.temp_is_red(mean):
        #     cv2.imshow('frame1', temp_IW.output_image)
        #     cv2.imshow('frame2', temp_IW.lab)
        #     cv2.imshow('frameedged2', temp_IW.edged)
        #     graphics_utils.draw_contour(temp_IW.output_image, CW.approx)
        #     cv2.waitKey(0)

        # for c in temp_IW.contours_shape():
        #     CW = ContourWrapper(c)
        #     self.shape.set_type(len(CW.approx))
        #     self.shape.area = CW.area
        #     graphics_utils.draw_contour(temp_IW.output_image, CW.approx)
        #
        pass

    def is_similiar_to_previous_shape(self, contour_wrapper):
        checks = []
        if abs(self.shape.area - contour_wrapper.area) < 50:
            checks.append(True)
        if abs(self.shape.x - contour_wrapper.x) < 20 and abs(self.shape.w - contour_wrapper.w) < 20:
            checks.append(True)
        if abs(self.shape.y - contour_wrapper.y) < 20 and abs(self.shape.y - contour_wrapper.y) < 20:
            checks.append(True)
        if checks.count(True) >= 2:
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
