import numpy as np
import cv2
import imutils
from imutils import contours
import math
import copy


class ColorLabel:
	'''
	Opis: Model przechowujacy informacje o liczbie pixeli r,g,b na konkretnym obrazie
	 
	Zmienne:
		area - pole, z ktorego beda zliczane pixele
		w - szerokosc area
		h - wysokosc area	   
	'''
    def __init__(self, area, w, h):
        self.area = area
        (self.width, self.height) = (w, h)
        self.bgr = [0, 0, 0]
        pass
		
	'''
	Opis: Glowna funkcja uruchamaiacja prywatne funkcje zliczajace pixele 
	'''
    def label(self):
            return self.__label_square()
			
	'''
	Opis: Prywatna funkcja zliczajaca pixele z kwadratu.
	'''
    def __label_square(self):
        for y in range(self.height):
            for x in range(self.width):
                self.__update_bgr(self.__max_channel(self.area[y, x]))
        return self.__color()

	'''
	Opis: Prywatna funkcja decydujaca jaki kolor (rgb) jest dominujacy na obrazie (area).
	'''
    def __color(self):
        index = np.argmax(self.bgr)
        if index == 0:
            return "purple"
        if index == 1:
            return "green"
        if index == 2:
            return "red"
			
	'''
	Opis: Prywatna funkcja dodajaca wartosc do tablicy bgr - tablica przechowuajca wartosc o liczbie dominujacacyh kolorow pixeli
	Zmienne wejściowe: index (int)
	'''
    def __update_bgr(self, index):
        self.bgr[index] += 1
        pass
		
	'''
	Opis: Prywatna funkcja dodajaca jaki kolor (rgb) dominuje na pixelu. 
	Zmienne wejściowe: pixel (array)
	'''
    def __max_channel(self, pixel):
        index = np.argmax(pixel)
        return index


class ImageWrapper:
	'''
	Opis: Wrapper (funkcja opakowujaca) dla obrazu(danych przechowywanych przez OpenCV).
		Przechowuje dodatkowe transofrmacje obrazu. 
		
	Zmienne: klatka przechowycona przez opencv, wspolczynnik do zmiany wielkosci obrazu	   
	'''
    def __init__(self, image, ratio=1):
        self.image = image
        self.output_image = copy.deepcopy(image)
        self.ratio = ratio
        self.height, self.width = self.image.shape[:2]
        self.resized = cv2.resize(self.image, (int(self.height * ratio), int(self.width * ratio)))
        self.blurred = cv2.GaussianBlur(self.image, (5, 5), 0)
        self.hsv = cv2.cvtColor(cv2.GaussianBlur(self.image, (11, 11), 0), cv2.COLOR_BGR2HSV)
        self.gray = cv2.cvtColor(self.blurred, cv2.COLOR_BGR2GRAY)
        self.edged = cv2.Canny(self.blurred, 50, 150)
        self.lab = cv2.cvtColor(self.blurred, cv2.COLOR_BGR2LAB)
        self.thresh = cv2.threshold(self.gray, 60, 255, cv2.THRESH_BINARY)[1]
        self.cnts = None
	
	'''
	Opis: Prywatna funkcja znajdujaca contury na obrazie.
	Zmienne wejściowe: obraz z opencv
	'''
    def __contours(self, image):
        self.cnts = cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.cnts = self.cnts[0] if imutils.is_cv2() else self.cnts[1]
		
	'''
	Opis: Funkcja zwaracajaca kontury z obrazu po transofmracji Cannego (krawedzie)
	Zmienne wyjściowe: kontury obrazu
	'''
    def contours_shape(self):
        self.__contours(self.edged)
        return self.cnts
		
	'''
	Opis: Funkcja zwaracajaca kontury z obrazu po binearyzacji (obraz czarno bialy)
	Zmienne wyjściowe: kontury obrazu
	'''
    def contours_color(self):
        self.__contours(self.thresh)
        return self.cnts


