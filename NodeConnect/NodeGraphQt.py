from PySide2 import QtWidgets, QtCore
from Zeus.NodeConnect import NodeDialog

from PySide2 import QtGui

import json, os
reload(NodeDialog)


#获取当前文件所在文件目录
path = os.path.dirname(os.path.abspath(__file__))

srcPath = path + r"\src"

class BackWidget(QtWidgets.QWidget):
    """背景窗口"""
    def __init__(self):
        super(BackWidget, self).__init__()
        self.resize(800,600)
        
       
        self.setStyleSheet("color:white")


        # 用于保存节点连接数据
        self.pipe = Pipe()
     
       
        self.nodeData = None
       
        
    #按下右键，打开节点选择器
    def mousePressEvent(self,event):
    
        self.setFocus()

       
        if event.buttons() == QtCore.Qt.RightButton:
            
            dialogs = self.findChildren(QtWidgets.QDialog, "节点选择器")
            for dialog in dialogs:
                dialog.close()

            self.loadNodeList()

            nodeDialog = NodeDialog.NodeDialog(event.x(), event.y())

            nodeDialog.setParent(self)
            nodeDialog.move(event.x(),event.y())
            
            #为nodeDialog设置按钮数据
            nodeDialog.getNodeList(self._node_path, self._node_name, self._node_type)

            
            nodeDialog.show()

    def loadNodeList(self):
        """加载资源视图资源到节点列表"""

        #第一步先清空
        self._node_path = []
        self._node_name = []
        self._node_type = []

        self.list = self.parent().getCenterSource()
    
        for path in self.list:

            name = (path.split("/"))[-1]
            type = os.path.splitext(path)[-1]
            if type == ".obj":
                self._node_type.append(type)
                self._node_name.append(name)
                self._node_path.append(path)
                
    def updateRadio(self):
        """"更新radio按钮"""
        
        #查找所有子节点
        node_list = self.findChildren(QtWidgets.QFrame)
        for node in node_list:
            #先关闭所有按钮，再打开有记录的按钮
            try:
                node.setRadioCheckFalse()
            except:
                pass

        for node_out in self.pipe.Node1:

            node_out.setRadioOutputCheck()
            
        for node_in in self.pipe.Node2:
            
            node_in.setRadioInputCheck()
            

     


    def paintEvent(self, event):

        """绘制界面"""

        nodeNum = 0
        ## 遍历每一对连接的节点
        for node in self.pipe.Node2:
            
            #获取要画线的四个顶点
            self.nodeData = Pipe.connectNode(self.pipe.Node1[nodeNum], self.pipe.Node2[nodeNum])

            painter = QtGui.QPainter()
            pen = QtGui.QPen(QtCore.Qt.white,10,QtCore.Qt.SolidLine)

            painter.setPen(pen)
            painter.begin(self)
            # self.painter.drawLine(self.nodeData[0], self.nodeData[1],self.nodeData[2],self.nodeData[3])

            path = QtGui.QPainterPath()

            path.moveTo(self.nodeData[0], self.nodeData[1])

            #绘制控制连接线的曲率点
            x_1 = (self.nodeData[0] + self.nodeData[2]) * 149 / 300
            
            y_1 = (self.nodeData[1] + self.nodeData[3]) * 1 / 4 
            
            x_2 = (self.nodeData[0] + self.nodeData[2]) * 151 / 300
            
            y_2 = (self.nodeData[1] + self.nodeData[3]) * 3 / 4
            
            path.cubicTo(x_1, y_1, x_2, y_2, self.nodeData[2], self.nodeData[3])

            
            painter.drawPath(path)

      
            brush = QtGui.QBrush(QtCore.Qt.white)
            painter.setBrush(brush)
            point = QtCore.QPoint((self.nodeData[0] + self.nodeData[2]) / 2, (self.nodeData[1] + self.nodeData[3]) / 2)
            painter.drawEllipse(point, 3, 3)



            painter.end()
            
            nodeNum += 1


        # self.pipe.printData()







    def updateWindow(self):
        """更新窗口"""
        
        
        QtWidgets.QWidget.update(self)





 







class Pipe():
    """用于储存节点连接数据"""
    def __init__(self):
        
        # 储存节点连接的数据
        self.Node1 = [] #输出节点 
    
        self.Node2 = []     #输入节点
     
        self.hasSelectFirst = False  #是否已经选择了第一个连接节点


    def setOutputNode(self, node):
        """设置输出节点数据"""
        for node_out in self.Node1: #防止一个端口多个输出
            if (node == node_out):
                return
           
        self.Node1.append(node)
        self.setHasSelectFirst(True)

    def setInputNode(self, node):
        """设置输入节点数据"""
     
        for node_in in self.Node2: #防止一个端口多个输入
            if (node == node_in):
                return
        node.isConnect = True
        self.Node1[-1].isConnect = True
        self.Node2.append(node)
        
        self.setHasSelectFirst(False)
        

    def setHasSelectFirst(self,charge):
        """设置选择节点"""
        self.hasSelectFirst = charge

    def getHasSelectFirst(self):
        """获取是否已经选择了第一个节点"""
        return self.hasSelectFirst

    def delNodeFirstSelect(self):
        """删除上一次选择"""
        del(self.Node1[-1])
      
    def printData(self):
        """打印连接数据,用于检查"""
        print("Node1:")
        print (self.Node1)
        
        print ("Node2:")
        print (self.Node2)
      


    @classmethod
    def connectNode(cls, node1, node2):
        """
        作用：
            获取连接节点的位置,然后把节点设置为只读
        参数：
            node1 - 输出节点
            node2 - 输入节点
            node1_num - 输出端口号，默认第一个端口
            node2_num - 输出端口号，默认第一个端口
        返回：
            节点端口位置
        """
        


        node1_x = node1.getOutputPos()[0]
        node1_y = node1.getOutputPos()[1]

        node2_x = node2.getInputPos()[0]
        node2_y = node2.getInputPos()[1]

        return node1_x,node1_y,node2_x,node2_y
        


