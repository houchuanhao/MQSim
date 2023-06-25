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
    def getRandValue(self,structMax=None):

        if self.type == Type.t_ignore:
            self.value = self.default
            return
        if self.type == Type.t_modifed:
            self.value = self.value
            return
        if self.type == Type.t_float:
            self.value = random.uniform(self.min,self.max)
            #print("test float: ",self.key, " ",self.value, self.min, self.max)
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


path_ssd = xml_ssdcfg
path_workload = xml_workload


def gen_run():
    maxC = 999999999999999999999999  # 大于这个就不能运行 不能运行的下界
    minC = 0  # 小于这个一定能运行 能运行的上界
    i = 0
    try:
        os.system("rm -rf workspace/")
    except:
        print("rm -rf workspace 失败")
    os.system("mkdir workspace")
    while(1):
        tree_ssd, root_ssd = getTree(path_ssd)
        tree_workload, root_workload = getTree(path_workload)
        dic_ssd = root2dic(root_ssd, {})
        dic_workload = root2dic(root_workload, {})
        lst_ssd = xlsx2lst(xlsx_config, "ssd")
        lst_workload = xlsx2lst(xlsx_config, "workload")
        # dic_ssd_ref 和dic_workload_ref 是参考模板
        # lst_ssd 和lst_workload 记录参数的类型、默认值等
        # parameters_ssd parameters_workload 中存放range了
        parameters_ssd = []
        parameters_workload = []

        for key, value in dic_ssd.items():
            row = getrow(lst_ssd,key)
            p = Parameter(row)
            p.getRange()
            p.getRandValue()
            dic_ssd[key] = p.value
            parameters_ssd.append(p.r2lst())
        for key, value in dic_workload.items():
            row = getrow(lst_workload,key)
            p = Parameter(row)  # key default type min max
            p.getRange()
            if key in Parameter.struct.keys():
                p.getRandValue(dic_ssd[Parameter.struct[key]])
            else:
                p.getRandValue()
            dic_workload[key] = p.value
            parameters_workload.append(p.r2lst())

        c = 1
        clst = ['Flash_Channel_Count','Chip_No_Per_Channel','Die_No_Per_Chip',
                'Plane_No_Per_Die','Block_No_Per_Plane','Page_No_Per_Block','Page_Capacity']
        for key in clst:
            c = c * int(dic_ssd[key])
            print(key," :",dic_ssd[key])
        if c > maxC:
            continue
        os.system("mkdir workspace/" + str(i))

        dic2root(dic_ssd,root_ssd)
        path = "workspace/"+str(i)+"/"+xml_ssdcfg
        print("path= ------",path)
        tree_ssd.write(path)

        dic2root(dic_workload,root_workload)
        path = "workspace/"+str(i)+"/"+xml_workload
        tree_workload.write(path)

        lst2excel(parameters_ssd, "workspace/"+str(i)+"/ssdRange.xlsx")
        lst2excel(parameters_workload, "workspace/"+str(i)+"/workloadRange.xlsx")

        os.system("cp  ../link/run workspace/" + str(i) + "/run")
        os.system("cp  ../link/run.py workspace/" + str(i) + "/run.py")
        try:
            os.system("../../MQSim -i workspace/"+str(i) + "/"+xml_ssdcfg + " -w workspace/"+str(i)+"/"+xml_workload)
        except:
            print(i,"error")
        if(os.path.exists("workspace/"+str(i)+"/workload_scenario_1.xml")): # 能运行
            if minC < c:
                minC = c
                print("minC ",minC)
        else: # 不能运行
            #os.system("rm -rf workspace/"+str(i))
            if maxC > c:
                maxC = c
                print("maxC: ",maxC)
        i = i + 1


def main():
    gen_run()
main()

