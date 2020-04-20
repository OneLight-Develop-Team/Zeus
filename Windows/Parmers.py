# using utf-8
from Qt.QtGui import QPixmap
from Qt.QtWidgets import QWidget, QDockWidget, QLabel, QPushButton, QLineEdit, QTableWidget, \
    QMessageBox,QTableWidgetItem,QHeaderView,QVBoxLayout,QFrame
from Qt.QtCore import Qt,Signal
from Qt.QtCore import QPropertyAnimation, QSize
from Qt.QtCompat import loadUi, setSectionResizeMode

import os, time
import pymongo
from CefWidget import CefBrowser




from settings.Setting import Data


from dayu_widgets import dayu_theme
from dayu_widgets.label import MLabel
from dayu_widgets.divider import MDivider
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.push_button import MPushButton
from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets.qt import QTimer
from dayu_widgets.tab_widget import MTabWidget
from dayu_widgets import MMessage
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



class ParmerPanel(QWidget):
    """参数面板类"""
    send_message_signal = Signal(str,str)
    def __init__(self, username):
        super(ParmerPanel, self).__init__()
        
        self.username = username
        self.id = None
   
        self.setObjectName("parmPanel")
        
        self.setupUI()
        
        dayu_theme.apply(self)

    
 
    # 设置UI界面
    def setupUI(self):
      
        self.setMaximumWidth(Data.getWindowWidth()/3)

       

        self.ui = loadUi(file_path + "\\res\\UI\\ParameterWindow.ui")

        self.ui.setParent(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.ui)
       
        self.widget_1 = self.ui.findChild(QWidget, "widget")
        self.widget_2 = self.ui.findChild(QWidget, "widget_2")
        self.widget_3 = self.ui.findChild(QWidget, "widget_3")
        self.widget_4 = self.ui.findChild(QWidget, "widget_4")
        self.widget_1.setLayout(QVBoxLayout())
        self.widget_2.setLayout(QVBoxLayout())
        self.widget_4.setLayout(QVBoxLayout())
        self.widget_2.layout().setSpacing(8)
        #设置布局


     
        tab_card = MTabWidget()
        self.label_filePic = MLabel("")
        self.widget_1.setMinimumSize(Data.getWindowHeight()/2.8,Data.getWindowHeight()/2.8)
        tab_card.addTab(self.label_filePic, u'预览图')

        # Todo 加载3d视口
        # self.model_widget = QWidget()
        self.model_widget = CefBrowser(self,url="editor")
        # self.model_widget.setLayout(QVBoxLayout())
        tab_card.addTab(self.model_widget, u'3D视口')
    
    
        self.widget_1.layout().addWidget(tab_card)
        self.widget_1.layout().setContentsMargins(0,0,0,0)

        self.widget_2.layout().addWidget(MDivider(u'操作面板'))

        self.let_filename  = MLineEdit(text='filename')
        tool_button = MLabel(text=u'文件名').mark().secondary()
        tool_button.setAlignment(Qt.AlignCenter)
        tool_button.setFixedWidth(80)
        self.let_filename .set_prefix_widget(tool_button)
        self.widget_2.layout().addWidget(self.let_filename)

        self.let_path  = MLineEdit(text='filepath')
        tool_button_2 = MLabel(text=u'文件地址').mark().secondary()
        tool_button_2.setAlignment(Qt.AlignCenter)
        tool_button_2.setFixedWidth(80)
        self.let_path .set_prefix_widget(tool_button_2)
        self.widget_2.layout().addWidget(self.let_path)
        self.widget_2.layout().addWidget(MLabel(u'标签'))

        self.let_tag = MLineEdit(text='tag')
        self.btn_reviseTag = MPushButton(text=u'修改').primary()
        self.btn_reviseTag.setFixedWidth(80)
        self.let_tag.set_suffix_widget(self.btn_reviseTag)
        self.widget_2.layout().addWidget(self.let_tag)
        self.btn_export = MPushButton(u'导出到houdini').primary()
        self.widget_2.layout().addWidget(self.btn_export)
        self.btn_exportToMaya = MPushButton(u'导出到Maya').primary()
        self.widget_2.layout().addWidget(self.btn_exportToMaya)
        
        
        self.timer = QTimer()
        self.timer.setInterval(0.1)
        self.timer.timeout.connect(self.slot_timeout)
        self.auto_color_progress = MProgressBar().auto_color()
    
       
        self.widget_2.layout().addWidget(self.auto_color_progress)

        self.widget_4.layout().addWidget(MDivider(u'操作记录'))
        self.setWindowTitle(u"参数面板")

        # #获取控件
        
      



        self.tableWidget_operationNote = self.ui.findChild(QTableWidget, "tableWidget_operationNote")

        self.tableWidget_operationNote.setStyleSheet(Data.getQSS())
        #设置默认值
        self.let_filename.setReadOnly(True)#只读
        self.let_path.setReadOnly(True)#只读
        self.let_tag.setReadOnly(True)#只读
        self.tableWidget_operationNote.setHorizontalHeaderLabels([u'用户', u'操作', u'时间'])

        # #连接信号与槽
        self.btn_export.clicked.connect(self.slot_run)
        self.btn_reviseTag.clicked.connect(lambda: self.reviseTag())
        # self.tableWidget_operationNote.setColumnCount(3)
        setSectionResizeMode(self.tableWidget_operationNote.horizontalHeader(),QHeaderView.Stretch) # 自适应
        

    def setParam(self, type, name, path):
        self.type = type
        self.filename = name
        self.filepath = path
       

       

       
        # 根据图片类型设置图片
        if (type == "jpg" or type == "jpeg" or type == "png"):
            self.setPic(path)
        elif (type == "obj" or type == "fbx"):
            self.setObjPic()

        filepath = os.path.dirname(path)
        filename = filepath.split("/")[-1]

        self.let_filename.setText(filename)
        self.let_path.setText(filepath)

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
                newItem1 = QTableWidgetItem(str1)
                self.tableWidget_operationNote.setItem(i, 0, newItem1)

            if "Time" in xdir:
                str3 = xdir["Time"]
                newItem3 = QTableWidgetItem(str3)
                self.tableWidget_operationNote.setItem(i, 2, newItem3)

            if "Operation" in xdir:
                str2 = xdir["Operation"]
                newItem2 = QTableWidgetItem(str2)
                self.tableWidget_operationNote.setItem(i, 1, newItem2)
                i += 1

       

        self.saveBrowseNode(self.username, name, type)  #保存浏览信息到库

        # 链接信号与槽函数
        self.btn_export.clicked.connect(lambda: self.exportModelToHoudini(name, type, path))
        self.btn_exportToMaya.clicked.connect(lambda: self.exportModelToMaya(name, type, path))
        # self.saveBrowseNode(self.username, name, type)

    # 进度条
    def slot_run(self):
        self.timer.start()
        self.auto_color_progress.setValue(0)

    def slot_timeout(self):
        if self.auto_color_progress.value() > 99:
            self.timer.stop()
        else:
            self.auto_color_progress.setValue(self.auto_color_progress.value() + 1)


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


    def exportModelToHoudini(self, filename, type, path):
        try:
       
			import hrpyc
			connection, hou = hrpyc.import_remote_module()
			name = filename.split(".")[0]
			if (type == "obj" or type == "fbx"):
				print("exportModelHoudiniOBJ")

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
				try:
					print("exportModelHoudiniJPG")
					# 路径不能有中文
					imgNode = hou.node('/img').createNode('img', "comp1")
					imgNode = hou.node('/img/comp1').createNode('file', name)
					# fileNode = imgNode.createNode('file', name)
					imgNode.parm('filename1').set(path)
				except:
					print("ExportPictureFail")

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
        except:
            self.slot_show_message(MMessage.info, (u'导出失败！请确认Houdini是否配置成功或启动。'))
            print (path)
            print (type)

    def exportModelToMaya(self, filename, type, path):

        if type == "obj" or type == "fbx":
            print("ExportModelToMaya")

            import socket

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', 7001))
                #s.send('print("HelloWord!!!!!!!!!!!!");')
                name = filename.split(".")[0]

                command0 = "import maya.cmds as mc;"
                command1 = "imported_objects = mc.file(r'" + path + "\', ns='ns', i=True, rnn=True);"
                command2 = "transforms = mc.ls(imported_objects, type='transform');"
                command = command0 + command1 + command2
                s.send(command)
            except:
                self.slot_show_message(MMessage.info, (u'导出失败！请确认Maya是否配置成功或启动。'))
                print (path)
                print (type)
        else:
            print ("This can't export to Maya")

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
                self.send_message_signal.emit("warnning",u"只有管理员才可以修改标签")
                return 0

            self.let_tag.setReadOnly(False)#可写入
            self.btn_reviseTag.setText(u"确认修改")

            
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
            if newTag == "":
                continue
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


        self.btn_reviseTag.setText(u"修改")
        self.send_message_signal.emit("info", u"已成功修改标签")
        
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

    # Todo: 传入预览图路径，加载3d视口资源到3d视口
    def setModelWidget(self, path):

        file = os.path.dirname(path)
        modelpath = ""  # 存储模型文件
        picpath = []  #存储贴图数据
        
        for name in os.listdir(file):
            if name.split(".")[-1] == "obj" or name.split(".")[-1] == "fbx" :
                modelpath = file + "/" + name
                break
                
            elif name.split(".")[-1] == "jpg" :
                picpath.append(file + "/" + name)

        # self.model_widget.layout().addWidget(MLabel(modelpath))
 
        self.model_widget.loadAsset(modelpath)

    # 弹出信息提示窗口
    def slot_show_message(self, func, config):
        func(config, parent=self.parent())