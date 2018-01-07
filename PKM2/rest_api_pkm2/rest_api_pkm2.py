from flask import Flask, render_template,jsonify, Response, request, abort, redirect ,url_for
import os.path
import subprocess
import time
from camera import Camera
from Detection import Detection
from Sterowanie.ObjectsISA import *
from Sterowanie.trainConnection import trainClient
import cv2
from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime


app = Flask(__name__)


#route ADD 192.168.2.0 MASK 255.255.255.0 192.168.2.1   do podlaczenia do dwowch sieci



##################################
# 1.wykrywanie ruchu             #
# 2.wykrywanie zajezdni          #
# 3.wykrywanie peronu            #
# 4.wykrywanie przeszkod         #
# 5.wykrywanie reki              #
# 6.wykrzwanie twarzy            #
# 7.wykrywanie banana            #
##################################

# Klasa, która głównie służy do przechowywania listy "klucz: wartość" algorytmów,
# gdzie klucz jest danym algorytmem, a wartość przybierawartość prawda lub fałsz
# Algorytmy posiadające wartość prawda, są aktualnie włączone do przetwarzania
class Algorithms:
    def __init__(self):
        # Słownik, przechowujący informacje o włączonych algorytmach
        self.algorithms = {"movement" : "False", "depot" : "False", "station" : "False", "obstacles": "False", "hand" : "False", "face" : "False", "train" : "False"}
        self.log_output_table = {'type': [u'movement', u'depot', u'station', u'obstacles', u'hand', u'face', u'train'],
                                 'launched': [u"False", u"False", u"False", u"False", u"False", u"False", u"False"]}
        self.tracks = []
        self.counter_proste = 0
        self.counter_widac_tory = 0

        self.neural = False
        self.frame_neural = 1




    # Funkcja służąca do włączania/wyłączania algorytmów
    # po otrzymaniu pliku w formacie JSON
    def set_algorithms(self, data):
        data = request.json
        self.algorithms["movement"] = data['movement']
        self.algorithms["depot"] = data['depot']
        self.algorithms["station"] = data['station']
        self.algorithms["obstacles"] = data['obstacles']
        self.algorithms["hand"] = data['hand']
        self.algorithms["face"] = data['face']
        self.algorithms["train"] = data['train']


    def set_tracks(self, data):
        data = request.json
        temp = []
        print(data)
        for row in data:
            temp.append(row)
            print(row)
        self.tracks = temp

        #for i in range(0,len(data))

    def get_tracks(self):
        json_data = jsonify(alg.tracks)
        return json_data

    # Funkcja służąca do wysyłania aktualnego słownika algorytmów
    def get_algorithms(self):
        json_data = jsonify(alg.algorithms)
        return json_data

    # Zapis tablicy algorytmów w formacie tabeli do pliku txt
    # w formacie tabeli w języku HTML
    # Obecnie nieużywana
    def dict_to_text_file(self):
       f = open('table.txt', 'w')

       f.write('<table style="width:100%">')

       f.write('<tr>')
       for key, value in self.algorithms.items():
           f.write('<th>'+ key +'</th>')
       f.write('</tr>')

       f.write('<tr>')
       for key, value in self.algorithms.items():
           f.write('<td>' + value + '</td>')
       f.write('</tr>')

       f.write('</table>')
       f.close()

    # Formatowanie słownika w taki sposób, aby w prosty sposób
    # możnabyło go wyświetlić na stronie internetowej (RestApi, HTML)
    def get_log_zip_format_data(self):

        self.log_output_table['type'] = self.algorithms.keys()
        self.log_output_table['launched'] = self.algorithms.values()
        log_data = zip(self.log_output_table['type'], self.log_output_table['launched'])
        return log_data

    def get_tracks_zip_format_data(self):
        self.log_output_table['type'] = self.algorithms.keys()
        self.log_output_table['launched'] = self.algorithms.values()
        log_data = zip(self.log_output_table['type'], self.log_output_table['launched'])
        return log_data

