from shape_detector import ShapeDetector
<<<<<<< HEAD
<<<<<<< HEAD
from hsv_detection import HSV_Detector
=======
>>>>>>> e1c56d5... python3.6
import cv2
import color_labeler
<<<<<<< HEAD

=======
>>>>>>> 2f2e5fc... fixed square detection. started new colorlaber
def image():
    frame = cv2.imread("../shapes/test2.jpg")
<<<<<<< HEAD

=======
>>>>>>> e1c56d5... python3.6
    shape = ShapeDetector(frame)
    cv2.imshow('imuout', shape.IW.output_image)

   # cv2.imshow('imuout2', shape.IW.imaqge[236:300, 554:618])
    #cl = color_labeler.ColorLabeler(shape.IW.image[236:300, 554:618])
    #print(shape.IW.output_image[580, 227])

    #cv2.imshow('imuout2', shape.IW.image[236:300, 554:618])
    #cl = color_labeler.ColorLabeler(shape.IW.image[236:300, 554:618])
    #print(shape.IW.output_image[580, 227])
=======
import cv2
import copy


def image():
    frame = cv2.imread("../shapes/foto3.jpg")
    shape = ShapeDetector(frame)
    cv2.imshow('imuout', shape.IW.output_image)
<<<<<<< HEAD
>>>>>>> ea1d704... inital algorithm
=======

   # cv2.imshow('imuout2', shape.IW.imaqge[236:300, 554:618])
    #cl = color_labeler.ColorLabeler(shape.IW.image[236:300, 554:618])
    #print(shape.IW.output_image[580, 227])

    #cv2.imshow('imuout2', shape.IW.image[236:300, 554:618])
    #cl = color_labeler.ColorLabeler(shape.IW.image[236:300, 554:618])
    #print(shape.IW.output_image[580, 227])
>>>>>>> 2f2e5fc... fixed square detection. started new colorlaber
    cv2.imshow('imedged', shape.IW.edged)
    cv2.waitKey(0)
    pass


def video():
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

    cap = cv2.VideoCapture('../shapes/biale_przejazd_z_znacznikami.avi')

=======
    cap = cv2.VideoCapture('../shapes/video3.mp4')
    frame_width = cap.get(3)
    frame_height = cap.get(4)
>>>>>>> ea1d704... inital algorithm
=======
    cap = cv2.VideoCapture('../shapes/video1.mp4')
>>>>>>> e1c56d5... python3.6
=======
    cap = cv2.VideoCapture('../shapes/biale_przejazd_z_znacznikami.avi')
>>>>>>> 2f2e5fc... fixed square detection. started new colorlaber
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        shape = ShapeDetector(frame)
<<<<<<< HEAD
        cv2.imshow('frameOUT', shape.IW.output_image)
        cv2.imshow('frameedged', shape.IW.edged)
        #print("frame" + str(cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)))
=======
        #cv2.imshow('framIN', shape.IW.image)
        cv2.imshow('frameOUT', shape.IW.output_image)
        cv2.imshow('frameedged', shape.IW.edged)
<<<<<<< HEAD
        print "frame" + str(cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES))
>>>>>>> ea1d704... inital algorithm
=======
        #print("frame" + str(cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)))
>>>>>>> e1c56d5... python3.6
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> e1c56d5... python3.6

        cv2.imshow('original webcam', shape.IW.image)
        cv2.imshow('processed image', shape.IW.output_image)
        cv2.imshow('frameedged', shape.IW.edged)
=======
        cv2.imshow('original webcam', shape.IW.image)
        cv2.imshow('processed image', shape.IW.output_image)
>>>>>>> ea1d704... inital algorithm
        if cv2.waitKey(1) == 27:  #esc
            break
    cv2.destroyAllWindows()
    pass


def main():
<<<<<<< HEAD
<<<<<<< HEAD
    #image()
<<<<<<< HEAD
    video()
    #web_cam()
=======
    #video()
    web_cam()
>>>>>>> ea1d704... inital algorithm
=======
    image()
    #video()
   #web_cam()
>>>>>>> e1c56d5... python3.6
=======
    #image()
    video()
    #web_cam()
>>>>>>> 2f2e5fc... fixed square detection. started new colorlaber
    pass


if __name__ == "__main__":
    main()