import cv2
import numpy as np


def przeszkody(frame,counter_proste,counter_widac_tory):
    '''
    Opis: Wykrywa przeszkody na obrazie
    Zmienne wejściowe: obraz z kamery, licznik zwiększany w momencie wykrycia prostych, licznik zwiększany w momencie wykrycia torów
    Zmienne wyjsciowe: licznik zwiększany w momencie wykrycia prostych, licznik zwiększany w momencie wykrycia torów
    '''
    # wycinamy fragment, na ktorym widac tory
    subframe = frame[300:500, 150:350]

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