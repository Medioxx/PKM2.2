import cv2
import numpy as np
from marker_detector import ShapeDetector
##################################
# 1.wykrywanie ruchu             #
# 2.wykrywanie zajezdni          #
# 3.wykrywanie peronu            #
# 4.wykrywanie przeszkod         #
# 5.wykrywanie reki              #
# 6.wykrzwanie twarzy            #
# 7.wykrywanie pociągu            #
##################################
#self.algorithms = {"movement" : "False", "depot" : "False", "station" : "False",
# "obstacles": "False", "hand" : "False", "face" : "False", "banana" : "False"}

class Detection(object):
    # Inicjalizacja algorytmów oraz niezbędnych do działania ich zmiennych
    def __init__(self):
        ################### wykrywanie reki ###################
        self.zatrzask = 0
        self.track_window = 0
        self.term_crit = 0
        self.roi_hist = 0
        self.track_window, self.term_crit, self.roi_hist = self.init_hand()
        # FACE INITIALIZATION
        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # obstacles
        self.counter_proste = 0
        self.counter_widac_tory = 0
        # movement
        self.licznik_ruch = 0
        self.fgbg = cv2.createBackgroundSubtractorMOG2()



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

    # Najważniejsza funkcja służąca do przetwarzania obrazu
    # Na podstawie otrzymanego słownika 'choosenAlgorithms'
    # przetwarza otrzymaną ramkę (obraz) 'frame'
    def detect_choosen_objects(self,frame,choosenAlgrithms):
        shape_detector = ShapeDetector(frame)

        if choosenAlgrithms["movement"] == "True":
            self.licznik_ruch = self.ruchomy(frame, self.licznik_ruch, self.fgbg)
            pass
        if choosenAlgrithms["depot"] == "True":
            shape_detector.detect_depot()
            frame = shape_detector.IW.output_image
            #frame = shape_detector.IW.edged
            pass
        if choosenAlgrithms["station"] == "True":
            shape_detector.detect_platforms()
            frame = shape_detector.IW.output_image
            pass
        if choosenAlgrithms["obstacles"] == "True":
            self.counter_proste, self.counter_widac_tory = self.przeszkody(frame, self.counter_proste, self.counter_widac_tory)
            pass
        if choosenAlgrithms["hand"] == "True":
            frame, self.track_window, self.term_crit, self.roi_hist = self.detect_hand(frame, self.track_window, self.term_crit, self.roi_hist)
            pass
        if choosenAlgrithms["face"] == "True":
            self.detect_face(frame)
        #pociag
        if choosenAlgrithms["train"] == "True":
            #self.detect_banana(frame)
            shape_detector.detect_trains()
            frame = shape_detector.IW.output_image

        return frame

    ############################### Ruch pociągu ####################################
    def ruchomy(self, frame,licznik,fgbg):

        """"
        :param frame:array, pojedyncza ramka RGB ze video
        :param licznik:int, treshold ktory odpowiada za wyzwalanie z opoznieniem wykrywania ruchu pociagu
        :param fgbg:BackgroundSubtractorMOG2, Obiekt do porownnywania ramek
        :return:licznik, int
        """
        height, width = frame.shape[:2]
        prev_frame = np.zeros([130, width])
        history = 4

        obraz = frame[350:height]
        fgmask = fgbg.apply(obraz, learningRate=1.0/history)
        gray = cv2.cvtColor(obraz, cv2.COLOR_BGR2GRAY)

        prev_frame = gray

        uklad = np.sum(fgmask)

        font = cv2.FONT_HERSHEY_SIMPLEX
        if(uklad < 40000):
            licznik -= 1
        elif (uklad > 40000):
            licznik = 6

        if(licznik <= 0):
            cv2.putText(frame, 'stoi', (100, 100), font, 3, (255, 255, 255), 2)

        if(licznik > 0):
            cv2.putText(frame, 'Jedzie', (100, 100), font, 3, (255, 255, 255), 2)

        return licznik

    ############################## Twarz ######################################
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

    ############################### Ręka ####################################
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

    ############################### Przeszkody ####################################
    def przeszkody(self,frame,counter_proste,counter_widac_tory):
        # wycinamy fragment, na ktorym widac tory
        subframe = frame[200:400, 150:350]

        # konwertujemy BGR do HSV
        hsv = cv2.cvtColor(subframe, cv2.COLOR_BGR2HSV)

        # definiujemy zakres koloru brazowego (mozna tutaj jeszcze poeksperymentowac)
        lower_brown = np.array([0, 15, 21])
        upper_brown = np.array([46, 106, 130])

        # maskowanie w celu uzyskania tylko brazowego koloru
        mask = cv2.inRange(hsv, lower_brown, upper_brown)

        # Thresholding, zdefiniowanie obszaru widocznosci torow
        thresh = cv2.threshold(mask, 25, 30, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # tutaj przechowujemy obszary
        contours = []

        for c in cnts:
            # ignorowanie zbyt malych obszarow
            if cv2.contourArea(c) < 8000:
                continue
            else:
                counter_widac_tory = 20
                contours.append(cv2.contourArea(c))

                #naniesienie ramki
                # (x, y, w, h) = cv2.boundingRect(c)
                # cv2.rectangle(subframe, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # wykrywanie lini
        empty = True
        numberOfLines = 0
        edges = cv2.Canny(subframe, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=70, lines=np.array([]),
                                minLineLength=80, maxLineGap=10)
        if lines is None:
            empty = False

        #pod uwage bierzemy linie prostopadle do dolnej krawedzi
        if (empty):
            a, b, c = lines.shape
            for i in range(a):
                if (abs(lines[i][0][2] - lines[i][0][0]) < 50):
                    cv2.line(subframe, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3,
                             cv2.LINE_4)
                    numberOfLines += 1

        #zabezpieczenie przed migajacymi komunikatami
        if (numberOfLines > 2):
            counter_proste = 15
        elif (numberOfLines == 0):
            counter_proste -= 1

        #wyswietlenie komunikatow
        if (counter_proste <= 1):
            cv2.putText(frame, 'ZAKRET ALBO PRZESZKODA', (30, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255))

        if (counter_widac_tory <= 1 and counter_proste <= 1):
            cv2.putText(frame, 'PRZESZKODA!', (30, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))

        counter_widac_tory -= 1

        return counter_proste, counter_widac_tory