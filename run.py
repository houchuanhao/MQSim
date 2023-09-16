#import os
#os.system("./MQSim -i ssdconfig.xml -w workload.xml")

A = [] # 15 15 10 10 9 9
B = [] # 16 16 10 10 9 8 8
n = []
for i in range(1,20):
    A.append(0)
    B.append(0)
A[15] = 2
A[10] = 2
A[9] = 2
B[16] = 2
B[10] = 2
B[9] = 1
B[8] = 2

class node:
    ca = []
    cb = []
    asturn = True
    current = (0,0)
    subNodes= []

histories = []
def travel(ca,cb,now,asTurn,history):
    win = 0
    for n in ca:
        win = win + n
    if win ==0:
        print("awin!")
        #histories.append(history)
        print(history)
        return
    win = 0
    for n in cb:
        win = win + n
    if win ==0:
        print("bwin!")
        #histories.append(history)
        print(history)
        return


    base = []
    if asTurn == True:
        base = ca
    else:
        base = cb
    num,id = now
    for i in range(0,len(base)): # i is id   base[i] is num
        if base[i]==0:
            continue
        else:
            if num == 0: # 不能不出
                for j in range(1,base[i]+1):
                    base_tmp = base.copy()
                    base_tmp[i] = base_tmp[i] - j
                    hcp = history.copy()
                    hcp.append((asTurn,j, i))
                    if asTurn:
                        travel(base_tmp.copy(),cb,(j,i),not asTurn,hcp)
                    else:
                        travel(ca, base_tmp.copy(), (j, i), not asTurn, hcp)
            else:
                if i > id and base[i] >= num:
                    base_tmp = base.copy()
                    base_tmp[i] = base_tmp[i] - num
                    hcp = history.copy()
                    hcp.append((asTurn,num, i))
                    if asTurn:
                        travel(base_tmp.copy(),cb,(num,i),not asTurn, hcp)
                    else:
                        travel(ca, base_tmp.copy(), (num, i), not asTurn, hcp)
                hcp = history.copy()
                hcp.append((asTurn,0, 0))
                travel(ca,cb,(0,0),not asTurn ,hcp)

travel(A,B,(0,0),False,[])

print("zzzzz\n",histories)