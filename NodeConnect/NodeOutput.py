from PySide2.QtWidgets import *
from PySide2.QtCore import *
import PySide2.QtUiTools as QLoader
from PySide2.QtGui import QPixmap,QDoubleValidator

import os
from node import BaseNode

try:
    import hou
except:
    pass

#获取主文件目录
path = os.path.dirname(os.path.abspath(__file__))

srcPath = path+ r"\src"
class NodeOutput(BaseNode):
    """输出节点"""

    new_obj_signal = Signal()
    
    def __init__(self,parent,posX,posY):

        super(NodeOutput, self).__init__(parent,posX,posY,scaX=120,scaY=120)
        
        self.setParent(parent)
        self.show()

        self.nodeType = "nodeOutput"

        self.isConnect = False

      
        self.radioButton = self.ui.findChild(QRadioButton,"radioButton")
        self.radioButton.clicked.connect(lambda: self.on_radioButton_click())

        self.lineEdit1 = self.ui.findChild(QLineEdit, "lineEdit_1")
        self.lineEdit2 = self.ui.findChild(QLineEdit, "lineEdit_2")
        self.lineEdit3 = self.ui.findChild(QLineEdit,"lineEdit_3")
        self.lineEdit4 = self.ui.findChild(QLineEdit,"lineEdit_4")
        self.lineEdit5 = self.ui.findChild(QLineEdit,"lineEdit_5")
        self.lineEdit6 = self.ui.findChild(QLineEdit,"lineEdit_6")
        self.lineEdit7 = self.ui.findChild(QLineEdit,"lineEdit_7")
        self.lineEdit8 = self.ui.findChild(QLineEdit,"lineEdit_8")
        self.lineEdit9 = self.ui.findChild(QLineEdit, "lineEdit_9")
        
        for lineEdit in self.ui.findChildren(QLineEdit):
            lineEdit.setValidator(QDoubleValidator())  #设置只能输入double类型的数据
            
        self.lineEdit1.setText("0")
        self.lineEdit2.setText("0")
        self.lineEdit3.setText("0")
        self.lineEdit4.setText("1")
        self.lineEdit5.setText("1")
        self.lineEdit6.setText("1")
        self.lineEdit7.setText("0")
        self.lineEdit8.setText("0")
        self.lineEdit9.setText("0")

        self.btn = self.ui.findChild(QPushButton,"pushButton")
        self.btn.clicked.connect(self.on_btn_click)

        self.new_obj_signal.connect(self.getObj)

    def setUI(self):
        self.uiPath = srcPath + r"\OutputNode.ui"
        self.loader = QLoader.QUiLoader()
        self.ui = self.loader.load(self.uiPath)
        self.ui.setParent(self)




    def on_radioButton_click(self):
        """点击按钮，如果之前已经选择好了输出按钮，则输入数据"""
        if self.isConnect == False:
            if (self.parent().pipe.getHasSelectFirst()):

                self.parent().pipe.setInputNode(self)
            

        self.parent().updateRadio()
        self.parent().updateWindow()




    def getInputPos(self):

        return self.PosX + self.radioButton.geometry().x(), self.PosY + self.radioButton.geometry().y() + 40
   


 

    def setRadioInputCheck(self):
        """设置输入端口选中状态"""
        
        self.radioButton.setChecked(True)



        
    def setRadioCheckFalse(self):
        """关闭所有radio"""
        self.radioButton.setChecked(False)
     

    
      
    def getNodeType(self):
        return self.nodeType


    def on_btn_click(self):

        if self.isConnect == True:
            dialog = QFileDialog() 
            
            
            # self.path = dialog.getOpenFileName(self,'选择文件','')
            self.path = dialog.getExistingDirectory(self,
                                        "选取文件夹",
                                        "C:/")                                 #起始路径
            self.new_obj_signal.emit()

    # 导出模型
    def getObj(self):

        try:
    
            node_num = 0
            for node in self.parent().pipe.Node2:
                
                
                if self == node:
                    break
                node_num += 1
            input = self.parent().pipe.Node1[node_num].obj_path

            name = (input.split("/"))[-1]
        
            name = (name.split("."))[0]

            output = self.path + "\\" + name + "_xform" + ".obj"

            obj = hou.node("obj")
            geo = obj.createNode("geo")
            fileImport = geo.createNode("file")
            fileImport.parm("file").set(input)

            transform = geo.createNode("xform")    
            transform.setFirstInput(fileImport)
            transform.parm("tx").set(float(self.lineEdit1.text()))
            transform.parm("ty").set(float(self.lineEdit2.text()))
            transform.parm("tz").set(float(self.lineEdit3.text()))
            transform.parm("rx").set(float(self.lineEdit4.text()))
            transform.parm("ry").set(float(self.lineEdit5.text()))
            transform.parm("rz").set(float(self.lineEdit6.text()))
            transform.parm("sx").set(float(self.lineEdit7.text()))
            transform.parm("sy").set(float(self.lineEdit8.text()))
            transform.parm("sz").set(float(self.lineEdit9.text()))

            fileExport = geo.createNode("file")
            fileExport.setFirstInput(transform)
            fileExport.parm("filemode").set(2)
            fileExport.parm("file").set(output)
            fileExport.setDisplayFlag(1)
            fileExport.parm("reload").pressButton()

        except:
            pass