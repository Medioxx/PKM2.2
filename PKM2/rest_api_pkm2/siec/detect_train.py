from keras.models import model_from_json
import numpy as np
import os
import cv2
import sys

"""
Modul ten zawiera dwie sieci neuronowe. 
Pierwsza z nich sluzy do rozpoznawnia trzech roznych pociagow zawierajace odpowiednie znaczniki.
Druga natomiast sluzy do rozpoznawania okreslonych stacji PKM
W celu uzyskania pliku do uczenia sieci i danych testowych, nalezy skontaktowac sie pod maila adbelniak@gmail.com
"""


def load_model():
    """ Funkcja ta sluzy do zaladowania modeli sieci neurnowoych w kontekscie aplikacji webowej.
    W celu zaladowania modelu w kontekscie tego modulu, nalezy zmienic sciezki do plikow .json i .h5
    
    :return: model obu sieci neuronowych
    """
    model_path = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)) + '\\pociag.json'
    weights_path = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)) + '\\pociag.h5'

    json_file = open(model_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(weights_path)

    model_path = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)) + '\\stacja.json'
    weights_path = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)) + '\\stacja.h5'

    json_file = open(model_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    station_model = model_from_json(loaded_model_json)
    station_model.load_weights(weights_path)
    return model, station_model


def detect_train(img, model, station_model):
    """Funkcja sluzy do detekcji pociagow i stacji kolejowych. 
    Model jest dostarczany z zewnatrz tak by nie ladowac go ponownie i zaosczedzic na czasie.
    
    output:
    0 - nothing
    1 - train blue square
    2 - train green square
    3 - train red square

    output_station:
    0 - nothig
    1 - kielpinek
    2 - strzyza
    3 - zajezdnia
     :param img:  array pojedynczy obraz odczytany z kamery z pociagu
      :param model:  array model sieci neuronowej do wykrywania pociagu
    :param station_model:  array model sieci neuronowej do wykrywania stacji
     :return:int, informacja na temat tego ktory obiekt zostal wykryty
     """

    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_height, img_width = 128, 96
    W, H, C = img.shape
    input_shape = ( 1, img_height, img_width, 3)
    pred_val = ''
    # skalowanie obrazu do rozmiaru 128x96
    img = cv2.resize(img, (0, 0), fx=img_height/H, fy=img_width/W)

    image = img
    grey_x = image.astype('float32')
    # normalizacja danych wejsciowych
    grey_x = grey_x.reshape(input_shape) / 255
    pred_value = model.predict(grey_x, batch_size=1, verbose=0)
    pred_value_station = station_model.predict(grey_x, batch_size=1, verbose=0)

    pred_train = np.argmax(pred_value)
    pred_station = np.argmax(pred_value_station)

    return pred_train, pred_station


if __name__ == '__main__':

    model, station_model = load_model()
    # Capture frame-by-frame

    path = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))
    path = os.path.abspath(os.path.join(path,os.pardir)) + '//static' + str(sys.argv[0])
    print(path)
    frame = cv2.imread(path)
    # Our operations on the frame come here
    detected, pred_station = detect_train(frame, model, station_model)
    # Display the resulting frame
    print(detected)
    print(pred_station)
    # Utworzenie nowego pliku txt i zapisanie do niego, outputow z sieci
    obj = open('output.txt', 'w')
    obj.write(str(detected) + '\n')
    obj.write(str(pred_station))

    obj.close()

