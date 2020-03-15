# using utf-8

from PySide2.QtWidgets import QWidget, QDockWidget,QVBoxLayout,QPushButton,QLabel,QHBoxLayout
from PySide2.QtCore import Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap

# import houdiniPlay.Command as hc
from Zeus.settings.Setting import Data


import os
# #获取当前文件所在路径
# current_path = os.path.dirname(os.path.abspath(__file__))

# file_path = os.path.dirname(current_path)


class ViewPanel(QDockWidget):
    """视口界面"""
    def __init__(self):
        super(ViewPanel, self).__init__()

        self.setObjectName("ViewPanel")
        
        self.setupUI()

        # self.label = self.ui.findChild(QLabel, "label")
        # self.btnContain = self.ui.findChild(QWidget,"widget")
        
        # self.btnContain.setLayout(QHBoxLayout())
        # # self.label.set

       

    # 设置UI界面
    def setupUI(self):
     
        self.setFloating(False)

        self.widget = QWidget()
        self.widget.setMinimumSize(Data.getWindowWidth()/4,Data.getWindowHeight()/4)
        self.widget.setLayout(QVBoxLayout())
        self.setWidget(self.widget)

        # #加载ui,并设置ui界面
        # loader = QUiLoader()
        # self.ui = loader.load(file_path + "\\res\\UI\\UserLogin.ui")
        # self.ui.setParent(self.widget)
        # #设置布局
        # self.widget.layout().addWidget(self.ui)
        # self.widget.layout().setContentsMargins(0,0,0,0)

        self.setWindowTitle("视口")

    
        


    # 设置视口
    def setView(self, type, name, path):

        print (type)
        print (name)
        print (path)
    #     #清除原有组件
    #     for i in range(self.btnContain.layout().count()): 
    #         self.btnContain.layout().itemAt(i).widget().deleteLater()

    #     if type == "jpg" or type == "jpeg" or type == "png":
    #         # self.label.setScaledContents(True)
    #         #加载图片,图片保持比例
    #         pixmap = QPixmap()
    #         pixmap.load(path)
    #         self.label.setPixmap(pixmap)
            
    #         #设置图片自适应背景
    #         self.label.setScaledContents(True)
    #         # self.label.setMaximumSize(600, 600)
    #         btn = QPushButton("show in mview")
    #         btn.clicked.connect(hc.showImage(path))
    #         self.btnContain.layout().addWidget(btn)

    #     elif type == "obj":
            
    #         pixmap = QPixmap()
    #         pixmap.load(file_path+"\\res\\image\\not_screenshot.jpg")
    #         self.label.setPixmap(pixmap)

           
    #         btn_prep = QPushButton("透视图")
    #         btn_left = QPushButton("左视图")
    #         btn_before = QPushButton("主视图")
    #         btn_top = QPushButton("顶视图")


    #         btn_gplay = QPushButton("gplay")
    #         btn_gplay.clicked.connect(lambda: hc.showModel(path))

            

    #         self.btnContain.layout().addWidget(btn_prep)
    #         self.btnContain.layout().addWidget(btn_before)
    #         self.btnContain.layout().addWidget(btn_left)
    #         self.btnContain.layout().addWidget(btn_top)

            
    #         self.btnContain.layout().addWidget(btn_gplay)

            




            

            
            
            