# coding:utf-8


import pymongo
import os
import time



#链接数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")


alldocdb = client["alldocdb"]  #文件类型总库
alldoccol = alldocdb["alldoccol"]  #文件类型集合
tagfiledb = client["tagFiledb"]  #标签文件数据库

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
    
    collist = assetdb.list_collection_names()
    if not (docName in collist):        #如果该文件没有导入过
        assetcol = assetdb[docName]  #资产数据库集合

        dirName = {"_id": "FileName", "FileName": docName}  # 资产名字典
        dirFileType = {"_id": "FileType", "FileType": docType}  # 文件类型名字典
        dirPath = {"_id":"Path", "Path":docPath}    #资产路径字典
        dirUploadUserName = {"_id":"UploadUserName", "UserName": userName, "Time":RTime}  #上传文件用户名、时间字典
        allDir = [dirName, dirFileType, dirPath, dirUploadUserName]

        assetcol.insert_many(allDir)    #储存信息数据到资产数据库*****

        #把tags标签元组里面的标签一个个拿出来放进数据库
        for tag in tags:
            dirTag = {"Tag": tag}  # 标签字典
            assetcol.insert_one(dirTag)     #保存标签到资产库*******

            col = tagfiledb[tag]  # 以标签名为集合名,标签文件库
            dict = {"FileName": docName}
            col.insert_one(dict)    #保存文件名到标签文件库******

        #把导入的文件类型，判断之前是否导入过，如果没有，则文件类型存入alldocdb库的alldoccol集合里面
        wh = True
        for x in alldoccol.find({},{"Type":1}):
            hadType = x["Type"]
            if docType == hadType:
                wh = False
                break
        if wh:
            dir = {"Type":docType}
            alldoccol.insert_one(dir)  #保存文件类型到文件类型库

    else:       #如果该文件导入过
        assetcol = assetdb[docName]  # 资产数据库集合
        assertaglist = assetcol.find({}, {"Tag": 1})
        oldtaglist = []
        for tagdic in assertaglist:
            if "Tag" in tagdic:
                oldtaglist.append(tagdic["Tag"])

        for newtag in tags:
            wn = True
            for oldtag in oldtaglist:
                if oldtag == newtag:
                    wn = False
            if wn:      #新的标签
                col = tagfiledb[newtag]  # 以标签名为集合名,标签文件库
                dict = {"FileName": docName}
                col.insert_one(dict)  # 保存文件名到标签文件库

                dirTag = {"Tag": newtag}  # 标签字典
                assetcol.insert_one(dirTag)  # 保存新标签到资产库