# Klasa służąca do sterowania pociągiem
class SteerTrain():

    def __init__(self):
        self.trainDlg = trainClient()
        self.train=Train(5)
        self.train_properties={'velocity':0,'control':0}



    # Ustawianie prędkości pociągu
    def set_velocity(self, data):
        data = request.json
        self.train_properties["velocity"] = data['velocity']
        self.train_properties["control"] = data['control']
        print(self.train_properties)
        try:
            self.trainDlg.connect('127.0.0.1')
            time.sleep(1)
            self.trainDlg.sendMsg(self.train.changeVelocity(int(self.train_properties['velocity']),
                                                          int(self.train_properties['control'])))
            self.trainDlg.disconnect()
            return "OK"
        except:
            return "NOK"
# Klasa służąca do obsługi nagrań z folderu
class Movie():

    def __init__(self):
        self.path = path=os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)) + '\\FILMY'
        self.movieDict = []
        self.get_movies()
        if len(self.movieDict)==0:
            self.movie = None
        else:
            self.movie = self.movieDict[0]

    # Zwraca dostępne liste dostępnych filmó
    def get_movies(self):
        self.movieDict = []
        for file in os.listdir(self.path):
            if file.endswith(".avi"):
                self.movieDict.append(file)
        return self.movieDict

    # Wybiera film
    def set_movie(self,movie):
        self.movie = movie



def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)

#############################################################################
#                                                                           #
# Wszystko co znajduje się poniżej służy do obsługi RestApi                 #
# W '@app.route()' mamy podaną ścieżkę względną strony                      #
# Przy 'return' zwracamy szablon HTML'owy strony internetowej,              #
# w zależności od wybranej podstrony                                        #
#############################################################################

# Aby RestApi poprawnie działało wymagane jest połączenie z interneem do
# pobrania JQuery, Bootstrapa, ikon
# Oraz połączenie z Kamerą z pociągu do wyświetlania strumienia z kamery

# Główna strona
@app.route('/')
def index():
    return render_template('index.html')

# Opis aplikacji
@app.route('/about')
def about():
    return render_template('about.html')

# Wyświetla słownik algorytmów
@app.route('/logs', methods = ['GET', 'POST'] )
def logs():
    #Zapisuje słownik do pliku txt
    alg.dict_to_text_file()

    log_data = alg.get_log_zip_format_data()
    movie_data = movies.get_movies()
    return render_template('logs.html',log_data=log_data,movie_data = movie_data)

@app.route('/update_movie', methods = ['POST'] )
def update_movie():
    if request.method == 'POST':
        movie = request.form['movies']
        movies.set_movie(movie)
        return redirect(url_for('recorded'))
    return "test"

# Wyświetla, które tory są zajęte przez pociągi
@app.route('/tracks', methods = ['GET', 'POST'] )
def tracks():
    #save logs as a html structure to a text file
    #alg.dict_to_text_file()

    return render_template('tracks.html',data=alg.tracks)

# Przyjmuje informacje od algorytmu zajętości torów i wyświetla je na stronie
# '/tracks'
@app.route('/tracks/set_tracks', methods = ['POST'] )
def logs_set_tracks():
    if not request.json:
        alg.set_tracks([])
        abort(400)
        output_data = alg.get_tracks()
        return output_data
    data = request.get_json()
    alg.set_tracks(data)
    output_data = alg.get_tracks()
    return output_data

# Zwraca aktualny słownik algorytmów w formacie JSON
@app.route('/logs/get_algorithms', methods = ['GET'] )
def logs_get_algorithms():
    output_data = alg.get_algorithms()
    return output_data

# Aktualizuje słownik algorytmów w RestApi
@app.route('/logs/set_algorithms', methods = ['POST'] )
def logs_set_algorithms():
    if not request.json:
        abort(400)
        output_data = alg.get_algorithms()
        return output_data
    data = request.get_json()
    alg.set_algorithms(data)
    output_data = alg.get_algorithms()
    return output_data

