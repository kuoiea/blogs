#!/usr/bin/env python
# -*-coding:UTF-8 -*-
import os
def file_name(file_dir):
    L = []
    print(file_dir)
    for root, dirs, files in os.walk(file_dir):
        # print(root,dirs,files)
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                L.append(os.path.join(root, file))
    return L
path = os.path.join(os.getcwd(),'static')

ret = file_name(path)
print(ret)


# def GetFileList(dir, fileList):
#     newDir = dir
#     if os.path.isfile(dir):
#         fileList.append(dir)
#     elif os.path.isdir(dir):
#         for s in os.listdir(dir):
#             #如果需要忽略某些文件夹，使用以下代码
#             #if s == "xxx":
#                 #continue
#             newDir=os.path.join(dir,s)
#             GetFileList(newDir, fileList)
#     return fileList




