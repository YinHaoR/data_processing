import glob
import xml.dom.minidom
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os
import xml.etree.ElementTree as ET
import glob
# 定义待批量裁剪图像的路径地址
IMAGE_INPUT_PATH = r'E:\shipdata\xml-1024\images'
XML_INPUT_PATH = r'E:\\shipdata\\xml-1024'
# 定义裁剪后的图像存放地址
IMAGE_OUTPUT_PATH = r'E:\\shipdata\\'
XML_OUTPUT_PATH = r'E:\\shipdata\\'
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

        # min_side = 544
        # scale = max(width,height) / min_side
        # new_w,new_h = int(width/scale),int(height/scale)
        # resize_img = cv2.resize(img,(new_w,new_h))
        #
        # if new_w % 2 != 0 and new_h % 2 == 0:
        #     top, bottom, left, right = (min_side - new_h) / 2, (min_side - new_h) / 2, (min_side - new_w) / 2 + 1, (
        #                 min_side - new_w) / 2
        # elif new_h % 2 != 0 and new_w % 2 == 0:
        #     top, bottom, left, right = (min_side - new_h) / 2 + 1, (min_side - new_h) / 2, (min_side - new_w) / 2, (
        #                 min_side - new_w) / 2
        # elif new_h % 2 == 0 and new_w % 2 == 0:
        #     top, bottom, left, right = (min_side - new_h) / 2, (min_side - new_h) / 2, (min_side - new_w) / 2, (
        #                 min_side - new_w) / 2
        # else:
        #     top, bottom, left, right = (min_side - new_h) / 2 + 1, (min_side - new_h) / 2, (min_side - new_w) / 2 + 1, (
        #                 min_side - new_w) / 2
        # pad_img = cv2.copyMakeBorder(resize_img, int(top), int(bottom), int(left), int(right), cv2.BORDER_CONSTANT, value=[0, 0, 0])
        # height,width = pad_img.shape[:2]

        # scale1 = 544 / height
        # scale2 = 544 / width
        height = 1024
        width = 1024
        # 更新xml
        width_xml = root.getElementsByTagName("width")
        width_xml[0].firstChild.data = width
        height_xml = root.getElementsByTagName("height")
        height_xml[0].firstChild.data = height
        # print(scale1)
        # print(scale2)
        # xmin[0].firstChild.data = round(xmin_data * scale)
        # ymin[0].firstChild.data = round(ymin_data * scale-int(right))
        # xmax[0].firstChild.data = round(xmax_data * scale-int(top))
        # ymax[0].firstChild.data = round(ymax_data * scale-int(bottom))

        # 另存更新后的文件
        with open(xml_output_fullname, 'w') as f:
            dom.writexml(f, addindent='  ', encoding='utf-8')

        # 测试缩放效果
        # img = cv2.resize(img, (width, height))

        # # xmin, ymin, xmax, ymax分别为xml读取的坐标信息
        # left_top = (int(xmin_data * scale-int(left)), int(ymin_data * scale-int(right)))
        # right_down = (int(xmax_data * scale-int(top)), int(ymax_data * scale-int(bottom)))
        # cv2.rectangle(img, left_top, right_down, (255, 0, 0), 1)
        # cv2.imwrite(image_output_fullname, img)
