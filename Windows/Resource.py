# coding:utf-8

import pymongo
import os
import time

#链接数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")


alldocdb = client["alldocdb"]  #文件类型总库
alldoccol = alldocdb["alldoccol"]  #文件类型集合

def uploadSaveBaseData(docPath,userName,tags):
    """
    上传文件时保存文件基本信息：文件名、文件类型、上传用户名、标签
    参数：文件路径、用户名、标签
    """
    docType = os.path.splitext(docPath)[-1]  # 文件类型，后缀名
    docType = docType.split(".")[-1]
    docName = (docPath.split("/"))[-1]  # 文件名
    RTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))#当前时间

    #创建对应数据库和集合
    assetdb = client[docType]  #资产数据库
    assetcol = assetdb[docName]  #资产数据库集合

    dirName = {"_id": "FileName", "FileName": docName}  # 资产名字典
    dirFileType = {"_id": "FileType", "FileType": docType}  # 文件类型名字典
    dirPath = {"_id":"Path", "Path":docPath}    #资产路径字典
    dirUploadUserName = {"_id":"UploadUserName", "UserName": userName, "Time":RTime}  #上传文件用户名、时间字典

    allDir = [dirName,dirFileType,dirPath,dirUploadUserName]
    assetcol.insert_many(allDir)

    #把tags标签元组里面的标签一个个拿出来放进数据库
    for tag in tags:
        dirTag = {"Tag": tag}  # 标签字典
        assetcol.insert_one(dirTag)

    #把导入的文件类型，判断之前是否导入过，如果没有，则文件类型存入alldocdb库的alldoccol集合里面
    wh = True
    for x in alldoccol.find({},{"Type":1}):
        hadType = x["Type"]
        if docType == hadType:
            wh = False
            break
    if wh:
        dir = {"Type":docType}
        alldoccol.insert_one(dir)




