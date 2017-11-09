import cv2


def draw_crosshair(image, shape):
    (startX, endX) = (int(shape.centerX - (shape.w * 0.15)), int(shape.centerX + (shape.w * 0.15)))
    (startY, endY) = (int(shape.centerY - (shape.h * 0.15)), int(shape.centerY + (shape.h * 0.15)))
    cv2.line(image, (startX, shape.centerY), (endX, shape.centerY), (0, 0, 255), 3)
    cv2.line(image, (shape.centerX, startY), (shape.centerX, endY), (0, 0, 255), 3)
    pass


def draw_contour(image, approx):
    cv2.drawContours(image, [approx], -1, (0, 255, 255), 4)
    pass
