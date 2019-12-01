from flask import Flask, request, Response
from flask_cors import CORS
from datetime import datetime
import json
import pandas as pd
import logging
import heapq as hq

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

_key_delimiter = "_"
_host = "127.0.0.1"
_port = 5002
_api_base = "/api"

application = Flask(__name__)
CORS(application)

dataMop = pd.read_csv("Mop.csv", header=None)
Mop = dataMop.values.tolist()
dataMco = pd.read_csv("Mco.csv", header=None)
Mco = dataMco.values.tolist()

Wco = 7
Wop = 5


def handle_args(args):
    result = {}
    if args is not None:
        for k, v in args.items():
            if type(v) == list:
                v = v[0]
            result[k] = v
    return result

def log_and_extract_input(method, path_params=None):
    path = request.path
    args = dict(request.args)
    data = None
    headers = dict(request.headers)
    method = request.method
    url = request.url
    base_url = request.base_url
    try:
        if request.data is not None:
            data = request.json
        else:
            data = None
    except Exception as e:
        data = "You sent something but I could not get JSON out of it."
    log_message = str(datetime.now()) + ": Method " + method
    args = handle_args(args)
    inputs = {
        "path": path,
        "method": method,
        "path_params": path_params,
        "query_params": args,
        "headers": headers,
        "body": data,
        "url": url,
        "base_url": base_url
    }
    if args and args.get('fields', None):
        fields = args.get('fields')
        fields = fields.split(",")
        del args['fields']
        inputs['fields'] = fields
    log_message += " received: \n" + json.dumps(inputs, indent=2)
    logger.debug(log_message)
    return inputs


def log_response(path, rsp):
    msg = rsp
    logger.debug(str(datetime.now()) + ": \n" + str(rsp))

def get_field_list(inputs):
    return inputs.get('fields', None)


def generate_error(status_code, ex=None, msg=None):
    rsp = Response("Oops", status=500, content_type="text/plain")
    if status_code == 500:
        if msg is None:
            msg = "INTERNAL SERVER ERROR. Please take COMSE6156 -- Cloud Native Applications."
        rsp = Response(msg, status=status_code, content_type="text/plain")
    return rsp


def recommend1(teammates, opponents,ban):
    data = []
    for i in range(len(Mop)):
        D_max = 0
        Dco = 0
        Dop = 0
        if i + 1 in teammates or i + 1 in opponents or i + 1 in ban:
            continue
        for n in teammates:
            n = n - 1
            Dco = Dco + float(Mco[i][n])
        for n in opponents:
            n = n - 1
            Dop = Dop + float(Mop[i][n])
        D_max = Dco * float(Wco) + Dop * float(Wop)
        data.append((i + 1, D_max))
    res = sorted(data, key=lambda x: -x[1])
    champion = ""
    score = ""
    for i in range(9):
        champion = champion + str(res[i][0]) + ","
        score = score + str(res[i][1]) + ","
    champion = champion + str(res[10][0])
    score = score + str(res[10][1])
    recommend = {"recommend": champion, "score": score}
    return recommend


def recommend2(teammates, opponents, ban):
    data = []
    for j in range(len(Mop)):
        if j + 1 in teammates or j + 1 in opponents or j + 1 in ban:
            continue
        for i in range(j+1,len(Mop)):
            D_max = 0
            Dco = 0
            Dop = 0
            if i + 1 in teammates or i + 1 in opponents or i + 1 in ban:
                continue
            for n in teammates:
                n = n - 1
                Dco = Dco + float(Mco[i][n]) + float(Mco[j][n])
            for n in opponents:
                n = n - 1
                Dop = Dop + float(Mop[i][n]) + float(Mop[j][n])
            D_max = Dco * float(Wco) + Dop * float(Wop)
            data.append((j+1, i+1, D_max))
    res = sorted(data, key=lambda x: -x[2])
    champion1 = ""
    champion2 = ""
    for i in range(9):
        champion1 = champion1 + str(res[i][0]) + ","
        champion2 = champion2 + str(res[i][1]) + ","
    champion1 = champion1 + str(res[10][0])
    champion2 = champion2 + str(res[10][1])
    recommend = {"recommend1": champion1, "recommend2": champion2}
    return recommend

@application.route("/")
def hello():
    f = open("demo.html",'r')
    res = f.read()
    return res

@application.route("/url/<data>",methods=["GET"])
def UrlTest(data):
    res_list = {}
    inputs = log_and_extract_input(UrlTest, {"parameter": data})
    data_new = inputs['query_params']
    teammates = list(map(int, data_new['pick0'].split(',')))
    teammates = [x for x in teammates if x != 0]
    opponents = list(map(int, data_new['pick1'].split(',')))
    opponents = [x for x in opponents if x != 0]
    bans = list(map(int, data_new['bans'].split(',')))
    bans = [x for x in bans if x != 0]
    need = int(data_new['need'])
    if need == 1:
        res_list = recommend1(teammates, opponents, bans)
    elif need == 2:
        res_list = recommend2(teammates, opponents, bans)
    res = json.dumps(res_list)
    return res


if __name__ == "__main__":
    logger.debug("Starting test time : " + str(datetime.now()))
    application.debug = True
    application.run(host = _host, port= _port)