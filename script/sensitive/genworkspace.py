import os

from script.tools import *
#treeOri,rootOri
os.system("rm -rf workspace")
os.system("mkdir workspace")
treeSSD,rootSSD = getTree("./" + xml_ssdcfg)
treeWorkload,rootWorkload = getTree("./"+xml_workload)

dicWorkload = root2dic(rootWorkload)
dicOri = root2dic(rootSSD)
for key,value in dicOri.items():
    p_ssd = "workspace/" + key + "/" + xml_ssdcfg
    p_workload = "workspace/" + key + "/" + xml_workload
    if value != None and is_numeric(value):
        os.system("chmod +rw *")
        os.system("mkdir workspace/"+key)
        os.system("cp ./workload.xml workspace/"+key+"/")
        os.system("cp ./ssdconfig.xml workspace/"+key+"/")
        os.system("cp  ../link/run workspace/" + key + "/run")
        os.system("cp  ../link/run.py workspace/" + key + "/run.py")
        v = 0
        if is_numeric(value) == 1:
            v = int(value)
            v = int(v/10)
            v = str(v)
        else:
            v = float(value)
            v= v /10
            v = str(v)
        tree,root = getTree(p_ssd)
        setext(root,key,v)
        tree = ET.ElementTree(root)
        tree.write(p_ssd)