class ContourWrapper:
	'''
	Opis: Wrapper (funkcja opakowujaca) dla kontury(obiekt biblioteki OpenCV).
		Przechowuje dodatkowe informacje o konturze.
		
	Zmienne: kontur wykryty przez openCV
	'''
    def __init__(self, contour):
        self.contour = contour
        self.peri = cv2.arcLength(self.contour, True)
        self.approx = cv2.approxPolyDP(self.contour, 0.04 * self.peri, True)
        self.M = cv2.moments(self.contour)
        (self.x, self.y, self.w, self.h) = cv2.boundingRect(self.approx)
        self.bounding_rect = (self.y, self.x, self.w, self.h)
        ((self.x_mnc, self.y_mnc), self.radius) = cv2.minEnclosingCircle(contour)
        self.area = cv2.contourArea(self.contour)
        # cX and cY are center of mass of contour
        self.cX, self.cY = self.__get_cx_cy()
		
	'''
	Opis: Prywatna funkcja zwaracajaca srodek (x,y) konturu.
	Zmienne wyjściowe: x, y konturu
	'''
    def __get_cx_cy(self):
        cx = 0
        cy = 0
        if self.M["m00"] > 0:
            cx = int((self.M["m10"] / self.M["m00"]) * self.ratio)
            cy = int((self.M["m01"] / self.M["m00"]) * self.ratio)
        return cx, cy


