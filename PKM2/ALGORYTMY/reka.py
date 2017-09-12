import numpy as np
import cv2




def reka( frame, track_window, term_crit, roi_hist ):
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

    return track_window, term_crit, roi_hist

