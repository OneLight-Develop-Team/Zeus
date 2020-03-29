from PySide2.QtWidgets import QDialog,QPushButton,QVBoxLayout,QWidget
from PySide2 import QtCore
import PySide2.QtUiTools as QLoader
from functools import partial
import os
import NodeObj,NodeOutput

reload(NodeOutput)

reload(NodeObj)



#获取主文件目录
path = os.path.dirname(os.path.abspath(__file__))

srcPath = path + r"\src"


class NodeDialog(QDialog):
    """节点选择窗口"""    

    def __init__(self,x,y):
        super(NodeDialog, self).__init__()
        
        self.x = x
        self.y = y
         
        self.setObjectName("节点选择器")
        
        self.uiPath = srcPath + r"\NodeSelectDialog.ui"
       
        self.loader = QLoader.QUiLoader()

        self.ui = self.loader.load(self.uiPath)
        self.ui.setParent(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.node_contain = self.ui.findChild(QWidget, "node_contain_widget")
        
        
        self._node_path = []
        self._node_name = []
        self._node_type = []

        #用于当前定位节点
        self.nodeNum = 0



    def getNodeList(self,list_path,list_name,list_type):
        """获取节点列表"""
        self._node_path = list_path
        self._node_name = list_name
        self._node_type = list_type


        self.setNodeDialog()

    def setNodeDialog(self):
        """将加入的节点数据转换成按钮导入到窗口中"""
        self.node_contain.setLayout(QVBoxLayout())
        self.node_contain.layout().setMargin(0)
        self.node_contain.layout().setSpacing(0)


        # 输出按钮
        btn_output = QPushButton("Output")
        
        self.node_contain.layout().addWidget(btn_output)
        btn_output.clicked.connect(self.createNodeOutput)
        btn_output.clicked.connect(self.close)


        
        for name in self._node_name:
            
            btn = QPushButton(name)
            #btn.clicked.connect(lambda: self.node_btn_clicked(self._node_path[self.nodeNum], self._node_name[self.nodeNum], self._node_type[self.nodeNum]))
            #必须用particle,不然无法传入正确参数
            btn.clicked.connect(partial(self.node_btn_clicked, self._node_path[self.nodeNum], self._node_name[self.nodeNum], self._node_type[self.nodeNum]))
            btn.clicked.connect(self.close)
            self.node_contain.layout().addWidget(btn)
            self.nodeNum = self.nodeNum + 1



        # 关闭按钮
        btn_cancel = QPushButton("Cancel")
        
        self.node_contain.layout().addWidget(btn_cancel)
        
        btn_cancel.clicked.connect(self.close)
        self.node_contain.layout().addStretch()

        
        #重置到第一个节点
        self.nodeNum = 0
        

    def node_btn_clicked(self, path, name, type):
        """节点按钮点击"""
        # if type == ".jpg" or type == ".png" or type == ".jpeg":


        #     self.createNodeTexture(path,name)


        
        if type == ".obj":
            self.createNodeObj(path,name)





    # def createNodeTexture(self, path, name):
    #     """创建贴图节点"""
    #     node = NodeTexture.NodeTexture(self.parent(),self.x,self.y)

    #     node.setName(name)
    #     node.setPic(path)

    #     node.show()
    #     return node
    #     #self.parent().setFocus()


    def createNodeObj(self,path,name):
        """创建Obj节点"""
        node = NodeObj.NodeObj(self.parent(), self.x, self.y)
        node.setName(name)
        node.setFilePath(path)
        node.show()

    def createNodeOutput(self):
        """创建输出节点"""
        node = NodeOutput.NodeOutput(self.parent(),self.x,self.y)


        node.show()

  