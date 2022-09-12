import cv2 as cv
import os
import numpy as np

img_path = 'F:\\test\\ground-truth\\'  # 图像路径
re_path = 'F:\\NWPU-test\\test\\'  # 图像路径

img_num = len(os.listdir(img_path))  # 计算目录下有多少图像

# 注：如果文件名不是顺序排列（1,2,3,4....n），可以用以下方式取文件
img_list=os.listdir(img_path)
re_list=os.listdir(re_path)

for i in range(0, img_num):  #
    # img_name = img_path + str(i) + '.jpg'  # 图像格式为“.png”
    # re_name = re_path + str(i) + '.jpg'

    # 当文件名不是顺序排列时
    img_name=img_path+img_list[i]
    re_name=re_path+re_list[i]
    result = img_list[i]
    img = cv.imread(img_name)
    re = cv.imread(re_name)

    # img = cv.resize(img, (800, 800))
    # re = cv.resize(re, (800, 800))

    cv.namedWindow('result', cv.WINDOW_AUTOSIZE)

    h_all = np.hstack((img, re))  # 参数（img,re）取决于你要横向排列的图像个数
    # v_all=np.vstack((img,re)) #纵向排列

    cv.imshow('result', h_all)

    # for filename in os.listdir(img_path):
    cv.imwrite("F:/NWPU-vhr/result"+'_' + img_list[i], h_all)
    cv.waitKey(10)  # 0.1s后进行下轮循环

cv.destroyAllWindows()
