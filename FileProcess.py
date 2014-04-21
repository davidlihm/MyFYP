__author__ = 'User'
import os
import shutil
from_path = "C:\\Users\\User\\Desktop\\spam"
to_pth = "C:\\Users\\User\\Desktop\\spam2"
def moveAllFiles(from_path, to_path):
    #count = count
    L = os.listdir(from_path)
    for path in L:
        if os.path.isdir(from_path+"\\"+path):
            print("Folder: "+str(path))
            moveAllFiles(from_path+"\\"+path, to_path)
        else:
            #count = count+1
            print("File: "+from_path+"\\"+path)
            shutil.copyfile(from_path+"\\"+path, to_path)

moveAllFiles(from_path, to_pth)