class GraphicsUtils:
	'''
	Opis: Klasa pomocniczna. Rysuje informacje na obrazie wyjsciowym
	'''
    def __init__(self):
        pass

	'''
	Opis: Funkcja pisze na obrazie informacje o wykrytej(lub nie) stacji
	Zmienne wejściowe: klatka, nazwa stacji(string)
	'''
    def draw_station_status(self, image, text):
        string = "Station: " + text
        cv2.putText(image, string, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        pass
		
	'''
	Opis: Funkcja pisze na obrazie informacje o wykrytym(lub nie) pociagu
	Zmienne wejściowe: klatka, nazwa pociagu(string)
	'''
    def draw_train_status(self, image, idx):
        string = "Train: " + str(idx)
        cv2.putText(image, string, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        pass


square_str = "square"
triangle_str = "triangle"


class Shape:
	'''
	Opis: Klasa pomocniczna. Przechowuje informacje o figurze.
	
	Zmienne:
		typ - typ figury(string)
		area - pole,
		center_x - polozenie x srodka figury
		center_y - polozenie y srodka figury
		x - polozenie x najbardziej wysunietego lewego, dolnego punktu figury
		y - polozenie y najbardziej wysunietego lewego, dolnego punktu figury
		w - szerokosc figury
		h - wysokosc figury
	'''
    def __init__(self, type="", area=0, center_x=0, center_y=0, x=0, y=0, w=0, h=0):
        self.type = type
        self.contour = None
        self.area = area
        self.centerX = center_x
        self.centerY = center_y
        (self.x, self.y, self.w, self.h) = (x, y, w, h)
        pass
		
	'''
	Opis: Funkcja prywatna. Sprawdza czy typ 1 jest tym typem co typ 2 czy nie. 
	Zmienne wejściowe: nazwa typu 1, nazwa typu 2
	Zmienne wyjściowe: czy typ1 jest tym samym typem co typ2
	'''
    def __if_type(self, type1, type2):
        return type1 == type2
		
	'''
	Opis: Funkcja przypisujaca kontur do figury.
	Zmienne wejściowe: kontur
	'''
    def set_contour(self, contour):
        self.contour = contour
        pass
		
	'''
	Opis: Funkcja przypisujaca polozenie srodak
	Zmienne wejściowe: srodek x figury, srodek y figury
	'''
    def set_center(self, c_x, c_y):
        self.centerX = c_x
        self.centerY = c_y

	'''
	Opis: Funkcja ustawiajaca typ figury na podstawie liczby krawedzi.
	Zmienne wejściowe: liczba krawedzi
	'''
    def set_type(self, approx):
        if 4 <= approx <= 4:
            self.type = square_str
        elif approx == 3:
            self.type = triangle_str
        else:
            self.type = "unknown"
        pass

	'''
	Opis: Funkcja ustawiajaca polozenie i wielkosc figury.
	Zmienne wejściowe: lewy dolny x, lewy dolny y, szeokosc, wysokosc
	'''	
    def set_size(self, x, y, w, h):
        (self.x, self.y, self.w, self.h) = (x, y, w, h)
        pass

	'''
	Opis: Funkcja prywatna sprawdzajaca czy figura jest kwadratem.
	Zmienne wyjściowe: czy figura jest kwadratem (bool)
	'''			
    def is_square(self):
        if self.__if_type(self.type, square_str):
            return True
        return False
		
	'''
	Opis: Funkcja prywatna sprawdzajaca czy figura jest trojkatem.
	Zmienne wyjściowe: czy figura jest trojkatem (bool)
	'''	
    def is_triangle(self):
        if self.__if_type(self.type, triangle_str):
            return True
        return False

	'''
	Opis: Funkcja sprawdzajca czy pole figury jest wieksze niz dane
	Zmienne wyjściowe: pole do porownania
	Zmienne wyjściowe: bool
	'''		
    def is_area_higer_than(self, value):
        return self.area >= value
		
	'''
	Opis: Funkcja sprawdzajca czy pole figury jest mniejsze niz dane
	Zmienne wyjściowe: pole do porownania
	Zmienne wyjściowe: bool
	'''	
    def is_area_lower_than(self, value):
        return self.area <= value
		
	'''
	Opis: Funkcja pozwalajca wypisac figure za pomoca print()
	'''	
    def __str__(self):
        str = "Type: %s, color: %s, area: %d, center(x,y): %d, %d, size(x,y,w,h): %d, %d, %d, %d" % (self.type, self.color, self.area, self.centerX, self.centerY, self.x, self.y, self.w, self.h)
        return str


class ShapeDetector:
	'''
	Opis: Klasa sluzaca szukaniu zajezdni, peronow i pociagow.
	
	Zmienne:
		image - obiekt klasy ImageWrapper
	'''
    def __init__(self, image):
        self.IW = ImageWrapper(image)
        self.shape = Shape()
        self.detected = False
        self.stations = {'red': 'zajezdnia', 'green': 'strzyza', 'purple': 'kieplinek'}
        self.trains = {'red': 6, 'green': 2, 'purple': 1}
        pass

	'''
	Opis: Funkcja uruchamiajaca detekcje pociagow.
	'''		
    def detect_trains(self):
        return self.__detect(trains=True)
		
	'''
	Opis: Funkcja uruchamiajaca detekcje stacji.
	'''	
    def detect_platforms(self):
        return self.__detect(platforms=True)

	'''
	Opis: Funkcja uruchamiajaca detekcje zajezdni.
	'''	
    def detect_depot(self):
        return self.__detect(depot=True)

	'''
	Opis: Prywatna, glowna funkcja, uruchamiana przez odpowiednie funkcje powyzej.
		Jej zadaniem jest detekcja wybranych obiektow.
	Zmienne wejściowe: detekcja stacji(bool), detekcja zajezdni(bool), detekcja pociagow(bool)
	
	Zmienne wyjściowe: przetworzona klatka
	'''	
    def __detect(self, platforms=False, depot=False, trains=False):
        self.detected = False
        output = {"train": 0 , "platform": None}
        array_of_contours = []
        GU = GraphicsUtils()
        for c in self.IW.contours_shape():
            CW = ContourWrapper(c)
            self.shape.set_type(len(CW.approx))
            self.shape.area = CW.area
            self.shape.set_contour(CW.contour)
            if self.shape.is_square():
                if self.shape.is_area_higer_than(200):
                    array_of_contours = self.add_cw_to_similarity_array(array_of_contours, CW)

            if self.shape.is_triangle():
                if self.shape.is_area_higer_than(200):
                    array_of_contours = self.add_cw_to_similarity_array(array_of_contours, CW)
        #
        # for i in range(len(array_of_contours)):
        #     print(i)
        #     ratio = abs(array_of_contours[i].w / array_of_contours[i].h)
        #     print(str(array_of_contours[i].w) + ', ' + str(array_of_contours[i].h) + ', ' + str(ratio))
        #     if abs(ratio - 1.0) >= 0.3:
        #         print(abs(ratio - 1.0))
        #         array_of_contours.pop(i)
        #         print('usunieto')
        #         i -= 1

        for elem in array_of_contours:
            ratio = elem.w / elem.h
            if abs(ratio - 1.0) >= 0.3:
                array_of_contours.remove(elem)

        if len(array_of_contours) >= 2:
            if trains is True:
                #check squres
                a, b = self.check_cws_array_ratios(array_of_contours, 4.5, 1)
                if a is None and b is None:
                    pass
                else:
                    self.shape.set_center(b.cX, b.cY)
                    self.shape.set_size(b.x, b.y, b.w, b.h)
                    GU.draw_contour(self.IW.output_image, a.approx)
                    GU.draw_contour(self.IW.output_image, b.approx)
                    GU.draw_crosshair(self.IW.output_image, self.shape)
                    cl2 = ColorLabel(self.IW.image[b.y:b.y + b.h, b.x:b.x + b.w], b.w, b.h)
                    color2 = cl2.label()
                    GU.draw_train_status(self.IW.output_image, str(self.trains[color2]) + ", " + color2)
                    output["train"] = self.trains[color2]
            if platforms is True or depot is True:
                #check triangles
                a, b = self.check_cws_array_ratios(array_of_contours, 8.5, 1)
                if a is None and b is None:
                    pass
                else:
                    self.shape.set_center(b.cX, b.cY)
                    self.shape.set_size(b.x, b.y, b.w, b.h)
                    cl2 = ColorLabel(self.IW.image[b.y:b.y + b.h, b.x:b.x + b.w], b.w, b.h)
                    color2 = cl2.label()
                    if platforms is True:
                        if color2 is "green" or color2 is "purple":
                            GU.draw_station_status(self.IW.output_image, self.stations[color2] + ", " + color2)
                            GU.draw_contour(self.IW.output_image, a.approx)
                            GU.draw_contour(self.IW.output_image, b.approx)
                            GU.draw_crosshair(self.IW.output_image, self.shape)
                            output["platform"] = self.stations[color2]
                    if depot is True:
                        if color2 is "red":
                            GU.draw_station_status(self.IW.output_image, self.stations[color2] + ", " + color2)
                            GU.draw_contour(self.IW.output_image, a.approx)
                            GU.draw_contour(self.IW.output_image, b.approx)
                            GU.draw_crosshair(self.IW.output_image, self.shape)
                            output["platform"] = self.stations[color2]
        return output

	'''
	Opis: Funckja dodajca do tablicy kontur ktore tylko bardzo rozni sie od innych konturow (wiele kontorow rysujacych ten sam obiekt - a chcemy tylko jeden)
	Zmienne wejściowe: tablica konturow, kontur ktora ma byc dodany do tablicy konturow
	
	Zmienne wyjściowe: tablica kontoruow
	'''	
    def add_cw_to_similarity_array(self, cnts_array, CW):
        for cnt in cnts_array:
            if cnt.cX == CW.cX and cnt.cY == CW.cY:
                if 0.95 <= (cnt.area/CW.area) <= 1.05:
                    return cnts_array
        cnts_array.append(CW)
        return cnts_array

	'''
	Opis: Funckja sprawdzajaca kazdy kontur z kazdym. Jesli dwa maja dobry stosunek pola i polozenie x i y bardzo przyblzione to figura w figurze. 
	Zmienne wejściowe: tablica konturow, spodziewany stosunek pol, maxymalny blad stosunku jaki akceptujmy
	
	Zmienne wyjściowe: dwa kontury, ktore sa ulokowane jeden w drugim, o odpowiednim stosunku pola (lub None, None)
	'''	
    def check_cws_array_ratios(self, cnts_array, exp_ratio, error):
        expected_ratio = exp_ratio
        err = error
        ratio = 0
        for i in range(0, len(cnts_array)):
            for j in range(0, len(cnts_array)):
                if cnts_array[j].area != 0:
                    ratio = cnts_array[i].area / cnts_array[j].area
                    if abs(ratio-expected_ratio) <= err and self.check_similarity_of_two_cw(cnts_array[i], cnts_array[j]):
                        return cnts_array[i], cnts_array[j]
        return None, None
		
	'''
	Opis: Funckja sprawdzajaca polozenie x,y konturu z konturem. 
		Funckja zwraca true jesli kontur w koturze, false w przeciwnymn wypadku
	Zmienne wyjściowe: bool
	'''	
    def check_similarity_of_two_cw(self, cw_1, cw_2):
        err = 50
        if abs(cw_1.cX - cw_2.cX) <= err:
            if abs(cw_1.cY - cw_2.cY) <= err:
                return True
        return False