import os, errno
import cv2
from marker_detector import ShapeDetector

class frames_saver:
    def __init__(self):
        self.prefix    = "train_data/"
        self.negative  = "negative_data"
        self.train1    = "train_1_data"
        self.train2    = "train_2_data"
        self.train6    = "train_6_data"
        self.depot     = "zajezdnia_data"
        self.kielpinek = "kieplinek_data"
        self.strzyza   = "strzyza_data"
        self.frames_latch = 10

    def __create_dir(self, name):

        try:
            os.makedirs(self.prefix + name)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def __save_frame(self, folder_name, movie_id, frame_number, frame):
        cv2.imwrite(self.prefix + folder_name + "/" + movie_id +  "_frame%d.jpg" % frame_number, frame)

    def create_dirs(self):
        self.__create_dir(self.negative)
        self.__create_dir(self.train1)
        self.__create_dir(self.train2)
        self.__create_dir(self.train6)
        self.__create_dir(self.depot)
        self.__create_dir(self.kielpinek)
        self.__create_dir(self.strzyza)
        pass

    def __parse_dicts(self, dict__arr, movie_id, frame_number, frame):
        output = False
        train_nr = 0
        platform_name = None
        for elem in dict__arr:
            if train_nr == 0:
                train_nr = elem["train"]
            if platform_name is None:
                platform_name = elem["platform"]

        if train_nr == 0 and platform_name is None:
            self.__save_frame(self.negative, movie_id, frame_number, frame)
            output = False

        if train_nr == 1:
            self.__save_frame(self.train1, movie_id, frame_number, frame)
            output = True
        if train_nr == 2:
            self.__save_frame(self.train2, movie_id, frame_number, frame)
            output = True
        if train_nr == 6:
            self.__save_frame(self.train6, movie_id, frame_number, frame)
            output = True
        if platform_name == "kieplinek":
            self.__save_frame(self.kielpinek, movie_id, frame_number, frame)
            output = True
        if platform_name == "strzyza":
            self.__save_frame(self.strzyza, movie_id, frame_number, frame)
            output = True
        if platform_name == "zajezdnia":
            self.__save_frame(self.depot, movie_id, frame_number, frame)
            output = True
        return output

    def parse_video(self, path_to_movie, movie_id):
        cap = cv2.VideoCapture(path_to_movie) #'../shapes/z_pocigami_2.avi'
        frame_counter = 0;
        detected = False
        detected_frame = 0
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            frame_counter += 1
            shape = ShapeDetector(frame)
            if detected is False:
                out1 = shape.detect_depot()
                out2 = shape.detect_trains()
                out3 = shape.detect_platforms()
                dicts_arr = [out1, out2, out3]
                detected_frame = frame_counter
            elif detected is True:
                if detected_frame + self.frames_latch <= frame_counter:
                    detected = False
                    continue
            detected = self.__parse_dicts(dicts_arr, str(movie_id), frame_counter, frame)

            cv2.imshow('frameOUT', shape.IW.output_image)
            cv2.imshow('frameOUT2', shape.IW.edged)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        pass



def main():
    saver = frames_saver()
    saver.create_dirs()
    saver.parse_video('../shapes/bez_pociagow.avi', 0)
    saver.parse_video('../shapes/pociagi_rozne_miejsca.avi', 1)
    saver.parse_video('../shapes/pociagi_rozne_miejsca_2', 2)
    saver.parse_video('../shapes/pociagi_rozne_miejsca_3.avi', 3)
    saver.parse_video('../shapes/z_pociagami_1.avi', 4)
    saver.parse_video('../shapes/z_pocigami_2.avi',  5)
    pass


if __name__ == "__main__":
    main()