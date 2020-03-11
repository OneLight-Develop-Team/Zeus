# <-- coding utf-8 -->

from PySide2.QtWidgets import QDockWidget,QTreeView,QPushButton,QVBoxLayout,QWidget
from PySide2.QtCore import Signal
from functools import partial
from settings.Setting import Data
import os,json

#获取当前文件所在路径
current_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.dirname(current_path)

class FileTreeWindow(QDockWidget):
    """大纲视图"""

    # 发送大纲视图点击信号
    # load_center_signal = Signal(str)

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
        self.widget.setMinimumSize(Data.getWindowWidth()/6,Data.getWindowHeight()/4)

        self.setWidget(self.widget)
        
        self.setWindowTitle("大纲视图")

        # self.setBtn()

    # # 获取标签
    # def getTags(self):
    #     self.tags = Data.getTag()

    # # 设置按钮
    # def setBtn(self):
    #     self.widget.setLayout(QVBoxLayout())

    #     # 根据标签添加按钮
    #     for tag in self.tags:
    #         btn = QPushButton(tag)
    #         btn.clicked.connect(partial(self.sendLoadCenter,tag))
    #         self.widget.layout().addWidget(btn)

    #     # 添加分类按钮
    #     btn_new = QPushButton("添加分类")
    #     self.widget.layout().addWidget(btn_new)
    #     self.widget.layout().addStretch()

    #     self.setWidget(self.widget)
        



    
  

        
    # 发送加载center信号到主窗体
    def sendLoadCenter(self, tag):

        self.load_center_signal.emit(tag)
      
