from script.tools import tools
import os

def collection(folder_path="workspace1",lst = None):
    rLst = []
    if lst != None:
        rLst = lst
    for f in os.scandir(folder_path):
        if f.is_dir():
            xmlpath= f.path+"/workload_scenario_1.xml"
            if not os.path.exists(xmlpath):
                continue
            ssd = f.path + "/" + tools.xml_ssdcfg
            workload = f.path + "/" + tools.xml_workload
            dic_ssd,dic_worload = tools.xml2dic(ssd,workload)
            tree,root = tools.getTree(xmlpath)
            iops = tools.getext(root,"IOPS")
            rLst.append([iops,dic_ssd,dic_worload,f.path])
            #print(iops)
    print(len(rLst))
    return (rLst)
#collection()

