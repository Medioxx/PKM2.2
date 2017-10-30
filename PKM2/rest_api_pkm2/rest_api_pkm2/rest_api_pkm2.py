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
class Algorythms:
    def __init__(self):
        # face, bananas, tracks
        self.algorythms = {"movement" : "False","depot" : "False","station" : "False","obstacles": "False","hand" : "False","face" : "False","banana" : "False"}
        self.log_output_table = {'type': [u'movement', u'depot', u'station', u'obstacles', u'hand', u'face', u'banana'],
                                 'launched': [u"False", u"False", u"False", u"False", u"False", u"False", u"False"]}



    def set_algorythms(self, data):
        data = request.json
        self.algorythms["movement"] = data['movement']
        self.algorythms["depot"] = data['depot']
        self.algorythms["station"] = data['station']
        self.algorythms["obstacles"] = data['obstacles']
        self.algorythms["hand"] = data['hand']
        self.algorythms["face"] = data['face']
        self.algorythms["banana"] = data['banana']



    def get_algorythms(self):
        json_data = jsonify(alg.algorythms)
        return json_data

    #save dictionary to a txt file in html format
    def dict_to_text_file(self):
       f = open('table.txt', 'w')

       f.write('<table style="width:100%">')

       f.write('<tr>')
       for key, value in self.algorythms.items():
           f.write('<th>'+ key +'</th>')
       f.write('</tr>')

       f.write('<tr>')
       for key, value in self.algorythms.items():
           f.write('<td>' + value + '</td>')
       f.write('</tr>')

       f.write('</table>')
       f.close()

    # format dictionary to make it easy to display on a html page
    def get_log_zip_format_data(self):

        self.log_output_table['type'] = self.algorythms.keys()
        self.log_output_table['launched'] = self.algorythms.values()
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

@app.route('/logs/get_algorythms', methods = ['GET'] )
def logs_get_algorythms():
    output_data = alg.get_algorythms()
    return output_data


@app.route('/logs/set_algorythms', methods = ['POST'] )
def logs_set_algorythms():
    if not request.json:
        abort(400)
        output_data = alg.get_algorythms()
        return output_data
    data = request.get_json()
    alg.set_algorythms(data)
    output_data = alg.get_algorythms()
    return output_data


if __name__ == "__main__":
    alg = Algorythms()
    app.run(port=5000)
