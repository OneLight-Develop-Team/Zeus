# <-- coding utf-8 -->

from PySide2.QtWidgets import QDockWidget,QTreeView,QPushButton,QVBoxLayout,QWidget
from PySide2.QtCore import Signal

from Zeus.settings.Setting import Data
import layouitflow
from functools import partial

import os,json
reload(layouitflow)
#获取当前文件所在路径
current_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.dirname(current_path)

class FileTreeWindow(QDockWidget):
    """大纲视图"""

    # 发送大纲视图点击信号
    load_center_signal = Signal(str)

    def __init__(self):

        super(FileTreeWindow,self).__init__()

        self.setObjectName("TreeView")
        # self.getTags()
        self.setupUI()

        #双击treeView文件时，资源窗口会自动显示点击的文件内容
        # self.treeview.doubleClicked.connect(self.sendFile)
        
        
        

       
    # 设置UI界面
    def setupUI(self):
        # self.setStyleSheet("background-color:rgb(221,22,23)")
        self.setFloating(False)

  
        self.widget = QWidget()
        self.widget.setMinimumSize(Data.getWindowWidth()/6,Data.getWindowHeight()/2)

        self.setWidget(self.widget)
        
        self.setWindowTitle("大纲视图")

        self.setBtn()

    # # 获取标签
    # def getTags(self):
    #     self.tags = Data.getTag()

    # 从数据库加载标签，设置按钮
    def setBtn(self):
        self.widget.setLayout(layouitflow.FlowLayout())

        #加载标签数据到字典
        with open(file_path + r"\res\temp\setting.json") as js:
            setting_json = json.load(js)

        

        # 根据标签添加按钮
        for tag in setting_json["Tags"]:
            btn = QPushButton(tag)
            btn.clicked.connect(partial(self.sendLoadCenter,tag))
            self.widget.layout().addWidget(btn)

        # 添加分类按钮
        # self.widget.layout().setSpacing(1)
        # self.widget.layout().addStretch()

        self.setWidget(self.widget)
        


    # 添加新建标签
    def addBtn(self,tags):
        for tag in tags:
            btn = QPushButton(tag)
            btn.clicked.connect(partial(self.sendLoadCenter,tag))
            self.widget.layout().addWidget(btn)
  

        
    # 发送加载center信号到主窗体
    def sendLoadCenter(self, tag):
        
        self.load_center_signal.emit(tag)
      
