import os
import xml.etree.ElementTree as ET

import pandas as pd


def extract_values_from_xml(xml_file):
    # 解析 XML 文件
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 定义要收集的节点名称
    nodes_to_collect = ['IOPS_Read', 'IOPS_Write', 'Bandwidth_Read', 'Bandwidth_Write']

    # 初始化字典来存储节点值
    collected_values = {}

    # 遍历 XML 文件中的每个子元素
    for elem in root.iter():
        # 检查节点是否在我们感兴趣的节点列表中
        if elem.tag in nodes_to_collect:
            # 存储节点值
            collected_values[elem.tag] = float(elem.text)  # 将值转换为浮点数（如果适用）

    return collected_values
def xml2dict(xml_file,params,seed):
    # 解析 XML 文件
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for elem in root.iter():
        # 检查当前元素是否为叶节点
        if len(elem) == 0:
            if elem.tag=='Seed':
                params[seed]=elem.text
            else:
                params[elem.tag]=elem.text
    return params
workspace_path = "workspace"
i= 0
paramslst=[]
for item in os.listdir(workspace_path):
    #print(item)
    path_ssdcfg=workspace_path+"/"+item+"/ssdconfig.xml"
    path_workload = workspace_path + "/" + item + "/workload.xml"
    path_result=workspace_path+"/"+item+"/workload_scenario_1.xml"
    if not os.path.exists(path_result):
        continue
    params =  xml2dict(path_ssdcfg, {},"ssdSeed")
    params = xml2dict(path_workload, params,"workloadSeed")
    print(params)
    result = extract_values_from_xml(path_result)
    #print(result)
    params['id']=item
    for key,value in result.items():
        params[key]=value
    paramslst.append(params)
    i = i+1
    #if i>3: break
df = pd.DataFrame(paramslst)
df.to_excel("result.xlsx", index=False)