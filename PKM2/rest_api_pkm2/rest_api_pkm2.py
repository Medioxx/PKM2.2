from flask import Flask, render_template,jsonify, Response, request, abort
import os.path
import subprocess
from camera import Camera
from Detection import Detection


import cv2
app = Flask(__name__)



##################################
# 1.wykrywanie ruchu             #
# 2.wykrywanie zajezdni          #
# 3.wykrywanie peronu            #
# 4.wykrywanie przeszkod         #
# 5.wykrywanie reki              #
# 6.wykrzwanie twarzy            #
# 7.wykrywanie banana            #
##################################
class Algorithms:
    def __init__(self):
        # face, bananas, tracks
        self.algorithms = {"movement" : "False", "depot" : "False", "station" : "False", "obstacles": "False", "hand" : "False", "face" : "False", "train" : "False"}
        self.log_output_table = {'type': [u'movement', u'depot', u'station', u'obstacles', u'hand', u'face', u'train'],
                                 'launched': [u"False", u"False", u"False", u"False", u"False", u"False", u"False"]}
        self.tracks = []
        self.counter_proste = 0
        self.counter_widac_tory = 0

        self.neural = False





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

        for row in data:
            temp.append(row)
            print(row)
        self.tracks = temp

        #for i in range(0,len(data))

    def get_tracks(self):
        json_data = jsonify(alg.tracks)
        return json_data


    def get_algorithms(self):
        json_data = jsonify(alg.algorithms)
        return json_data

    #save dictionary to a txt file in html format
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

    # format dictionary to make it easy to display on a html page
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




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logs', methods = ['GET', 'POST'] )
def logs():
    #save logs as a html structure to a text file
    alg.dict_to_text_file()

    log_data = alg.get_log_zip_format_data()
    return render_template('logs.html',log_data=log_data)

@app.route('/tracks', methods = ['GET', 'POST'] )
def tracks():
    #save logs as a html structure to a text file
    #alg.dict_to_text_file()

    return render_template('tracks.html',data=alg.tracks)

@app.route('/tracks/set_tracks', methods = ['POST'] )
def logs_set_tracks():
    if not request.json:
        abort(400)
        output_data = alg.get_tracks()
        return output_data
    data = request.get_json()
    alg.set_tracks(data)
    output_data = alg.get_tracks()
    return output_data

@app.route('/logs/get_algorithms', methods = ['GET'] )
def logs_get_algorithms():
    output_data = alg.get_algorithms()
    return output_data


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
        ################################ choose your camera man #####################################

        #frame = camera.get_frame_aiball() # <-- ai-ball camera ()
        frame = camera.get_frame_webcam() # <-- personal computer camera

        # Achtung!
        frame = detection.detect_choosen_objects(frame, alg.algorithms)


        # Convert frame to format in which is it able to be displayed on a RestApi
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_out = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_out + b'\r\n\r\n')

# Recorded
def gen_recorded():
    path=os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)) + '\\FILMY'
    path += '\\bez_pociagow.avi'
    try:
        cap = cv2.VideoCapture(path)
    except:
        print("NOT FOUND")

    print("+++")
    while True:
        ################################ choose your camera man #####################################

        ret, frame = cap.read()
        if ret == True:

            # Display the resulting frame
            #cv2.imshow('Frame', frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break
        # Achtung!
        frame = detection.detect_choosen_objects(frame, alg.algorithms)


        # Convert frame to format in which is it able to be displayed on a RestApi
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_out = jpeg.tobytes()
        if alg.neural == True:
            path = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)) + '\\siec'+'\\frame.jpg'
            cv2.imwrite(path, frame)
            alg.neural = False

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_out + b'\r\n\r\n')

@app.route('/get_stream')
def get_stream():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_recorded')
def get_recorded():
    return Response(gen_recorded(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream')
def stream():
    return render_template('stream.html')

@app.route('/neural')
def neural():
    #tutaj nalezy podac sciezke do swojego pythona albo samego pythona jesli macie domyslnie ustawionego odpowiedniego dla naszego projektu
    path = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)) + '\\siec' + '\\detect_train.py'
    some_command = 'python %s' % path
    #p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)
    #(output, err) = p.communicate()
    #print(output)
    return render_template('neural.html',frame = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)) + '\\siec' +'\\frame.jpg')

@app.route('/neural/set_frame')
def neural_set_frame():
    alg.neural = True
    return "neural"

@app.route('/recorded')
def recorded():
    return render_template('recorded.html')

if __name__ == "__main__":
    alg = Algorithms()
    detection = Detection()
    app.run(host='0.0.0.0',port=5000, threaded=True)
