# 原始图片宽为 w,高为h,bounding box(xmin,ymin,xmax,ymax)
# 归一化后的图片：宽为w1,高为h1,中心点坐标为（x,y)
# 由归一化到原始图片：xmin=w*(x-w1/2)  xmax=w*(x+w1/2)   ymin=h*(y-h1/2) ymax=h*(y+h1/2)

import os
import cv2

image_path = 'F:\\1-fromszn\\tank\\val\\images'  # 图片路径
txt_path = 'F:\\1-fromszn\\tank\\val\\labels-1'  # txt文档路径
image_out_path = r'F:\\1-fromszn\\tank\\val\\yolo-realbox'  # 绘制框之后的图片保存路径
if not os.path.exists(image_out_path):
    os.mkdir(image_out_path)

list = os.listdir(image_path)  # 返回指定路径下文件列表
list2 = os.listdir(txt_path)

# print(list)
for i in range(0, len(list)):
    out_image_name = os.path.splitext(list[i])[0]
    # 读出原始图片的高 宽
    pathimage = os.path.join(image_path, list[i])
    # print(list[i])
    image = cv2.imread(pathimage)
    imginfo = image.shape
    h = imginfo[0]
    w = imginfo[1]
    print(h, w)
    imageNamelist = '.jpg'
    # print(h)
    # txt文档操作
    pathtxt = os.path.join(txt_path, list2[i])
    # print(pathtxt)
    f = open(pathtxt, 'r')
    lines = f.readlines()  # 按行读取

    for i in lines:
        line_object = i.split(' ')  # 用空格分开
        x = float(line_object[1])
        y = float(line_object[2])
        w1 = float(line_object[3])
        h1 = float(line_object[4])

        print(x, y, w1, h1)

        # 坐标系的转换
        xmin = int(w * (x - (w1 / 2.0)))
        ymin = int(h * (y - (h1 / 2.0)))
        xmax = int(w * (x + (w1 / 2.0)))
        ymax = int(h * (y + (h1 / 2.0)))

        ptLeftTop = (xmin, ymin)
        ptRightBottom = (xmax, ymax)
        point_color = (0, 255, 0)
        thickness = 1
        lineType = 4
        # cv2.rectangle(image,ptLeftTop,ptRightBottom,point_color,thickness,lineType)
        # ptLeftTop =(xmin,ymin)左上角
        # ptRightBottom=(xmax,ymax)右下角
        # point_color=(0,255,0)绿色 (0,0,255)红色
        # thickness=1
        # lineType=4
        # if (float(line_object[0]) == 0):
        #     point_color = (0, 0, 255)  # 蓝色
        # elif (float(line_object[0]) == 1):
        #     point_color = (0, 255, 0)  # 绿色
        # elif (float(line_object[0]) == 2):
        #     point_color = (0, 255, 255)  # 青色
        # elif (float(line_object[0]) == 3):
        #     point_color = (0, 255, 0)  # 红色
        # else:
        #     point_color = (200, 10, 10)  # 白色

        cv2.rectangle(image, ptLeftTop, ptRightBottom, point_color, 2, 4)

        # cv2.imshow('AlanWang', image)
        # cv2.waitKey(1000)  # 显示 10000 ms 即 10s 后消失
        # cv2.destroyAllWindows()
    path_out = os.path.join(image_out_path, out_image_name + '.jpg')
    print(path_out)
    cv2.imwrite(path_out, image)
