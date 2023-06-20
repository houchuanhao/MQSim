from script.tools import *
treeOri,rootOri = getTree("./"+xml_ssdcfg) # sensitive下的配置文件
dicOri = root2dic(rootOri)
collection = "collection.xlsx"
i=0
elst=[]
tittle = ['key','value','value*10','default_iops','modifed_iops',]
elst.append(tittle)
for key,value in dicOri.items():
    if value== None or is_numeric(value)==0:
        continue
    p_ssd = "workspace/" + key + "/" + xml_ssdcfg
    p_workload = "workspace/" + key + "/" + xml_workload
    p_out = "workspace/" + key + "/" + xml_out

    if value != None and is_numeric(value) > 0:
        print("pout",p_out)
        tree,root = getTree(p_ssd)
        dic = root2dic(root,{})
        lst = []
        lst.append(key)
        lst.append(value)
        lst.append(getext(root,key))
        lst.append('37293')
        iops = 0
        try:
            o_tree,o_root = getTree(p_out)
            iops = getext(o_root, 'IOPS')
        except Exception as e:
            print("nowork ",p_out)
        lst.append(iops)
        elst.append(lst)

    print("111",lst)
lst2excel(elst,collection)