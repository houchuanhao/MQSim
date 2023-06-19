from script.tools import *
treeOri,rootOri = getTree("../"+xml_ssdcfg) # script下的配置文件


dicOri = root2dic(rootOri)
for key,value in dicOri.items():
    p_ssd = "workspace/" + key + "/" + xml_ssdcfg
    p_workload = "workspace/" + key + "/" + xml_workload
    if value != None and is_numeric(value)>0:
        os.system("../../MQSim -i "+p_ssd + " -w "+ p_workload )