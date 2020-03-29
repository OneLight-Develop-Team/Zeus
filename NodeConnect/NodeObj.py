from PySide2.QtWidgets import *
from PySide2.QtCore import *
import PySide2.QtUiTools as QLoader
from PySide2.QtGui import QPixmap
import os
from node import BaseNode

#获取主文件目录
path = os.path.dirname(os.path.abspath(__file__))

srcPath = path+ r"\src"
class NodeObj(BaseNode):
    """Obj节点"""

    

    def __init__(self,parent,posX,posY):

        super(NodeObj, self).__init__(parent,posX,posY,scaX = 100,scaY = 100)
        
        self.setParent(parent)

        self.isConnect = False
        self.nodeType = "ObjNode"
        
        self.label = self.ui.findChild(QLabel, "label")

        
        self.radioButton = self.ui.findChild(QRadioButton, "radioButton")



        self.radioButton.clicked.connect(self.on_radioButton_Click)


        # self.numOutputSignal.connect(lambda: self.parent().selectFirst(self))



    def setUI(self):
        self.uiPath = srcPath + r"\ObjNode.ui"
        self.loader = QLoader.QUiLoader()
        self.ui = self.loader.load(self.uiPath)
        self.ui.setParent(self)

    


    def setName(self,name):
        """设置节点名称"""
        self.label.setText(name)
    
    def setFilePath(self, path):
        self.obj_path = path

    # def setPic(self, path):
    #     """设置节点图片"""
    #     pixmap = QPixmap(path)
    #     self.label_pic.setPixmap(pixmap)
    #     self.label_pic.setScaledContents(True)

   
    # def getPath(self, path):
    #     """获取图片路径"""
    #     self.pic_path = path


    def on_radioButton_Click(self):
        """按钮按下,如果已经选择了一个输出端，则删除原来的输出端"""
        if self.isConnect == False:
            if (self.parent().pipe.getHasSelectFirst()):
            
                self.parent().pipe.delNodeFirstSelect()
            self.parent().pipe.setOutputNode(self)


        self.parent().updateRadio()
        self.parent().updateWindow()

            
    

    def setRadioCheckFalse(self):
        """设置按钮未点击"""
        self.radioButton.setChecked(False)



    def setRadioOutputCheck(self):
        self.radioButton.setChecked(True)

    def getOutputPos(self):
        
        return self.PosX + self.radioButton.geometry().x(), self.PosY + self.radioButton.geometry().y() + 40
        

      
    def getNodeType(self):
        return self.nodeType