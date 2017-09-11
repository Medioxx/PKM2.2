import cv2

## xml'ka dzieki ktorej, mozemy wykrywac face'y
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def twarz(frame):
    # ramka w odcieniach szarosci
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #faces to lista punktow (x, y, w, h)
    faces = faceCascade.detectMultiScale(
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