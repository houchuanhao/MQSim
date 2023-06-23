from script.tools import *

path_ssd = xml_ssdcfg
path_workload = xml_workload

tree_ssd , root_ssd = getTree(path_ssd)
tree_workload , root_workload = getTree(path_workload)


def genWorkspace():

    return
def getRange(key):
    struct = {"Channel_IDs":"Flash_Channel_Count",
              "Chip_IDs":"Chip_No_Per_Channel",
              "Die_IDs":"Die_No_Per_Chip",
              "Plane_IDs":"Plane_No_Per_Die"}
    #if key in struct.keys():
    min = 0
    max = 0
    default = 0
    return min,max,default

dic_ssd = root2dic(root_ssd)
dic_ssd['Seed_ssd']=dic_ssd['Seed']
dic_worload = root2dic(root_workload)

lst_ssd = []
lst_workload = []

dic = dic_ssd
dic.update(dic_worload)

dic2xlsx(dic, "config.xlsx")

