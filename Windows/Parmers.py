# using utf-8
from Qt.QtGui import QPixmap
from Qt.QtWidgets import QWidget, QDockWidget, QLabel, QPushButton, QLineEdit, QTableWidget, QMessageBox
#from Qt.QtCompat import loadUi
from Qt.QtCore import Qt
import os, time
import pymongo
import hou

from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets

import MainWindow
reload(MainWindow)

#获取当前文件所在路径
current_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.dirname(current_path)

#链接标签数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")
tagdb = client["tagdb"]  #标签数据库
tagcol = tagdb["tagcol"]  #标签集合

#链接用户数据库
userdb = client["userdb"]

#链接标签文件数据库
tagfiledb = client["tagFiledb"]  #标签文件数据库


try:
    from Zeus.settings.Setting import Data
except:
    from settings.Setting import Data
class ParmerPanel(QDockWidget):
    """参数面板类"""
    def __init__(self, username):
        super(ParmerPanel, self).__init__()

        self.username = username
        self.id = None

        self.setObjectName("parmPanel")
        # self.setFeatures(Qt.DockWidgetVerticalTitleBar)
        self.setupUI()
        # self.show()

    # 设置UI界面
    def setupUI(self):
        # self.setStyleSheet("background-color:rgb(205,2,255)")
        self.setFloating(False)

        self.widget = QWidget()
        self.widget.setMinimumSize(Data.getWindowWidth()/4,Data.getWindowHeight()/4)
        self.setWidget(self.widget)

        #加载ui,并设置ui界面
        #self.ui = loadUi(file_path + "\\res\\UI\\ParameterWindow.ui")

        loader = QUiLoader()
        self.ui = loader.load(file_path + "\\res\\UI\\ParameterWindow.ui")

        self.ui.setParent(self.widget)
        #设置布局
        #self.widget.layout().addWidget(self.ui)
        #self.widget.layout().setContentsMargins(0,0,0,0)

        self.setWindowTitle(u"参数面板")

        #获取控件
        self.label_filePic = self.ui.findChild(QLabel, "label_filePic")
        self.let_path = self.ui.findChild(QLineEdit, "let_path")
        self.let_tag = self.ui.findChild(QLineEdit, "let_tag")
        self.let_filename = self.ui.findChild(QLineEdit, "let_filename")
        self.btn_reviseTag = self.ui.findChild(QPushButton, "btn_reviseTag")
        #self.btn_reviseFileName = self.ui.findChild(QPushButton, "btn_reviseFileName")
        self.btn_export = self.ui.findChild(QPushButton, "btn_export")

        self.tableWidget_operationNote = self.ui.findChild(QTableWidget, "tableWidget_operationNote")


        #设置默认值
        self.let_filename.setReadOnly(True)#只读
        self.let_path.setReadOnly(True)#只读
        self.let_tag.setReadOnly(True)#只读
        self.tableWidget_operationNote.setHorizontalHeaderLabels(['用户', '操作', '时间'])

        #连接信号与槽
        self.btn_reviseTag.clicked.connect(lambda: self.reviseTag())

    def setParam(self, type, name, path):
        self.type = type
        self.filename = name
        self.filepath = path

        # if self.username != None:
        #     print(self.username + "***username")
        #
        # if self.username == None:   #username为空
        #     print("****username is none")
        #     msgBox = QMessageBox()
        #     msgBox.setText(u'请先登陆！')
        #     msgBox.exec_()
        #     return 0

        # print(type)
        # print(name)
        # print(path)

        self.username = MainWindow.MainController.userNameMT
        if self.username == None:   #username为空
            msgBox = QMessageBox()
            msgBox.setText(u'请先登陆！')
            msgBox.exec_()
            return 0


        # Todo：读取数据库
        # 根据图片类型设置图片
        if (type == "jpg" or type == "jpeg" or type == "png"):
            self.setPic(path)
        elif (type == "obj"):
            self.setObjPic()

        self.let_filename.setText(name)
        self.let_path.setText(path)

        tags = ""
        assetdb = client[type]
        assetcol = assetdb[name]
        for tagdic in assetcol.find({},{"Tag":1}):
            if "Tag" in tagdic:
                tag = tagdic["Tag"]
                tags += tag + ","
        self.let_tag.setText(tags)


        #设置资产操作记录表：
        assetdb = client[type]
        assetcol = assetdb[name]
        assetlist = assetcol.find({}, {"UserName": 1, "Operation": 1, "Time": 1})
        #rowcount = len(assetlist)      #assetlist并不是列表类型
        i = 0
        # for x in assetlist:
        #     i += 1  #求得行数减一

        for xdir in assetlist:

            if "UserName" in xdir:
                str1 = xdir["UserName"]
                newItem1 = QtWidgets.QTableWidgetItem(str1)
                self.tableWidget_operationNote.setItem(i, 0, newItem1)

            if "Time" in xdir:
                str3 = xdir["Time"]
                newItem3 = QtWidgets.QTableWidgetItem(str3)
                self.tableWidget_operationNote.setItem(i, 2, newItem3)

            if "Operation" in xdir:
                str2 = xdir["Operation"]
                newItem2 = QtWidgets.QTableWidgetItem(str2)
                self.tableWidget_operationNote.setItem(i, 1, newItem2)
                i += 1



        self.saveBrowseNode("lin", name, type)  #保存浏览信息到库

        # 链接信号与槽函数
        self.btn_export.clicked.connect(lambda: self.exportModel(name, type, path))

        #self.saveBrowseNode(self.username, name, type)


    def setPic(self, path):
        pixmap = QPixmap(path)
        self.label_filePic.setPixmap(pixmap)
        self.label_filePic.setScaledContents(True)

    def setObjPic(self):
        """加载的是obj模型，设置obj的图片"""
        pixmap = QPixmap(file_path + r"\res\image\objimg.jpg")
        self.label_filePic.setPixmap(pixmap)
        self.label_filePic.setScaledContents(True)

    def saveBrowseNode(self, username, filename, type):

        RTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        #将浏览信息存入用户数据库
        col = userdb[username]
        dict = {"Operation": "Browse", "Time": RTime, "FileName":filename}
        col.insert_one(dict)

        #将浏览信息存入资产数据库
        assetdb = client[type]
        assetcol = assetdb[filename]
        adict = {"UserName": username, "Time": RTime, "Operation": "Browse"}
        assetcol.insert_one(adict)


    def exportModel(self, filename, type, path):

        #self.saveExportModelNode(self.username, filename, type)

        #hou.createNode('geometry', filename)
        #node = hou.pwd()
        #geo0 = node.createNode('Geometry', filename)

        # objNode = hou.node('/obj')
        # geo0 = objNode.createNode('geometry')

        # geo = hou.node('/obj').createNode('geo', "box")
        # fileNode = geo.createNode('file', "box")
        # materialNode = geo.createNode('material', "box_material")
        # materialNode.setInput(0, fileNode)
        # materialNode.moveToGoodPosition()
        # materialNode.setDisplayFlag(1)

        name = filename.split(".")[0]
        if (type == "obj" or type == "fbx"):

            geo = hou.node('/obj').createNode('geo', name)
            fileNode = geo.createNode('file', name)
            fileNode.parm('file').set(path)

            prinShaderNode = hou.node('/mat').createNode('principledshader', name)
            prinShaderNode.parm('basecolor_useTexture').set(1)

            materialNode = geo.createNode('material', name + "_material")
            materialNode.parm('shop_materialpath1').set("/mat/" + name)
            materialNode.setInput(0, fileNode)
            materialNode.moveToGoodPosition()
            materialNode.setDisplayFlag(1)



        if (type == "jpg" or type == "jpeg"):
            #路径不能有中文
            imgNode = hou.node('/img/comp1').createNode('file', name)
            #fileNode = imgNode.createNode('file', name)
            imgNode.parm('filename1').set(path)

        #保存导出记录到资产数据库
        RTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        assetdb = client[type]
        assetcol = assetdb[filename]
        adict = {"UserName": self.username, "Time": RTime, "Operation": "Export"}
        assetcol.insert_one(adict)
        # 保存导出记录到用户数据库
        usercol = userdb[self.username]
        adict = {"FileName": filename, "Time": RTime, "Operation": "Export"}
        usercol.insert_one(adict)

    def saveExportModelNode(self, username, filename, type):
        RTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # 将浏览信息存入用户数据库
        col = userdb[username]
        dict = {"Operation": "Export", "Time": RTime, "FileName": filename}
        col.insert_one(dict)

        # 将浏览信息存入资产数据库
        assetdb = client[type]
        assetcol = assetdb[filename]
        adict = {"UserName": username, "Time": RTime, "Operation": "Export"}
        assetcol.insert_one(adict)

    def reviseTag(self):

        if self.username != None:
            usercol = userdb[self.username]
            idlist = usercol.find({"_id": "UserID"}, {"UserID": 1})
            for iddir in idlist:
                self.id = iddir["UserID"]

            if self.id != "管理员":
                msgBox = QMessageBox()
                msgBox.setText(u'管理员才有权限修改！')
                msgBox.exec_()
                return 0

        self.let_tag.setReadOnly(False)#可写入
        self.btn_reviseTag.setText("确认修改")


        self.btn_reviseTag.clicked.disconnect()
        self.btn_reviseTag.clicked.connect(lambda: self.confirmReviseTag())

    def confirmReviseTag(self):
        self.let_tag.setReadOnly(True)  # 只读

        #连接数据库
        assetdb = client[self.type]
        assetcol = assetdb[self.filename]
        assetdb = client[self.type]
        assetcol = assetdb[self.filename]

        newTags = self.let_tag.text().split(",")
        self.oldTags = []
        taglist = assetcol.find({},{"Tag":1})
        for tag in taglist:
            if "Tag" in tag:
                self.oldTags.append(tag["Tag"])

        #是否有删除标签
        for oldTag in self.oldTags:
            delTag = True
            for newTag in newTags:
                if newTag == oldTag:
                    delTag = False
            if delTag:  #存在
                # 删除资产库里的标签
                deldir = {"Tag": oldTag}
                assetcol.delete_one(deldir)
                #删除标签文件库里对应的文件
                tagfilecol = tagfiledb[oldTag]
                deldir = {"FileName": self.filename}
                tagfilecol.delete_one(deldir)

        #是否有新标签
        for newTag in newTags:

            # 是否为从未有过的标签
            new = True
            for x in tagcol.find({}, {"Tag": 1}):  # 把数据库里的标签取出
                if newTag == x["Tag"]:
                    new = False
            if new:
                newTagdir = {"Tag": newTag}
                tagcol.insert_one(newTagdir)  # 添加到标签数据库

            addTag = True
            for oldTag in self.oldTags:
                if newTag == oldTag:
                    addTag = False
            if addTag:
                #资产库里添加新标签
                adict = {"Tag": newTag}
                assetcol.insert_one(adict)
                # 标签文件库里添加对应的文件
                tagfilecol = tagfiledb[newTag]
                deldir = {"FileName": self.filename}
                tagfilecol.insert_one(deldir)


        self.btn_reviseTag.setText("修改")

        #保存操作记录到用户数据库
        RTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        usercol = userdb[self.username]
        adict = {"FileName": self.filename, "Time": RTime, "Operation": "EditTag"}
        usercol.insert_one(adict)
        #保存操作记录到资产数据库
        RTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        adict = {"UserName": self.username, "Time": RTime, "Operation": "EditTag"}
        assetcol.insert_one(adict)

        self.btn_reviseTag.clicked.disconnect()
        self.btn_reviseTag.clicked.connect(lambda: self.reviseTag())