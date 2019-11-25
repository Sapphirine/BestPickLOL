import requests
import json
import os
from time import sleep

# 3.1 遇到未知错误后不再退出，而是重试最多10次。
"""
每人使用3个账号同时跑
跑之前修改以下三个参数
USER_NAME 改为你账号昵称或者登录名，以便 API_KEY 过期后知道是哪个账号过期。
API_KEY   改为该账号对应 TOKEN
START_ID  每人的三个进程分别修改如下：
    杨：3178355993, 3178355994, 3178355995
    罗：3178355996, 3178355997, 3178355998
    陈：3178355999, 3178356000, 3178355991
STEP 不要修改。保持9，以保证获取ID不重合
"""
USER_NAME = "Yuansasi"
API_KEY = "RGAPI-0bbb4420-690d-4a18-b3d6-aa6add112204" #【1】
START_ID = 3178355993 #【2】
STEP = 9

# 全局参数
global OUTPUT_DICT, FILE_OUTPUT, FILE_RECORD, OUTPUT_HEAD
OUTPUT_DICT = {}
FILE_OUTPUT = "getData_output.csv"
FILE_RECORD = "getData_record.txt"
if os.path.exists(FILE_OUTPUT):
    OUTPUT_HEAD = False
else:
    OUTPUT_HEAD = True
HIGHLIGHTS = ["seasonId", "gameId", "platformId", "gameMode", "gameType", "gameDuration", "mapId", "gameVersion",\
                "teams[0].win", \
                "teams[0].bans[0].pickTurn", "teams[0].bans[0].championId", "teams[0].bans[1].pickTurn", "teams[0].bans[1].championId", \
                "teams[0].bans[2].pickTurn", "teams[0].bans[2].championId", "teams[0].bans[3].pickTurn", "teams[0].bans[3].championId", \
                "teams[0].bans[4].pickTurn", "teams[0].bans[4].championId", \
                "teams[1].win", \
                "teams[1].bans[0].pickTurn", "teams[1].bans[0].championId", "teams[1].bans[1].pickTurn", "teams[1].bans[1].championId", \
                "teams[1].bans[2].pickTurn", "teams[1].bans[2].championId", "teams[1].bans[3].pickTurn", "teams[1].bans[3].championId", \
                "teams[1].bans[4].pickTurn", "teams[1].bans[4].championId", \
                "participants[0].spell1Id", "participants[0].spell2Id", "participants[0].championId", "participants[0].timeline.lane", \
                "participants[1].spell1Id", "participants[1].spell2Id", "participants[1].championId", "participants[1].timeline.lane", \
                "participants[2].spell1Id", "participants[2].spell2Id", "participants[2].championId", "participants[2].timeline.lane", \
                "participants[3].spell1Id", "participants[3].spell2Id", "participants[3].championId", "participants[3].timeline.lane", \
                "participants[4].spell1Id", "participants[4].spell2Id", "participants[4].championId", "participants[4].timeline.lane", \
                "participants[5].spell1Id", "participants[5].spell2Id", "participants[5].championId", "participants[5].timeline.lane", \
                "participants[6].spell1Id", "participants[6].spell2Id", "participants[6].championId", "participants[6].timeline.lane", \
                "participants[7].spell1Id", "participants[7].spell2Id", "participants[7].championId", "participants[7].timeline.lane", \
                "participants[8].spell1Id", "participants[8].spell2Id", "participants[8].championId", "participants[8].timeline.lane", \
                "participants[9].spell1Id", "participants[9].spell2Id", "participants[9].championId", "participants[9].timeline.lane"]

# 测试扁平化输出
def test(text = "", autoExit=True):
    global OUTPUT_DICT
    if not text:
        testFile = open("sample.json", "r")
        text = testFile.read()
    iterateJSON("", json.loads(text))
    for key in OUTPUT_DICT:
        print(str(key) + ": " + str(OUTPUT_DICT[key]))
    print()
    if autoExit:
        exit()

# 发起网络请求
def getRequest(requestId):
    requestId = str(requestId)
    baseUrl = "https://na1.api.riotgames.com/lol/match/v4/matches/"
    header = {"X-Riot-Token":API_KEY}
    return requests.get(baseUrl+requestId, headers=header)

# 遍历字典(dict)类型的JSON数据，将键值对加入字典
def iterateJSON(prefix, item):
    for key in item:
        newPrefix = prefix + key
        if type(item[key]) == list:
            # 非叶子节点，添加前缀并进入
            flatList(newPrefix, item[key])
        elif type(item[key]) == dict:
            # 非叶子节点，添加前缀并进入
            flatDict(newPrefix, item[key])
        else:
            # 叶子节点，直接加入缓存字典(dict)
            appendColumn(newPrefix, item[key])

