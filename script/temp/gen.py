import os
import xml.etree.ElementTree as ET
import pandas as pd
import random
import pdb
def set_value_random_ssd(parameterCfg):
    parameters={}
        # 遍历参数
    for index, row in parameterCfg.iterrows():
        #print(row)
        param_id = row['id']
        param_key = row['Parameter']
        param_default = row['Default Value']
        param_type = row['type']
        param_min = row['min']
        param_max = row['max']
        param_set = str(row['set'])
        if(param_type)=='int':
            param_default = int(param_default)
            param_min= int(param_min)
            param_max = int(param_max)
        if param_set !='NaN':
            param_set =param_set.replace(" ","")
            param_set = param_set.replace("{","")
            param_set = param_set.replace("}", "")
            param_set = param_set.split(",")
        # 处理不需要随机值的参数
        if param_type == 'ignore':
            random_value = param_default
            #print("ignore",param_key)
        # 处理布尔类型参数
        elif param_type == 'Boolean':
            random_value = random.choice([True, False])
        # 处理枚举类型参数
        elif param_type == 'enumeration':
            #random_value = param_name  # 默认取默认值
            random_value = random.choice(param_set)
        # 处理其他类型参数
        else:
            if param_type == 'double':
                random_value = random.uniform(param_min, param_max)
            elif param_type == 'int':
                if param_default>100 and param_default% 256 ==0:
                    z = int(param_default/256)
                    a = int(z*4)
                    b = int(max(1,z/4))
                    #print(a,b)
                    #pdb.set_trace()
                    random_value = random.randint(b, a)
                else:
                    random_value = random.randint(param_min, param_max)
            else:
                print(f"Unsupported parameter type for '{param_key}'. Skipping.")
                continue
        parameters[param_key] = random_value
    return parameters
def xml2xlsx(xml,xlsx):
    # 1. 读取 XML 文件并解析
    tree = ET.parse(xml)
    root = tree.getroot()
    # 2. 遍历所有叶子节点，并将叶子节点和默认值保存到字典中
    parameters = {}
    for elem in root.iter():
        if len(elem) == 0:  # 只处理叶子节点
            parameters[elem.tag] = elem.text
    # 3. 将字典保存到 Excel 文件中
    df = pd.DataFrame(list(parameters.items()), columns=['Parameter', 'Value'])
    df.to_excel(xlsx, index=False)
    print("helo")

def gen_ssdcfg(tree,root,parameters,path):
    # 5. 根据字典为每个叶子节点重新赋值，修改后保存到 new.xml 中
    for elem in root.iter():
        if len(elem) == 0:  # 只处理叶子节点
            elem.text = str(parameters[elem.tag])
    tree.write(path)
    return parameters


# workload 部分
# 生成workload中一个io flow的字典
def set_value_workload(parameterCfg, parasSsd):
    parameters={}
        # 遍历参数
    for index, row in parameterCfg.iterrows():
        #print(row)
        param_id = row['id']
        param_key = row['Parameter']
        param_default = row['Default Value']
        param_type = row['type']
        param_min = row['min']
        param_max = row['max']
        param_set = str(row['set'])
        parameters[param_key] = param_default
        if (param_type) == 'int':
            param_default = int(param_default)
            param_min = int(param_min)
            param_max = int(param_max)
        if param_set != 'NaN':
            param_set = param_set.replace(" ", "")
            param_set = param_set.replace("{", "")
            param_set = param_set.replace("}", "")
            param_set = param_set.split(",")
            # 处理不需要随机值的参数
        if param_type == 'ignore':
            random_value = param_default
            # print("ignore",param_key)
            # 处理布尔类型参数
        elif param_type == 'Boolean':
            random_value = random.choice([True, False])
            # 处理枚举类型参数
        elif param_type == 'enumeration':
            # random_value = param_name  # 默认取默认值
            random_value = random.choice(param_set)
            # 处理其他类型参数
        else:
            if param_type == 'double':
                random_value = random.uniform(param_min, param_max)
            elif param_type == 'int':
                random_value = random.randint(param_min, param_max)
            else:
                #print(f"Unsupported parameter type for '{param_key}'. Skipping.")
                continue
    #Flash_Channel_Count     Chip_No_Per_Channel     Die_No_Per_Chip     Plane_No_Per_Die
    #Channel_IDs    Chip_IDs    Die_IDs     Plane_IDs
    parameters['Channel_IDs'] = ','.join(map(str, range(int(parasSsd['Flash_Channel_Count']))))
    parameters['Chip_IDs'] = ','.join(map(str, range(int(parasSsd['Chip_No_Per_Channel']))))
    parameters['Die_IDs'] = ','.join(map(str, range(int(parasSsd['Die_No_Per_Chip']))))
    parameters['Plane_IDs'] = ','.join(map(str, range(int(parasSsd['Plane_No_Per_Die']))))
    parameters['Average_Request_Size'] = random.randint(2,22)
    return parameters
