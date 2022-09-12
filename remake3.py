import glob
import xml.dom.minidom
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os
import xml.etree.ElementTree as ET
import glob
# 定义待批量裁剪图像的路径地址
from numpy.distutils.fcompiler import none

IMAGE_INPUT_PATH = r'E:\\dataset\\SSDD SAR dataset1\\SSDD SAR dataset\\data and label\\JPEGImages'
XML_INPUT_PATH = r'E:\\dataset\\SSDD SAR dataset1\\SSDD SAR dataset\\data and label\\Annotations'
# 定义裁剪后的图像存放地址
IMAGE_OUTPUT_PATH = r'E:\\datasets\\SSDD SAR dataset\\old\\imgs'
XML_OUTPUT_PATH = r'E:\\datasets\\SSDD SAR dataset\\old\\xml'
imglist = os.listdir(IMAGE_INPUT_PATH)
xmllist = os.listdir(XML_INPUT_PATH)
for i in range(len(imglist)):
    # 每个图像全路径
    image_input_fullname = IMAGE_INPUT_PATH + '/' + imglist[i]
    xml_input_fullname = XML_INPUT_PATH + '/' + xmllist[i]
    image_output_fullname = IMAGE_OUTPUT_PATH + '/' + imglist[i]
    xml_output_fullname = XML_OUTPUT_PATH + '/' + xmllist[i]

    dom = xml.dom.minidom.parse(xml_input_fullname)
    root = dom.documentElement
    # 读取标注目标框
    objects = root.getElementsByTagName("bndbox")

    for object in objects:
        xmin = object.getElementsByTagName("xmin")
        xmin_data = round(float(xmin[0].firstChild.data))
        # xmin[0].firstChild.data =str(int(xmin1 * x))
        ymin = object.getElementsByTagName("ymin")
        ymin_data = round(float(ymin[0].firstChild.data))
        xmax = object.getElementsByTagName("xmax")
        xmax_data = round(float(xmax[0].firstChild.data))
        ymax = object.getElementsByTagName("ymax")
        ymax_data = round(float(ymax[0].firstChild.data))
        img = cv2.imread(image_input_fullname)
        height, width = img.shape[:2]

        min_side = 544
        scale = max(width,height) / min_side
        new_w,new_h = int(width/scale),int(height/scale)
        resize_img = cv2.resize(img,(new_w,new_h))

        if new_w % 2 != 0 and new_h % 2 == 0:
            top, bottom, left, right = (min_side - new_h) / 2, (min_side - new_h) / 2, (min_side - new_w) / 2 + 1, (
                        min_side - new_w) / 2
        elif new_h % 2 != 0 and new_w % 2 == 0:
            top, bottom, left, right = (min_side - new_h) / 2 + 1, (min_side - new_h) / 2, (min_side - new_w) / 2, (
                        min_side - new_w) / 2
        elif new_h % 2 == 0 and new_w % 2 == 0:
            top, bottom, left, right = (min_side - new_h) / 2, (min_side - new_h) / 2, (min_side - new_w) / 2, (
                        min_side - new_w) / 2
        else:
            top, bottom, left, right = (min_side - new_h) / 2 + 1, (min_side - new_h) / 2, (min_side - new_w) / 2 + 1, (
                        min_side - new_w) / 2
        pad_img = cv2.copyMakeBorder(resize_img, int(top), int(bottom), int(left), int(right), cv2.BORDER_CONSTANT, value=[0, 0, 0])

        tree = ET.parse(xml_input_fullname)
        root = tree.getroot()
        newsize = None
        # 获取全部子节点，为防止写入修改信息后节点改变
        annos = [anno for anno in root.iter()]
        for i, anno in enumerate(annos):
            # 修改xml文件中图像尺寸信息
            # 计算x轴,y轴位置变化率

            if newsize != None:
                if 'width' in anno.tag:
                    oldwidth = float(anno.text)
                    anno.text = str(newsize[0])
                    sizechangerate_x = newsize[0] / oldwidth
                if 'height' in anno.tag:
                    oldheight = float(anno.text)
                    anno.text = str(newsize[1])
                    sizechangerate_y = newsize[1] / oldheight

                    if 'object' in anno.tag:
                        for element in list(anno):
                            oldcls = newcls = None
                            # 这是之前教程中修改类别名用到的，
                            # 此处oldcls和newcls均输入为同一个值即可，例如均为None
                            if oldcls != newcls:
                                if 'name' in element.tag:
                                    if element.text == oldcls:
                                        element.text = newcls
                                        print(os.path.basename(xml_input_fullname) + ' change the class name')
                                break
                            # 修改位置信息
                            if newsize != None:
                                if 'bndbox' in element.tag:
                                    for coordinate in list(element):
                                        if 'xmin' in coordinate.tag:
                                            coordinate.text = str(int(int(coordinate.text) * sizechangerate_x))
                                        if 'xmax' in coordinate.tag:
                                            coordinate.text = str(int(int(coordinate.text) * sizechangerate_x))
                                        if 'ymin' in coordinate.tag:
                                            coordinate.text = str(int(int(coordinate.text) * sizechangerate_y))
                                        if 'ymax' in coordinate.tag:
                                            coordinate.text = str(int(int(coordinate.text) * sizechangerate_y))

                # 写入修改信息，覆盖原xml文件
                tree = ET.ElementTree(root)
                tree.write(xml_output_fullname, encoding="utf-8", xml_declaration=True)







        # scale1 = 544 / height
        # scale2 = 544 / width
        # height, width = pad_img.shape[:2]
        # # height = 544
        # # width = 544
        # # 更新xml
        # width_xml = root.getElementsByTagName("width")
        # width_xml[0].firstChild.data = width
        # height_xml = root.getElementsByTagName("height")
        # height_xml[0].firstChild.data = height
        # # print(scale1)
        # # print(scale2)
        # xmin[0].firstChild.data = round(xmin_data * scale2)
        # ymin[0].firstChild.data = round(ymin_data * scale1)
        # xmax[0].firstChild.data = round(xmax_data * scale2)
        # ymax[0].firstChild.data = round(ymax_data * scale1)
        #
        # # 另存更新后的文件
        # with open(xml_output_fullname, 'w') as f:
        #     dom.writexml(f, addindent='  ', encoding='utf-8')
        #
        # # 测试缩放效果
        # img = cv2.resize(pad_img, (width, height))
        #
        # # xmin, ymin, xmax, ymax分别为xml读取的坐标信息
        # left_top = (int(xmin_data * scale2), int(ymin_data * scale1))
        # right_down = (int(xmax_data * scale2), int(ymax_data * scale1))
        # cv2.rectangle(img, left_top, right_down, (255, 0, 0), 1)
    cv2.imwrite(image_output_fullname, pad_img)