# Stream
def gen(camera):
    while True:

        # Wybranie Kamery i pobranie obrazu
        frame = camera.get_frame_aiball()  # <-- ai-ball camera, kamera z pociągu
        #frame = camera.get_frame_webcam() # <-- Kamera z komputera (do testów)

        # Przetwarzanie obrazu wybranymi algorytmami
        frame = detection.detect_choosen_objects(frame, alg.algorithms)

        # Zmienia format obrazu, aby możnabyło go łatwo wyśietlić na stronie
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_out = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_out + b'\r\n\r\n')

# Nagranie
def gen_recorded():
    path=movies.path + '\\' + movies.movie
    try:
        cap = cv2.VideoCapture(path)
    except:
        print("NOT FOUND")

    while True:

        # Pobór obrazu z nagrania
        ret, frame = cap.read()
        if ret == True:

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break
        # Przetwarzanie obrazu
        frame = detection.detect_choosen_objects(frame, alg.algorithms)

        # Zmienia format obrazu, aby możnabyło go łatwo wyśietlić na stronie
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_out = jpeg.tobytes()
        if alg.neural == True:
            alg.frame_neural+=1
            path = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)) + '\\static'+'\\frame'\
                   +str(alg.frame_neural) +'.jpg'
            cv2.imwrite(path, frame)
            alg.neural = False

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_out + b'\r\n\r\n')

# Zwraca strumień z kamery
@app.route('/get_stream')
def get_stream():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Zwraca strumień z nagrania
@app.route('/get_recorded')
def get_recorded():
    return Response(gen_recorded(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Wyświetlanie strumienia na stronie
@app.route('/stream')
def stream():
    return render_template('stream.html')

@app.route('/neural')
@nocache
def neural():
    #tutaj nalezy podac sciezke do swojego pythona albo samego pythona jesli macie domyslnie ustawionego odpowiedniego dla naszego projektu
    path = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))
    absolute_path = path + '\\siec' + '\\detect_train.py' + '\\frame'\
                   +str(alg.frame_neural) +'.jpg'
    python = 'C:\\Users\\ISAlab\\Anaconda3\\python.exe'
    some_command = '%s %s' % (python,absolute_path)
    p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    file_path = path+ '\\siec' + '\\output.txt'
    with open(file_path) as f:
        content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    print(int(content[1]))
    print(int(content[0]))
    station = "Nothing"
    if int(content[1]) == 1:
        station = "Kelpinek"
    elif int(content[1]) == 2:
        station = "Strzyza"
    elif int(content[1]) == 3:
        station = "Zajezdnia"

    train = "Nothing"
    if int(content[0]) == 1:
        train = "blue square"
    elif int(content[0]) == 2:
        train = "green square"
    elif int(content[0]) == 3:
        train = "red square"

    return render_template('neural.html',station=station,train=train,frame='frame'\
                   +str(alg.frame_neural) +'.jpg')

@app.route('/neural/set_frame')
def neural_set_frame():
    alg.neural = True
    return "neural"

#  Wyświetla nagrania na stronie
@app.route('/recorded')
def recorded():
    return render_template('recorded.html',movie = movies.movie)


@app.route('/train/set_speed', methods = ['POST'] )
def train_set_speed():
    if not request.json:
        abort(400)
        output_data = alg.get_tracks()
        return output_data
    data = request.get_json()
    output_data=steerTrain.set_velocity(data)
    return output_data


if __name__ == "__main__":
    alg = Algorithms()
    detection = Detection()
    steerTrain=SteerTrain()
    movies = Movie()
    # RestApi jest domyślnie stawiane na localhoście
    # na porcie 5000
    # RestApi musi być wielowątkowe, aby działało poprawnie
    # (Obsługa kilku klientów)
    app.run(host='0.0.0.0',port=5000, threaded=True)
