
ADDRESS = "data/3187/yzh"
MODE = "normal"
AIM_STAGE = 18 # Max 6(normal) or 18(champion)

if MODE == "normal" and AIM_STAGE > 6:
    print(f"[WARNING] Parameter \"AIM_STAGE\" is set too large (max 6, found {AIM_STAGE}). Changed to 6 already.")
    AIM_STAGE = 6
elif AIM_STAGE > 18:
    print(f"[WARNING] Parameter \"AIM_STAGE\" is set too large (max 18, found {AIM_STAGE}). Changed to 18 already.")
    AIM_STAGE = 18

"""
    [00]gameDuration, [01]mapId, [02]<winnerTeam>, 
    [03]team0ban1, [04]t0b2, [05]t0b3, [06]t0b4, [07]t0b5, 
    [08]team1ban1, [09]t1b2, [10]t1b3, [11]t1b4, [12]t1b5, 
    [13]player1pick, [14]player1lane, [15]p2p, [16]p2l, [17]p3p, [18]p3l, ... 
    [23]player6pick, [24]player6lane, [25]p7p, [26]p7l, [27]p8p, [28]p8l, ... 
"""
stage = []
if MODE == "normal":
    # Environment
    stage.append([2, 3,4,5,6,7,8,9,10,11,12])
    # Pick
    stage.append([13,14])        # 1 Blue Pick 1
    stage.append([23,24, 25,26]) # 2 Red  Pick 2
    stage.append([15,16, 17,18]) # 3 Blue Pick 2
    stage.append([27,28, 29,30]) # 4 Red  Pick 2
    stage.append([19,20, 21,22]) # 5 Blue Pick 2
    stage.append([31,32])        # 6 Red  Pick 1
else:
    # Environment
    stage.append([0, 1, 2])
    # Ban 1
    stage.append([3])
    stage.append([8])
    stage.append([4])
    stage.append([9])
    stage.append([5])
    stage.append([10])
    # Pick 1
    stage.append([13, 14])
    stage.append([23, 24, 25, 26])
    stage.append([15, 16, 17, 18])
    stage.append([27, 28])
    # Ban 2
    stage.append([11])
    stage.append([6])
    stage.append([12])
    stage.append([7])
    # Pick 2
    stage.append([29, 30])
    stage.append([19, 20])
    stage.append([31, 32])
    stage.append([21, 22])

def filterByStages(arr, stage, turn):
    res = []
    for stageIndex in range(0, turn+1):
        for item in stage[stageIndex]:
            res.append(arr[item])
    return res

print("----- Mission Start -----")

for turn in range(1, AIM_STAGE+1):
    print(f"Processing stage #{turn}/{AIM_STAGE} ... ", end='')
    with open(f"{ADDRESS}/filtered.csv",'r') as f, \
        open(f"{ADDRESS}/t{turn}.csv",'w') as outf:
        for row in f:
            data = row.strip('\n').split(',')
            turnData = filterByStages(data, stage, turn)
            outf.write(','.join(turnData)+"\n")
    print("Done")

print("----- Mission Complete -----")
