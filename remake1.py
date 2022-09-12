# *_* coding : UTF-8 *_*
# 开发人员   ：csu·pan-_-||
# 开发时间   ：2020/11/09 18:15
# 文件名称   ：renameFile.py
# 开发工具   ：PyCharm
# 功能描述   ：将文件夹下的图片全部缩放(同时保持原有宽高比例),裁切，并按新文件名存储
#             同时调整xml里的坐标信息

import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET

path = r'E:\dataset\SSDD SAR dataset1\SSDD SAR dataset'          # 原文件夹路径
newpath = r'E:\dataset\SSDD SAR dataset1'    # 新文件夹路径
c_w ,c_h = 544,544                   # 全黑画布的大小

def edit_xml(xml_file,ratio,i):
    """
    修改xml文件
    :param xml_file:xml文件的路径
    :return:
    """
    all_xml_file = os.path.join(path, xml_file)
    tree = ET.parse(all_xml_file)
    objs = tree.findall('object')
    for ix, obj in enumerate(objs):
        # type = obj.find('type').text
        # if type == 'bndbox':
            obj_bnd = obj.find('bndbox')
            obj_xmin = obj_bnd.find('xmin')
            obj_ymin = obj_bnd.find('ymin')
            obj_xmax = obj_bnd.find('xmax')
            obj_ymax = obj_bnd.find('ymax')
            xmin = float(obj_xmin.text)
            ymin = float(obj_ymin.text)
            xmax = float(obj_xmax.text)
            ymax = float(obj_ymax.text)
            obj_xmin.text = str(round(xmin * ratio))
            obj_ymin.text = str(round(ymin * ratio))
            obj_xmax.text = str(round(xmax * ratio))
            obj_ymax.text = str(round(ymax * ratio))

        # elif type == 'robndbox':
        #     obj_bnd = obj.find('robndbox')
        #     obj_cx = obj_bnd.find('cx')
        #     obj_cy = obj_bnd.find('cy')
        #     obj_w = obj_bnd.find('w')
        #     obj_h = obj_bnd.find('h')
        #     obj_angle = obj_bnd.find('angle')
        #     cx = float(obj_cx.text)
        #     cy = float(obj_cy.text)
        #     w = float(obj_w.text)
        #     h = float(obj_h.text)
        #     obj_cx.text = str(cx * ratio)
        #     obj_cy.text = str(cy * ratio)
        #     obj_w.text = str(w * ratio)
        #     obj_h.text = str(h * ratio)

    newfile = os.path.join(newpath, '%05d'%(0+i)+'.xml')
    tree.write(newfile, method='xml', encoding='utf-8')  # 更新xml文件

if __name__ == '__main__':
    files = os.listdir(path)              # 获取文件名列表
    for i, file in enumerate(files):
        img_zeros = np.zeros((c_w, c_h, 3), np.uint8)  # 创建全黑的图像
        if file.endswith('.jpg'):
            imgName = os.path.join(path, file)         # 获取文件完整路径
            xml_file = file.replace('.jpg','.xml')
            img = cv2.imread(imgName)                  # 读图
            h, w , _ = img.shape                       # 获取图像宽高
            # 缩放图像，宽高大于800的按长边等比例缩放，小于800的保持原图像大小：
            if max(w,h) > c_w:
                ratio = c_w / max(w,h)
                imgcrop = cv2.resize(img, (round(w * ratio) , round(h * ratio)))
                # 将裁切后的图像复制进全黑图像里
                img_zeros[0:round(h * ratio), 0:round(w * ratio)] = imgcrop
                edit_xml(xml_file, ratio, i)
            else:
                ratio = c_w / max(w, h)
                img_zeros[0:h, 0:w] = img
                edit_xml(xml_file, ratio, i)

            # 设置新的文件名：
            newName = os.path.join(newpath, '%05d'%(0+i)+'.jpg')
            print(newName)
            cv2.imwrite(newName,img_zeros)            # 存储按新文件名命令的图片


