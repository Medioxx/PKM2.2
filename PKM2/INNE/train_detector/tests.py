import cv2
from wrappers import ImageWrapper, ContourWrapper
import numpy as np


# use to dump image to files for further tests
def dump_to_file(frame):
    image_wrapper = ImageWrapper(frame)
    image_wrapper.image.dump("test_data/test_image.txt")
    image_wrapper.edged.dump("test_data/test_edged.txt")
    image_wrapper.thresh.dump("test_data/test_thresh.txt")
    pass


def is_similar(image1, image2):
    return image1.shape == image2.shape and not(np.bitwise_xor(image1,image2).any())


def test_image_wrapper(frame):
    image_wrapper = ImageWrapper(frame)
    test_image = np.load("test_data/test_image.txt")
    test_edged = np.load("test_data/test_edged.txt")
    test_thresh = np.load("test_data/test_thresh.txt")
    return is_similar(test_image, image_wrapper.image) and is_similar(test_edged, image_wrapper.edged) and is_similar(test_thresh, image_wrapper.thresh)


def test_contour_wrapper(frame):
    test_contours = open("test_data/test_contours.txt", "r").read()
    test_str = ""
    image_wrapper = ImageWrapper(frame)
    for c in image_wrapper.contours_shape():
        contour_wrapper = ContourWrapper(c)
        if 4 <= len(contour_wrapper.approx) <= 5:
            if contour_wrapper.area > 1000:
                test_str += "area:" + str(contour_wrapper.area) + ", position: " + str((contour_wrapper.x, contour_wrapper.y, contour_wrapper.w, contour_wrapper.h))
    if test_contours == test_str:
        return True
    return False


def test(frame):
    test_1 = test_image_wrapper(frame)
    if test_1 is False:
        return "Test 1 failed"
    test_2 = test_contour_wrapper(frame)
    if test_2 is False:
        return "Test 2 failed"
    return "All tests passed."


def main():
    frame = cv2.imread("../shapes/foto1.jpg")
    choice = raw_input("Dump or test?")
    if choice == "dump":
        print(dump_to_file(frame))
    else:
        print(test(frame))
    pass


if __name__ == "__main__":
    main()
