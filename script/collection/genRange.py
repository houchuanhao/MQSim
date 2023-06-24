from enum import Enum
import random

from script.tools import *

class Type:
    t_float = "float"
    t_int = "int"
    t_ignore = "ignore"
    t_percentage = "percentage"
    t_reserved = "reserved"  # 保留 min_max
    t_struce = "struce"
    t_modifed = "modifed" # 保留value

class Parameter:

    struct = {"Channel_IDs":"Flash_Channel_Count",
              "Chip_IDs":"Chip_No_Per_Channel",
              "Die_IDs":"Die_No_Per_Chip",
              "Plane_IDs":"Plane_No_Per_Die"}
    def __init__(self,key=None,default=None,type=None,min=None,max=None,m=None,value = None):
        self.key = key
        self.default = default
        self.type = type
        self.min = min
        self.max = max
        self.m = m
        self.value = value
        if isinstance(key,list):
            lst = key
            #print(lst)
            self.key = lst[0]
            self.default = lst[1]
            self.type = lst[2]
            self.min = lst[3]
            self.max = lst[4]
            self.value = lst[6]
            self.m = lst[5]

    def getRange(self):
        if self.type == Type.t_reserved or self.type == Type.t_modifed:
            return
        if self.type == Type.t_percentage:
            self.max = 100
            self.min = 0
        if self.type == Type.t_int:
            self.default = int(self.default)
            if self.default % 256 == 0:
                self.min = int(self.default / 256 / 16)
                self.max = int(self.default / 256 * 16)
                self.m = 256
            if self.default >= 100:
                self.max = int(self.default * 10)
                self.min = int(self.default / 10)
                self.m = None
            else:
                self.min = int(1)
                self.max = int(self.default * 10)
            return
        if self.type == Type.t_float:
            self.default = float(self.default)
            self.max = self.default * 10
            self.min = self.default / 10
            self.m = None
            return
        #print(self.key," :",self.default," ",self.type)
    def r2lst(self):
        return [self.key,self.default,self.type,self.min,self.max,self.value, self.m,]

    @staticmethod
    def lst2parameter(lst):
        p = Parameter(lst)
        return p
    def getRandValue(self,structMax = 32):
        if self.type == Type.t_ignore:
            self.value = self.default
            return
        if self.type == Type.t_modifed:
            self.value = self.value
            return
        if self.type == Type.t_float:
            self.value = random.uniform(self.min,self.max)
            #print(self.key, " ", type(self.min), self.min, self.max)
            return
        if self.type == Type.t_int or self.type == Type.t_percentage or self.type ==Type.t_reserved:

            try:
                self.value = int(random.randint(self.min,self.max))
            except Exception as e:
                print(self.key," ",type(self.min),self.min, self.max)
            return
        if self.type == Type.t_struce:
            k = int(random.randint(1,structMax))
            #print(self.key," ",k)
            numbers = random.sample(range(structMax), k)
            numbers = sorted(numbers)
            s = str(numbers[0])
            self.value = str(numbers).replace('[','').replace(']','')
            return
        if self.type == None:
            print("None type"," ",self.key)
            return
        print("error type :" + self.key)

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
    dic_workload = root2dic(root_workload,{})
    lst = xlsx2lst(xlsx_config)
    parameters_ssd = []
    parameters_workload = []
    for key, value in dic_ssd.items():
        #print(key)
        row = getrow(lst,key)
        #p = Parameter(key,value,row[2])
        p = Parameter(row)
        p.getRange()
        p.getRandValue()
        parameters_ssd.append(p.r2lst())

    print("--------")
    for key, value in dic_workload.items():
        #print(key)
        row = getrow(lst,key)
        p = Parameter(row)  # key default type min max
        p.getRange()
        p.getRandValue()
        #print(p.r2lst())
        parameters_workload.append(p.r2lst())
    lst2excel(parameters_ssd, "ssdRange.xlsx")
    lst2excel(parameters_workload, "workloadRange.xlsx")
    # parameters_ssd parameters_workload 中存放range了
main()
