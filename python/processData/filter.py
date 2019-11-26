
ADDRESS = "data/3187/all"
FILE_NUM = 1

"""
    gameDuration, mapId, <winnerTeam>,
    team0ban1, t0b2, t0b3, t0b4, t0b5,
    team1ban1, t1b2, t1b3, t1b4, t1b5,
    player1pick, player1lane, p2p, p2l, p3p, p3l, ...
    player6pick, player6lane, p7p, p7l, p8p, p8l, ...
"""
indices = [ \
    5, 6, 8, \
    10, 12, 14, 16, 18, \
    21, 23, 25, 27, 29, \
    32, 33, 36, 37, 40, 41, 44, 45, 48, 49, \
    52, 53, 56, 57, 60, 61, 64, 65, 68, 69, \
    ]

illegalValue = ["", " ", "-1"]
def filterData(arr, indices):
    res = []
    for index in indices:
        if not arr[index] or arr[index] in illegalValue:
            arr[index] = "0"
        res.append(arr[index])
    if res[2] == "Win":
        res[2] = "0"
    else:
        res[2] = "1"
    return res

count = [0,0]
with open(f"{ADDRESS}/filtered.csv", 'w') as outf:
    print("----- Mission Start -----")
    for findex in range(1, FILE_NUM+1):
        print(f"Processing file #{findex}/{FILE_NUM} ... ", end='')
        with open(f"{ADDRESS}/{str(findex)}.csv", 'r') as f:
            head = f.readline()
            for row in f:
                count[0] += 1
                data = row.split(',')
                if len(data) >= 45:
                    if data[3] == "CLASSIC" and data[18] != "" and data[45] != 'NONE':
                        usefulData = filterData(data, indices)
                        outf.write(','.join(usefulData))
                        count[1] += 1
        print("Done")

print("----- Mission Complete -----")
print(f"{count[1]}/{count[0]} items were approved")
print("")
