import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET

path = r'E:\dataset\SSDD SAR dataset1\SSDD SAR dataset'  # 原文件夹路径
newpath = r'E:\dataset\SSDD SAR dataset1'  # 新文件夹路径
c_w, c_h = 544, 544  # 目标图片的尺寸

def edit_xml(xml_file, ratio, i):
    all_xml_file = os.path.join(path, xml_file)
    tree = ET.parse(all_xml_file)
    objs = tree.findall('object')


    for obj in objs:
        obj_bnd = obj.find('bndbox')
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

    newfile = os.path.join(newpath, '%06d' % (0 + i) + '.xml')
    tree.write(newfile, method='xml', encoding='utf-8')  # 更新xml文件


if __name__ == '__main__':
    files = os.listdir(path)  # 获取文件名列表
    i = 1
    for file in files:
        img_zeros = np.zeros((c_w, c_h, 3), np.uint8)  # 创建全黑的图像
        if file.endswith('.jpg'):
            imgName = os.path.join(path, file)  # 获取文件完整路径
            xml_file = file.replace('.jpg', '.xml')
            img = cv2.imread(imgName)  # 读图
            h, w, _ = img.shape  # 获取图像宽高
            # 缩放图像，宽高大于c_w的按长边等比例缩放，小于c_w的保持原图像大小：
            if max(w, h) < c_w:
                ratio1 = c_w / max(w, h)

                imgcrop = cv2.resize(img, (round(w * ratio1), round(h * ratio1)))
                # 将缩放后的图像复制进全黑图像里
                img_zeros[0:round(h * ratio1), 0:round(w * ratio1)] = imgcrop
                edit_xml(xml_file, ratio1, i)
            else:
                ratio2 = c_h / max(w, h)

                imgcrop = cv2.resize(img, (round(w * ratio2), round(h * ratio2)))
                # 将缩放后的图像复制进全黑图像里
                img_zeros[0:round(h * ratio2), 0:round(w * ratio2)] = imgcrop
                edit_xml(xml_file, ratio2, i)
            # else:
            #     img_zeros[0:h, 0:w] = img
            #     edit_xml(xml_file, 1, i)


            # 设置新的文件名：
            newName = os.path.join(newpath, '%06d' % (0 + i) + '.jpg')
            i += 1
            print(newName)
            cv2.imwrite(newName, img_zeros)  # 存储按新文件名命令的图片
