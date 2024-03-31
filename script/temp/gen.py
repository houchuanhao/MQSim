import xml.etree.ElementTree as ET
import pandas as pd
import random
import pdb
def setValueRandom(parameters,data_model):
        # 遍历参数
    for index, row in data_model.iterrows():
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

def main():
    # 1. 读取 XML 文件并解析
    tree = ET.parse('ssdconfig.xml')
    root = tree.getroot()
    # 4. 为字典中的每个参数赋随机值
    data = pd.read_excel("config.xlsx")
    parameters = {}
    setValueRandom(parameters,data)
    # 5. 根据字典为每个叶子节点重新赋值，修改后保存到 new.xml 中
    for elem in root.iter():
        if len(elem) == 0:  # 只处理叶子节点
            elem.text = str(parameters[elem.tag])
    tree.write('new.xml')
main()

    