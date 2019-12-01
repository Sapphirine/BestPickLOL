import json
import pandas as pd
import sys

print("HTTP/1.1 200 OK\
Cache-Control: private\
Content-Type: text/html; charset=utf-8\
Server: Microsoft-IIS/8.5\
Date: Sun, 01 Dec 2019 03:40:45 GMT\
Content-Length: 4663\n")
print("Hello")

dataMop = pd.read_csv("C:/inetpub/wwwroot/lab/bestbp/server/Mop.csv", header=None)
Mop = dataMop.values.tolist()
dataMco = pd.read_csv("C:/inetpub/wwwroot/lab/bestbp/server/Mco.csv", header=None)
Mco = dataMco.values.tolist()
Wco = 7
Wop = 5

# python [0]local.py [1]bans [2]out [3]opp
argv = sys.argv
bans = list(map(int, argv[1].split(',')))
teammates = list(map(int, argv[2].split(',')))
opponents = list(map(int, argv[3].split(',')))
need = int(argv[4])

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
    for i in range(9):
        champion = champion + str(res[i][0]) + ","
    champion = champion + str(res[10][0])
    #recommend = {"recommend": champion}
    return champion

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
    #recommend = {"recommend1": champion1, "recommend2": champion2}
    return [champion1, champion2]

print("HTTP/1.1 200 OK\
Cache-Control: private\
Content-Type: text/html; charset=utf-8\
Server: Microsoft-IIS/8.5\
Date: Sun, 01 Dec 2019 03:40:45 GMT\
Content-Length: 4663\n")
if need == 1:
    res_list = recommend1(teammates, opponents, bans)
    print(res_list)
elif need == 2:
    res_list = recommend2(teammates, opponents, bans)
    print(res_list[0])
    print(res_list[1])
# res = json.dumps(res_list)
# print(res)
