from script.tools import *

path_ssd = xml_ssdcfg
path_workload = xml_workload

tree_ssd , root_ssd = getTree(path_ssd)
tree_workload , root_workload = getTree(path_workload)

dic_ssd = root2dic(root_ssd)


