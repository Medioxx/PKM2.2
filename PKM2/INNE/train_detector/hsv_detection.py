import cv2
import imutils
import numpy as np
from wrappers import ImageWrapper, ContourWrapper
import graphics_utils

redLower = (110, 50, 50)
redUpper = (130, 255, 255)
import time
#RED_imgThreshLow = cv2.inRange(imgHSV, np.array([0, 100, 10]), np.array([19, 255, 255]))
#RED_imgThreshHigh = cv2.inRange(imgHSV, np.array([168, 100, 100]), np.array([179, 255, 255]))

#GREEN
# mask = cv2.inRange(imgHSV, np.array([29, 86, 6]), np.array([64, 255, 255]))



class HSV_Detector:
    def __init__(self, image, color="green"):
        (self.redLower, self.redUpper) = ((110, 50, 50), (130, 255, 255))
        (self.greenLower, self.greenUpper) = ((29, 86, 6), (64, 255, 255))
        self.IW = ImageWrapper(image)
        self.color = color
        self.mask = self.__prepare_mask()
        self.run()
        pass

    def __prepare_mask(self):
        if self.color == "green":
            mask = cv2.inRange(self.IW.hsv, np.array([29, 86, 6]), np.array([64, 255, 255]))
        elif self.color == "red":
            mask = cv2.inRange(self.IW.hsv, np.array([29, 86, 6]), np.array([64, 255, 255]))
        else:
            raise 'set red or green color'
        mask = cv2.erode(mask, np.ones((6, 6)), iterations=2)
        mask = cv2.dilate(mask, np.ones((5, 5)), iterations=2)
        return mask

    def run(self):
        cnts = cv2.findContours(self.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            CW = ContourWrapper(c)
            # ((x, y), radius) = cv2.minEnclosingCircle(c)
            # M = cv2.moments(c)
            # center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            print len(CW.approx)
            if CW.radius > 10 and 4 <= len(CW.approx) <=7:
                graphics_utils.draw_contour(self.IW.output_image, CW.approx)
                graphics_utils.draw_circle(self.IW.output_image, CW)

    def return_mask(self):
        return self.mask

# camera = cv2.VideoCapture(0)
# counter = 0
# frame_step = 1
# print cv2.__version__
# #cap = cv2.VideoCapture('../shapes/video5.mp4')
# #while cap.isOpened():
#     #time.sleep(0.15)
#     #ret, frame = cap.read()
#
#     #if not ret:
#         #break
# while True:
#     counter += 1
#
#     (grabbed, frame) = camera.read()
#
#
#     frame = imutils.resize(frame, width=600)
#     blurred = cv2.GaussianBlur(frame, (11, 11), 0)
#     imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#
#     mask = cv2.inRange(imgHSV, np.array([29, 86, 6]), np.array([64, 255, 255]))
#     mask = cv2.erode(mask, np.ones((6, 6)), iterations=2)
#     mask = cv2.dilate(mask, np.ones((5, 5)), iterations=2)
#
#
#
#
#     cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
#     center = None
#
#     # if len(cnts) > 1 and counter % frame_step == 0:
#     #     c = sorted(cnts, key=cv2.contourArea, reverse=True)
#     #     c1 = c[0]
#     #     c2 = c[1]
#     #     print str(cv2.contourArea(c[0])) + " " + str(cv2.contourArea(c[1]))
#     #
#     #
#     #     area_ratio = cv2.contourArea(c[0])/cv2.contourArea(c[1])
#     #     print "area ratio: "+ str(area_ratio)
#     #     ((x1, y1), radius1) = cv2.minEnclosingCircle(c1)
#     #     M1 = cv2.moments(c1)
#     #     center = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))
#     #     if radius1 > 10:
#     #         cv2.circle(frame, (int(x1), int(y1)), int(radius1), (0, 255, 255), 2)
#     #         cv2.circle(frame, center, 5, (0, 0, 255), -1)
#     #
#     #     ((x2, y2), radius2) = cv2.minEnclosingCircle(c2)
#     #     M2 = cv2.moments(c2)
#     #
#     #     x_ratio = x2 / x1
#     #     y_ratio = y2 / y1
#     #
#     #
#     #     print "x ratio: " + str(x_ratio) + "y_ratio: " + str(y_ratio)
#     #
#     #
#     #     center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))
#     #     if radius2 > 10:
#     #         cv2.circle(frame, (int(x2), int(y2)), int(radius2), (0, 255, 255), 2)
#     #         cv2.circle(frame, center2, 5, (0, 0, 255), -1)
#     #
#     #
#     #     print counter
#     #
#     #     key = cv2.waitKey(1) & 0xFF
#     #     cv2.imshow("mask", mask)
#     #     cv2.imshow("org", frame)
#     #     if key == ord("q"):
#     #         break
#
# #ONE MAX GREEN AREA
#     if len(cnts) > 0:
#         c = max(cnts, key=cv2.contourArea)
#         ((x, y), radius) = cv2.minEnclosingCircle(c)
#         M = cv2.moments(c)
#         center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
#
#         print "x: " + str(x) + "y: " + str(y) +  "radius " + str(x)
#
#         if radius > 10:
#             cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
#             cv2.circle(frame, center, 5, (0, 0, 255), -1)
#
#     key = cv2.waitKey(1) & 0xFF
#     cv2.imshow("mask", mask)
#     cv2.imshow("org", frame)
#     if key == ord("q"):
#         break
