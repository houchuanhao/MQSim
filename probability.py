
def add(s,i):
    if i <0:
        return False
    if s[i]==6:
        s[i] = 1
        return add(s,i-1)
    else:
        s[i] = s[i] + 1
        return True
def getnum(lst,k):
    s = 0
    for j in lst:
        if j ==k:
            s=s+1
    return  s
def p(n,m,k): # n个骰子恰好出现m个k的概率
    s = []
    for i in range(0,n):
        s.append(1)
    i = 0
    total = 0
    while True:
        total = total + 1
        if getnum(s,k) == m:
            i = i + 1
        #print(s)
        if (add(s,len(s)-1)):
            continue
        else:
            break
    return i/total

def p_mor(n,m,k): # n个骰子至少出现m个k的概率
    s = []
    for i in range(0,n):
        s.append(1)
    i = 0
    total = 0
    while True:
        total = total + 1
        if getnum(s,k) == m:
            i = i + 1
        #print(s)
        if (add(s,len(s)-1)):
            continue
        else:
            break
    return i/total
#print(p(5,2,1))