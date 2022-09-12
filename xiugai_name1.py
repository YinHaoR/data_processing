import os
import os.path
from xml.etree.ElementTree import parse, Element
#批量修改xml中内容
def test():
    path = "E:\\shipdata\\xml\\"#xml文件所在的目录
    files = os.listdir(path)  # 得到文件夹下所有文件名称
    s = []
    for xmlFile in files:  # 遍历文件夹
        if not os.path.isdir(xmlFile):  # 判断是否是文件夹,不是文件夹才打开
            print
            xmlFile
            pass
        path = "E:\\shipdata\\xml\\"
        print(xmlFile)
        path1 = "E:\\shipdata\\xml\\"+xmlFile#定位当前处理的文件的路径
        newStr = os.path.join(path, xmlFile)
        name = "ship"
        dom = parse(newStr)  ###最核心的部分,路径拼接,输入的是具体路径
        root = dom.getroot()
        print(root)
        for obj in root.iter('object'):#获取object节点中的name子节点
            obj.find('name').text=name
            name1 = obj.find('name').text#修改
            print(name1)
        dom.write(path1, xml_declaration=True)#保存到指定文件
        pass
if __name__ == '__main__':
    test()