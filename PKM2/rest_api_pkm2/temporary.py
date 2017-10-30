
class Algorythms:
    def __init__(self):

        #self.keys = ["movement", "depot", "station", "obstacles", "hand", "face", "banana"]
        #self.values = ["False", "False", "False", "False", "False", "False", "False"]
        #self.algorythms = map(self.keys, self.values)
        self.algorythms = {"movement" : "False","depot" : "False","station" : "False","obstacles": "False","hand" : "False","face" : "False","banana" : "False"}
        self.log_output_table = {'type': [u'movement', u'depot', u'station', u'obstacles', u'hand', u'face', u'banana'],
                                 'launched': [u"False", u"False", u"False", u"False", u"False", u"False", u"False"]}

    def set_algorythms(self, data):
        #data = request.json
        self.algorythms["movement"] = data['movement']
        self.algorythms["depot"] = data['depot']
        self.algorythms["station"] = data['station']
        self.algorythms["obstacles"] = data['obstacles']
        self.algorythms["hand"] = data['hand']
        self.algorythms["face"] = data['face']
        self.algorythms["banana"] = data['banana']
        self.log_output_table = {'type': [u'movement', u'depot', u'station', u'obstacles', u'hand', u'face', u'banana'],
                                 'launched': [u"False", u"False", u"False", u"False", u"False", u"False", u"False"]}
    def retFalse(self):
        return "False"

    def retTrue(self):
        return "True"


    def get_algorythms(self):
        pass

alg = Algorythms()

print(alg.algorythms.keys())
print(alg.log_output_table.keys())