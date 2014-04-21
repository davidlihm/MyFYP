__author__ = 'User'
import os
import shutil
label_path = "D:\\Dropbox\\FYP\\project\\CSDMC2010_SPAM\\SPAMTrain.label"
Train_path = "D:\\Dropbox\\FYP\\project\\CSDMC2010_SPAM\\TRAINING"
s = "D:\\Dropbox\\FYP\\project\\CSDMC2010_SPAM\\s"
h = "D:\\Dropbox\\FYP\\project\\CSDMC2010_SPAM\\h"
file = open(label_path,'r')
L = []

for line in file:
    l = line.split(' ')
    l[1] = l[1][0:-1]
    L.append(l)

#dir = os.listdir(Train_path)
for i in range(1000):
    result = L[i][0]
    name = L[i][1]
    path = Train_path + "\\"+name
    if result == '0':
        shutil.copy(path,s)
    else:
        shutil.copy(path,h)
        
    
    
