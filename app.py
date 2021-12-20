from mmap import ACCESS_DEFAULT
from flask import Flask, jsonify, make_response
from flask import request
import pandas as pd
import json
from pandas.io.formats.format import set_eng_float_format
import time

def current_milli_time():
    return round(time.time() * 1000)

app = Flask(__name__)

USERS = {}
USERS['Johannes Hool'] = -1
USERS['Yannis Heutschi'] = -1
USERS['Fernando Laski'] = -1
USERS['Thomas Rudolf'] = -1
USERS['Jakob Thiel'] = -1
USERS['Robin Zeltner'] = -1

LAST = {}
LAST['Johannes Hool'] = -1
LAST['Yannis Heutschi'] = -1
LAST['Fernando Laski'] = -1
LAST['Thomas Rudolf'] = -1
LAST['Jakob Thiel'] = -1
LAST['Robin Zeltner'] = -1

RESULTS = pd.read_csv('steam_test_server.csv').values

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route("/results")
def results():
    res = ''
    rang = 1

    for k, v in sorted(USERS.items(), key=lambda item: item[1], reverse=True):
        if rang == 1 and str(v) != "-1":
            
            res += '<font size="+2">' + str(rang) + '. ' + k + ': (Score: ' + str(v) + ')</font><br><br>'
        else:
            res += str(rang) + '. ' + k + ': (Score: ' + str(v) + ')<br><br>'
        rang += 1 

    return res

@app.route("/compete", methods=['GET','POST'])
def compete():

    user = request.values.get('user')
    predictions = json.loads(request.values.get('predictions'))

    if user in USERS:
        stamp = current_milli_time()
        if LAST[user] + 5000 > stamp:
            data = {'message': 'Wait 5 Seconds before next try', 'score': 0}
            return make_response(jsonify(data), 200)
        else:
            LAST[user] = stamp
            score = 0
                
            for i in range(len(predictions)):
                if predictions[i] == RESULTS[i][0]:
                    score += 1
            score = round(score / len(RESULTS) *100, 3)
            if USERS[user] < score:
                USERS[user] = score

            data = {'message': 'Predictions received', 'score': score}
            return make_response(jsonify(data), 200)
    else:
        data = {'message': 'Wrong User', 'score': 0}
        return make_response(jsonify(data), 200)
