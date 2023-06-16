import xml.etree.ElementTree as ET

def travel(root,l=0):
    s = ""
    for i in range(l):
        s = s + "   "
    for child in root:
        if len(child)>0:
            print(s, child.tag)
            travel(child,l+1)
        else:
            print(s,child.tag,":  ",child.text)
def getext(root,key):
    for child in root:
        if len(child)>0:
            t = getext(child,key)
            if t!=None:
                return t
        else:
            if(child.tag==key):
                return child.text
    return None
            #print(s,child.tag,":  ",child.text)
    # 读取XML文件
def setext(root,key,value):
    for child in root:
        if len(child)>0:
            t = setext(child,key,value)
            if t!=None:
                return 1
        else:
            if(child.tag==key):
                child.text = value
                return 1
    return None
tree = ET.parse('ssdconfig.xml')
root = tree.getroot()

travel(root)
print(getext(root,"Page_Metadat_Capacity"))
setext(root,"Page_Metadat_Capacity","1234")
print(getext(root,"Page_Metadat_Capacity"))
    # 将修改后的内容写回到文件
tree.write('example.xml')

#setssd()