# 进入子节点(list)，并添加前缀
def flatList(prefix, items):
    index = 0
    while index < len(items):
        iterateJSON(prefix+"["+str(index)+"].", items[index])
        index = index + 1

# 进入子节点(dict)，并添加前缀
def flatDict(prefix, item):
    iterateJSON(prefix+".", item)

# 当前为叶子节点，直接加入缓存字典(dict)
def appendColumn(key, value):
    global OUTPUT_DICT
    OUTPUT_DICT[key] = value

# 获取新ID
def getNewID(startID, iterTimes=0):
    return startID + STEP * iterTimes

# 获取字典(dict)子集
def interestedDict(items, HIGHLIGHTS):
    newDict = {}
    for highLight in HIGHLIGHTS:
        if highLight in items.keys():
            newDict[highLight] = items[highLight]
        else:
            newDict[highLight] = ""
    return newDict

# 写入记录
def appendRecord(items):
    global OUTPUT_DICT, OUTPUT_HEAD, HIGHLIGHTS
    if OUTPUT_HEAD:
        OUTPUT_HEAD = False
        appendRecord(HIGHLIGHTS)
    newStr = ""
    if type(items) == list:
        for i in range(0,len(HIGHLIGHTS)-1):
            newStr = newStr + str(items[i]) + ","
        newStr = newStr + str(items[len(items)-1]) + "\n"
    else:
        items = interestedDict(items, HIGHLIGHTS)
        for i in range(0,len(HIGHLIGHTS)-1):
            newStr = newStr + str(items[HIGHLIGHTS[i]]) + ","
        newStr = newStr + str(items[HIGHLIGHTS[len(items)-1]]) + "\n"
    
    record_file = open(FILE_OUTPUT,"a")
    record_file.write(newStr)
    record_file.close()

# 获取上一次任务进行到的ID和状态
def getLastID():
    if os.path.exists(FILE_RECORD):
        record_file = open(FILE_RECORD,"r")
        record_read = record_file.read().split(",")
        lastID   = int(record_read[0])
        skipThis = int(record_read[1])
        record_file.close()
    else:
        lastID = START_ID
        skipThis = 0
    return (lastID, skipThis)

# 记录上一次任务进行到的ID和状态
def recordID(id, code):
    if code == 200 or code == 404:
        skipThis = 1
    else:
        skipThis = 0
    record = str(id)+","+str(skipThis)
    record_file = open(FILE_RECORD,"w")
    record_file.write(record)
    record_file.close()

def main():
    #test()
    global OUTPUT_DICT
    tryTimes = 0
    (startID, iterTimes) = getLastID()
    print("用户名为 "+USER_NAME+" 的账户开始工作。起始测试ID为 "+str(startID)+" 步长为 "+str(STEP))
    while True:
        OUTPUT_DICT = {}
        newID = getNewID(startID, iterTimes)
        response = getRequest(newID)
        code = response.status_code
        if code == 404:
            print("["+str(iterTimes)+"-"+str(newID)+"] 404")
            tryTimes = 0
        elif code == 429:
            iterTimes = iterTimes - 1
            print("["+str(iterTimes)+"-"+str(newID)+"] 请求频率过高，休息2秒")
            sleep(2)
            tryTimes = 0
        elif code == 200:
            iterateJSON("", json.loads(response.text))
            appendRecord(OUTPUT_DICT)
            print("["+str(iterTimes)+"-"+str(newID)+"] 成功写入记录")
            tryTimes = 0
        elif code == 403:
            print("["+str(iterTimes)+"-"+str(newID)+"] API KEY 过期，请登录 https://developer.riotgames.com/ 更新用户 "+USER_NAME+" 的密钥")
            break
        else:
            tryTimes = tryTimes + 1
            print("["+str(iterTimes)+"-"+str(newID)+"] 第"+str(tryTimes)+"次错误。代码"+str(code)+"，以下是返回头：")
            test(text=str(response.headers).replace('"','@').replace("'",'"').replace('@',"'"), autoExit=False)
            iterTimes = iterTimes - 1
            if tryTimes >= 10:
                print("\n\n超过10次连续失败，放弃重试\n\n")
                break
            else:
                print("\n\n正在重试\n\n")
        recordID(newID, code)
        iterTimes = iterTimes + 1
        #sleep(0.3)
    print("用户名为 "+USER_NAME+" 的进程已停止工作。")
    exit()

if __name__ =="__main__":
    main()

"""
[1] 密钥有效期为24小时，过期后前往 https://developer.riotgames.com/ 获取新密钥
[2] 运行前设置为商议的值
"""