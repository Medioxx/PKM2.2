import cv2


def draw_crosshair(image, shape):
    (startX, endX) = (int(shape.centerX - (shape.w * 0.15)), int(shape.centerX + (shape.w * 0.15)))
    (startY, endY) = (int(shape.centerY - (shape.h * 0.15)), int(shape.centerY + (shape.h * 0.15)))
    cv2.line(image, (startX, shape.centerY), (endX, shape.centerY), (0, 0, 255), 3)
    cv2.line(image, (shape.centerX, startY), (shape.centerX, endY), (0, 0, 255), 3)
    pass


def draw_status(image, shape, detected=False):
    if detected:
        cv2.putText(image, "Marker detected", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(image, "cx: " + str(shape.centerX) + ", cy: " + str(shape.centerY), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(image, str(shape.color) + " " + str(shape.type), (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    else:
        cv2.putText(image, "Marker not detected.", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    pass


def draw_contour(image, approx):
    cv2.drawContours(image, [approx], -1, (0, 255, 255), 4)
    pass


def draw_circle(image, countour_wrapper):
    cv2.circle(image, (int(countour_wrapper.x_mnc), int(countour_wrapper.y_mnc)), int(countour_wrapper.radius), (0, 255, 255), 2)
    cv2.circle(image, (countour_wrapper.cX, countour_wrapper.cY), 5, (0, 0, 255), -1)
    pass
