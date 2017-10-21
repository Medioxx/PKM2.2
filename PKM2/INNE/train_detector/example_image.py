from shape_detector import ShapeDetector
import cv2
import copy


def image():
    frame = cv2.imread("../shapes/foto3.jpg")
    shape = ShapeDetector(frame)
    cv2.imshow('imuout', shape.IW.output_image)
    cv2.imshow('imedged', shape.IW.edged)
    cv2.waitKey(0)
    pass


def video():
    cap = cv2.VideoCapture('../shapes/video3.mp4')
    frame_width = cap.get(3)
    frame_height = cap.get(4)
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        shape = ShapeDetector(frame)
        #cv2.imshow('framIN', shape.IW.image)
        cv2.imshow('frameOUT', shape.IW.output_image)
        cv2.imshow('frameedged', shape.IW.edged)
        print "frame" + str(cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    pass


def web_cam():
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        shape = ShapeDetector(frame)
        cv2.imshow('original webcam', shape.IW.image)
        cv2.imshow('processed image', shape.IW.output_image)
        if cv2.waitKey(1) == 27:  #esc
            break
    cv2.destroyAllWindows()
    pass


def main():
    #image()
    #video()
    web_cam()
    pass


if __name__ == "__main__":
    main()