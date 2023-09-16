from script.tools import tools
from script.collection import Parameter
import os

def collection(folder_path="workspace1",lst = None):
    rLst = []
    if lst != None:
        rLst = lst
    i = 0
    for f in os.scandir(folder_path):
        i = i + 1
        if f.is_dir():
            xmlpath= f.path+"/workload_scenario_1.xml"
            if not os.path.exists(xmlpath):
                print("no scenario", xmlpath)
                continue
            ssd = f.path + "/" + tools.xml_ssdcfg
            workload = f.path + "/" + tools.xml_workload
            dic_ssd,dic_worload = tools.xml2dic(ssd,workload)
            tree,root = tools.getTree(xmlpath)
            iops = tools.getext(root,"IOPS")
            if iops == "inf":
                print("iops info ",xmlpath)
            rLst.append([iops,dic_ssd,dic_worload,f.path])
            #print(iops)
    print("collection: ",len(rLst))
    print("total :", i)
    return (rLst)

def getParameters(path,id):
    ssdlst = tools.xlsx2lst(path,"ssd"+id)
    workloadlst = tools.xlsx2lst(path,"workload"+id)
    lst = []
    for row in ssdlst:
        p = Parameter.Parameter(row)
        lst.append(p)
    for row in workloadlst:
        p = Parameter.Parameter(row)
        lst.append(p)
    return lst
def struce2int(value=""):
    num = 0
    value = value.replace(" ","")
    value = value.split(",")
    '''
    for v in value:
        t = int(v)
        num = num | (1 << t)
    return num
    '''
    return len(value)
def usefull( p : Parameter, expect):
    if p.type == Parameter.Type.t_ignore:
        return False
    if p.key in expect:
        return False
    return True
def getUsefullKeys(dic :dict,plst, expect:list):
    lst_key = []
    lst_value = []
    for p in plst:
        if usefull(p , expect):
            if p.key not in dic.keys():
                print("not found key :",p.key)
                continue
            value = dic[p.key]
            if p.type == Parameter.Type.t_struct:
                value = struce2int(value)
            else:
                if Parameter.Type.t_float in p.type:
                    value = float(value)
                else:
                    if p.type == Parameter.Type.t_int or p.type == Parameter.Type.t_reserved or p.type == Parameter.Type.t_percentage:
                        #print("getusefull keys: ",p.key,value)
                        value = int(float(value))
                    else:
                        continue

            lst_value.append(value)
            lst_key.append(p.key)
    return lst_value,lst_key


def result2lst(result,plst,expect):
    xlst = []
    ylst = []
    xylst = []
    keys = []
    for iops, dic_ssd, dic_worload, path in result:
        dic = dic_ssd
        dic.update(dic_worload)
        values, keys = getUsefullKeys(dic, plst, expect)
        if iops == 'inf':
            # print("inf------")
            continue
        xlst.append(values)
        ylst.append([float(iops)])
        xylst.append([values, [float(iops)]])
        keys = keys
    return xlst,ylst,keys


from torch.utils.data import Dataset, DataLoader
import torch.optim as optim
# 自定义数据集类
class CustomDataset(Dataset):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]