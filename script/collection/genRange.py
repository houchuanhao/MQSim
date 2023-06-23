from script.tools import *


class Parameter:

    struct = {"Channel_IDs":"Flash_Channel_Count",
              "Chip_IDs":"Chip_No_Per_Channel",
              "Die_IDs":"Die_No_Per_Chip",
              "Plane_IDs":"Plane_No_Per_Die"}
    def __init__(self,key=None,default=None,type=None,min=None,max=None,m=None):
        self.key = key
        self.default = default
        self.type = type
        self.min = min
        self.max = max
        self.m = m
    def __int__(self,lst):
        self.key = lst[0]
        self.default = lst[1]
        self.type = lst[2]
        self.min = lst[3]
        self.max = lst[4]
        self.m = lst[5]
    def getRange(self):
        if self.type == "percentage":
            self.max = 100
            self.min = 0
        if self.type == "int":
            self.default = int(self.default)
            if self.default % 256 == 0:
                self.min = int(self.default / 256 / 16)
                self.max = int(self.default / 256 * 16)
                self.m = 256
            if self.default > 100:
                self.max = int(self.default * 10)
                self.min = int(self.default / 10)
                self.m = None
            return
        if self.type == "float":
            self.default = float(self.default)
            self.max = self.default * 10
            self.min = self.default / 10
            self.m = None
            return
        print(self.key," :",self.default," ",self.type)
    def r2lst(self):
        return [self.key,self.default,self.type,self.min,self.max,self.m]

    @staticmethod
    def lst2parameter(lst):
        p = Parameter(lst)
        return p

def getrow(lst,key):
    for data in lst:
        if data[0]==key:
            return data
    return None

def main():
    path_ssd = xml_ssdcfg
    path_workload = xml_workload
    tree_ssd , root_ssd = getTree(path_ssd)
    tree_workload , root_workload = getTree(path_workload)
    dic_ssd = root2dic(root_ssd,{})
    #dic_ssd['ssd_Seed'] = dic_ssd['Seed']
    dic_workload = root2dic(root_workload,{})
    #dic_workload['workload_Seed'] = dic_workload['Seed']
    lst = xlsx2lst(xlsx_config)
    parameters_ssd = []
    parameters_workload = []
    for key, value in dic_ssd.items():
        #print(key)
        row = getrow(lst,key)
        p = Parameter(key,value,row[2])
        p.getRange()
        parameters_ssd.append(p.r2lst())
    print("--------")
    for key, value in dic_workload.items():
        #print(key)
        row = getrow(lst,key)
        p = Parameter(key,value,row[2])  # key default type min max
        p.getRange()
        parameters_workload.append(p.r2lst())
    #lst2excel(parameters,"testrange.xlsx")
    # parameters_ssd parameters_workload 中存放range了

main()
