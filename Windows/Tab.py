﻿

from PySide2.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout,QLineEdit
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt

from Zeus.Windows.layouitflow import FlowLayout
import os,json


#获取当前文件所在路径
current_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.dirname(current_path)



class TabWidget(QWidget):
    """
        标签选择窗口类
    参数：
        文件路径
    """
    def __init__(self,paths):
        super(TabWidget, self).__init__()

        self.paths = paths  #文件路径列表

        self.setupUI()
        self.widget = self.ui.findChild(QWidget,"widget")
        self.btn_ok = self.ui.findChild(QPushButton, "btn_ok")
        self.btn_cancel = self.ui.findChild(QPushButton,"btn_cancel")
        self.lineEdit = self.ui.findChild(QLineEdit, "lineEdit")
        
        self.setTags()


        self.btn_ok.clicked.connect(self.on_btnOK_clicked)
        self.btn_cancel.clicked.connect(self.on_btnCancel_clicked)




    def setupUI(self):

        # 设置为模态对话框        
        self.setWindowModality(Qt.ApplicationModal)


        #加载ui,并设置ui界面
        loader = QUiLoader()
        self.ui = loader.load(file_path + "\\res\\UI\\TabWidegt.ui")
        self.ui.setParent(self)
        
        #设置布局
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setContentsMargins(0,0,0,0)

    # Todo: 将读取标签数据，改到从数据库读取
    # 从json文件里的Tags键读取已经有的标签,设置窗口的标签
    def setTags(self):
        self.widget.setLayout(FlowLayout())
        
        #加载标签数据到字典
        with open(file_path + r"\res\temp\setting.json") as js:
            setting_json = json.load(js)

        if "Tags" not in setting_json.keys():
            setting_json["Tags"] = []
        
        # 根据标签数据添加标签按钮
        for tag in setting_json["Tags"]:
            self.widget.layout().addWidget(TabBtn(tag))


        
    # 确定按钮按下，保存标签数据，并保存文件数据
    def on_btnOK_clicked(self):
        self.saveTags()
        self.saveFile()
        self.close()
    
    # 取消按钮按下，关闭窗口
    def on_btnCancel_clicked(self):
        self.close()

    # Todo: 将保存的标签数据改到数据库
    # 保存新添加的标签数据
    def saveTags(self):
        tags_add = self.lineEdit.text().split(",")

        #加载标签数据到字典
        with open(file_path + r"\res\temp\setting.json") as js:
            setting_json = json.load(js)

        if "Tags" not in setting_json.keys():
            setting_json["Tags"] = []
        
        # 保存新添加的标签
        for tag in tags_add:
            if tag not in setting_json["Tags"] and tag != "": #如果新添加的标签已经存在或者空标签，则不添加到标签列表
                setting_json["Tags"].append(tag)

        #写入标签数据到json文件中
        with open(file_path + r"\res\temp\setting.json", 'w') as json_file:
            json.dump(setting_json, json_file, indent=4)


    # Todo: 把保存的数据从json文件转换到数据库
    # 保存图片数据
    def saveFile(self):
        
        tags = self.getTags()  #获取标签
    

        #加载资产数据到字典
        with open(file_path + r"\res\temp\asset.json") as js:
            asset_json = json.load(js)

        #遍历打开的文件路径，加载到json中
        for path in self.paths:
            asset_json[path] = {}  # 设置单个资产为一个字典
            asset_json[path]["path"] = path  #保存地址
            asset_json[path]["name"] = (path.split("/"))[-1]   #保存文件名
            asset_json[path]["type"] = os.path.splitext(path)[-1]  #保存文件类型，后缀名
            asset_json[path]["tags"] = tags #保存文件标签

        #写入标签数据到json文件中
        with open(file_path + r"\res\temp\asset.json", 'w') as json_file:
            json.dump(asset_json, json_file, indent=4)

        
            
            
    
    # 获取选择的标签数据，和新添加的标签
    def getTags(self):
        tags = []  #标签列表
        self.btn_tags = self.widget.findChildren(QPushButton)
        
        # 获取选中的标签
        for  btn in self.btn_tags:
            if btn.isSelected:
                tags.append(btn.tagName)
               

        # 获取新添加的标签
        tags_add = self.lineEdit.text().split(",")
        for tag in tags_add:
            if tag not in tags and tag != "": #如果新添加的标签已经选中或者空标签，则不添加到标签列表
                tags.append(tag)

        return tags

class TabBtn(QPushButton):
    """标签按钮类"""
    def __init__(self,text):
        super(TabBtn, self).__init__()
        
        self.setText(text)  
        self.tagName = text #标签名字
        self.isSelected = False  # 默认为不选择
        self.clicked.connect(self.changeColor)
        self.setMinimumSize(100,50)
    
    #改变颜色
    def changeColor(self):
        if self.isSelected:
            self.setStyleSheet("border:2px soild rgb(25,25,25)")
            self.isSelected = False

        else:
            self.setStyleSheet("border:2px solid red")
            
            self.isSelected = True


