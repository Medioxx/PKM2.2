import cv2
import numpy as np
##################################
# 1.wykrywanie ruchu             #
# 2.wykrywanie zajezdni          #
# 3.wykrywanie peronu            #
# 4.wykrywanie przeszkod         #
# 5.wykrywanie reki              #
# 6.wykrzwanie twarzy            #
# 7.wykrywanie banana            #
##################################
#self.algorithms = {"movement" : "False", "depot" : "False", "station" : "False",
# "obstacles": "False", "hand" : "False", "face" : "False", "banana" : "False"}

class Detection(object):
    # HERE WE ARE MAKING INITIALIZATION OF ALL NECESSARY THINGS (for detection algorithms ofc ;))
    def __init__(self):
        ################### wykrywanie reki ###################
        self.zatrzask = 0
        self.track_window = 0
        self.term_crit = 0
        self.roi_hist = 0
        self.track_window, self.term_crit, self.roi_hist = self.init_hand()
        # FACE INITIALIZATION
        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # BANANA INITIALIZATION
        self.bananaCascade = cv2.CascadeClassifier('banana_classifier.xml')



    def init_hand(self):
        r, a, c, b = 100, 200, 100, 150
        track_window = (r, a, c, b)
        x, y, w, h, = 100, 100, 400, 400
        # !
        frames = cv2.imread('ramka.jpg')
        obrazDloni = frames[y:y + h, x:x + w]
        # Dobor odpowiedniej maski filtrujaca nasza dlon z niepotrzebnych elementow
        dlonHsv = cv2.cvtColor(obrazDloni, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(dlonHsv, np.array((80., 90., 110.)), np.array((190., 160., 255.)))
        mask2 = cv2.inRange(dlonHsv, np.array((0., 98., 90.)), np.array((35., 183., 194.)))
        # Obliczenie histogramu naszej dloni
        roi_hist = cv2.calcHist([dlonHsv], [0, 1], mask, [180, 250], [0, 180, 0, 360])
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        return track_window, term_crit, roi_hist

    def detect_choosen_objects(self,frame,choosenAlgrithms):


        if choosenAlgrithms["movement"] == "True":
            pass
        if choosenAlgrithms["depot"] == "True":
            pass
        if choosenAlgrithms["station"] == "True":
            pass
        if choosenAlgrithms["obstacles"] == "True":
            pass
        if choosenAlgrithms["hand"] == "True":
            #frame, self.track_window, self.term_crit, self.roi_hist = self.detect_hand(frame, self.track_window, self.term_crit, self.roi_hist)
            pass
        if choosenAlgrithms["face"] == "True":
            self.detect_face(frame)
        if choosenAlgrithms["banana"] == "True":
            self.detect_banana(frame)

        return frame

    ############################## FACE ######################################
    def detect_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # faces to lista punktow i rozmiary (x, y, w, h)
        faces = self.faceCascade.detectMultiScale(
            gray,
            # parametry dobrane tak,by wykrywanie dzialalo najlepiej
            scaleFactor=1.15,
            minNeighbors=5,
            minSize=(20, 20),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        # rysowanie prostokata wokol twarzy
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)

        return frame
    ############################### BANANA ####################################
    def detect_banana(self, frame):
        subframe = frame[150:300, 150:350]
        gray = cv2.cvtColor(subframe, cv2.COLOR_BGR2GRAY)

        faces = self.bananaCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return frame

    ############################### HAND ####################################
    def detect_hand(self, frame, track_window, term_crit, roi_hist):
        """Funkcja sledzaca dlon na wideo

        Funkcja  szuka najlpeszego dopasowania histogramu obiektow na streamie z histograme modelu dloni,
        a nastepnie przesuwa tam ramke
        :param frame:array, pojedyncza ramka RGB ze video
        :param track_window:rect, zawiera ostatnie polozenie ramki otaczajacej dlon
        :param term_crit:
        :param roi_hist:array, histogram naszego modelu dloni
        :return: track_window, term_crit, roi_hist
        """
        # Odcinami dolna czesc obrazu poniewaz dlon kolorystycznie jest podobna do piasku przy torach
        frame = frame[0:500]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Funkcja porownujaca histogram modelu z histogramem z pojedynczej ramki
        dst = cv2.calcBackProject([hsv], [0, 1], roi_hist, [0, 180, 0, 250], 2)
        dst = cv2.medianBlur(dst, 3)  # powoduje usuniecie niektorych szumow do testowania

        # Funkcja szukajaca srodka masy tzn przesuwa okno w miejsce wiekszego zagesczenia dst
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)
        x, y, w, h = track_window
        # Pobieramy ramke z obrazu rozkladu prawdobodobientwa znalezienia tego samego histogramu
        ramka = dst[y:y + h, x:x + w]
        # pewnego rodzaju treshold ktory eliminuje szumy i powoduje ze nie pojawia sie obramowanie
        if np.sum(ramka) > 10000:
            cv2.rectangle(frame, (x, y), (x + w, y + h), 100, 2)

        return frame, track_window, term_crit, roi_hist