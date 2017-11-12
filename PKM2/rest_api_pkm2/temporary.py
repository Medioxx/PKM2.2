import requests
import json
import cv2
import sys
algorithms = {"movement": "False", "depot": "False", "station": "False", "obstacles": "False", "hand": "False",
                   "face": "False", "banana": "True"}

url_get = 'http://127.0.0.1:5000/logs/get_algorithms'
url_set = 'http://127.0.0.1:5000/logs/set_algorithms'

# GET


def get_algorithms():
    #get response from RestApi
    rest_api_response = requests.get(url_get)
    # Convert response to json/dictionary
    rest_api_dictionary = rest_api_response.json()

    algorithms["movement"] = rest_api_dictionary['movement']
    algorithms["depot"] = rest_api_dictionary['depot']
    algorithms["station"] = rest_api_dictionary['station']
    algorithms["obstacles"] = rest_api_dictionary['obstacles']
    algorithms["hand"] = rest_api_dictionary['hand']
    algorithms["face"] = rest_api_dictionary['face']
    algorithms["banana"] = rest_api_dictionary['banana']


def set_algorithms():
    requests.post(url_set, json=algorithms)

set_algorithms()
#get_algorithms()
print(algorithms)