#
def gen_workloadcfg(paramters,path):
    # 创建根节点
    root = ET.Element("MQSim_IO_Scenarios")
    # 创建 IO_Scenario 子节点
    io_scenario = ET.SubElement(root, "IO_Scenario")
    # 创建 IO_Flow_Parameter_Set_Synthetic 子节点
    io_flow_param_set_synthetic = ET.SubElement(io_scenario, "IO_Flow_Parameter_Set_Synthetic")
    for key,value in paramters.items():
        node = ET.SubElement(io_flow_param_set_synthetic, str(key))
        node.text = str(value)
    tree = ET.ElementTree(root)
    # 将 XML 写入文件
    tree.write(path, encoding="utf-8", xml_declaration=True, short_empty_elements=False)


def save_dict_to_excel(data_dict, file_path):
    # 将字典转换为 DataFrame
    df = pd.DataFrame(list(data_dict.items()), columns=['Key', 'Value'])

    # 将 DataFrame 保存到 Excel 文件
    df.to_excel(file_path, index=False)
def main():
    # 1. 读取 XML 文件并解析
    tree = ET.parse('ssdconfig.xml')
    root = tree.getroot()
    # 4. 为字典中的每个参数赋随机值
    parameterCfg = pd.read_excel("config.xlsx",sheet_name="ssd")
    paramSsd = set_value_random_ssd(parameterCfg)
    gen_ssdcfg(tree,root,paramSsd,"ezssd.xml")
    xml2xlsx("ezssd.xml","ezssd.xlsx")
    # 生成worklload.xml
    parameterCfg = pd.read_excel("config.xlsx", sheet_name="workload")
    paramters = set_value_workload(parameterCfg, paramSsd)
    gen_workloadcfg(paramters,"workloadez.xml")
    return
def checkPara(parameters_ssd,parameters_workload):
    rebuild = False
    if parameters_ssd['Caching_Mechanism'] == 'SIMPLE' :
        parameters_ssd['EQUAL_PARTITIONING']='EQUAL_PARTITIONING'
    c = 1
    clst = ['Flash_Channel_Count','Chip_No_Per_Channel','Die_No_Per_Chip',
            'Plane_No_Per_Die','Block_No_Per_Plane','Page_No_Per_Block']
    for key in clst:
        c = c * int(parameters_ssd[key])
        #print(key," :",parameters_ssd[key])
    if c> 13 *5 * 1 * 11 * 7000 * 150:
        rebuild = True
    return parameters_ssd,parameters_workload,rebuild
def genworkspace(begin=0):
    i = begin
    tree = ET.parse('ssdconfig.xml')
    root = tree.getroot()
    parameterCfg_ssd = pd.read_excel("config.xlsx", sheet_name="ssd")
    parameterCfg_workload = pd.read_excel("config.xlsx", sheet_name="workload")
    os.system("rm workspace/* -rf")
    while(1):
        parameters_ssd = set_value_random_ssd(parameterCfg_ssd)
        parameters_workload = set_value_workload(parameterCfg_workload,parameters_ssd)
        parameters_ssd,parameters_workload,rebuild = checkPara(parameters_ssd,parameters_workload)
        if rebuild:
            continue
        os.system("mkdir workspace/" + str(i))
        gen_ssdcfg(tree, root, parameters_ssd, "workspace/"+str(i)+"/ssdconfig.xml")
        gen_workloadcfg(parameters_workload,"workspace/"+str(i)+"/workload.xml")
        save_dict_to_excel(parameters_ssd,"workspace/"+str(i)+"/ssdconfig.xlsx")
        save_dict_to_excel(parameters_workload, "workspace/" + str(i) + "/workload.xlsx")
        os.system("pwd")
        os.system("cd workspace/"+str(i)+"/")
        os.system("pwd")
        os.system("../../../../MQSim -i ssdconfig.xml -w workload.xml")
        os.system("cd ../..")
        i = i +1
        if i>3:
            break
genworkspace(0)

    