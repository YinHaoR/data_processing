import os
import random


trainval_percent = 0.8
train_percent = 0.6
xmlfilepath = 'E:\\dataset\\NWPU-VHR-10-dataset\\xml'
txtsavepath = 'E:\\dataset\\NWPU-VHR-10-dataset'
total_xml = os.listdir(xmlfilepath)

num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)

ftrainval = open('E:\\dataset\\NWPU-VHR-10-dataset/trainval.txt', 'w')
ftest = open('E:\\dataset\\NWPU-VHR-10-dataset/test.txt', 'w')
ftrain = open('E:\\dataset\\NWPU-VHR-10-dataset/train.txt', 'w')
fval = open('E:\\dataset\\NWPU-VHR-10-dataset/val.txt', 'w')

for i in list:
    name = total_xml[i][:-4] + '\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()
