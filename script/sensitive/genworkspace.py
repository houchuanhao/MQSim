import os

from xlrd.xlsx import ET

from script import tools
#treeOri,rootOri
os.system("rm -rf workspace")
os.system("mkdir workspace")
treeSSD,rootSSD = tools.getTree("./" + tools.xml_ssdcfg)
treeWorkload,rootWorkload = tools.getTree("./"+tools.xml_workload)

dicWorkload = tools.root2dic(rootWorkload)
dicOri = tools.root2dic(rootSSD)
for key,value in dicOri.items():
    p_ssd = "workspace/" + key + "/" + tools.xml_ssdcfg
    p_workload = "workspace/" + key + "/" + tools.xml_workload
    if value != None and tools.is_numeric(value):
        os.system("chmod +rw *")
        os.system("mkdir workspace/"+key)
        os.system("cp ./workload.xml workspace/"+key+"/")
        os.system("cp ./ssdconfig.xml workspace/"+key+"/")
        os.system("cp  ../link/run workspace/" + key + "/run")
        os.system("cp  ../link/run.py workspace/" + key + "/run.py")
        v = 0
        if tools.is_numeric(value) == 1:
            v = int(value)
            v = int(v*10)
            v = str(v)
        else:
            v = float(value)
            v= v *10
            v = str(v)
        tree,root = tools.getTree(p_ssd)
        tools.setext(root,key,v)
        tree = ET.ElementTree(root)
        tree.write(p_ssd)
