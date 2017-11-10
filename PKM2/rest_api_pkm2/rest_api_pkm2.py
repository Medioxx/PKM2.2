from flask import Flask, render_template,jsonify, Response, request, abort
import subprocess
import time
import flask
import json

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
        self.algorithms = {"movement" : "False", "depot" : "False", "station" : "False", "obstacles": "False", "hand" : "False", "face" : "False", "banana" : "False"}
        self.log_output_table = {'type': [u'movement', u'depot', u'station', u'obstacles', u'hand', u'face', u'banana'],
                                 'launched': [u"False", u"False", u"False", u"False", u"False", u"False", u"False"]}



    def set_algorithms(self, data):
        data = request.json
        self.algorithms["movement"] = data['movement']
        self.algorithms["depot"] = data['depot']
        self.algorithms["station"] = data['station']
        self.algorithms["obstacles"] = data['obstacles']
        self.algorithms["hand"] = data['hand']
        self.algorithms["face"] = data['face']
        self.algorithms["banana"] = data['banana']



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


if __name__ == "__main__":
    alg = Algorithms()
    app.run(port=5000)
