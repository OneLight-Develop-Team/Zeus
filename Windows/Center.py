# <-- coding utf-8 -->

from PySide2.QtWidgets import QWidget,QVBoxLayout,QPushButton,QRadioButton
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Signal
# from setting.Setting import Data
from Windows.layouitflow import FlowLayout
import os,json

# from Window.btnWin import btnWin

# glonal_type = [".png",".jpg",".jpeg",".obj"]

#获取当前文件所在路径
current_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.dirname(current_path)



class CenterWindow(QWidget):
    """中心窗口类"""

    # load_view_signal = Signal()

    def __init__(self):

        super(CenterWindow,self).__init__()

        self.setObjectName("CenterWindow")
      
        self.setupUI()

        


    # 设置UI界面
    def setupUI(self):

        self.setWindowTitle("浏览窗口")

       
        #加载ui,并设置ui界面
        loader = QUiLoader()
        self.ui = loader.load(file_path + "\\res\\UI\\CenterWidget.ui")
        self.ui.setParent(self)

        #设置布局
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setContentsMargins(0,0,0,0)


        self.widget = self.ui.findChild(QWidget,"widget")

        self.flowLayout = FlowLayout()
        self.widget.setLayout(self.flowLayout)

    # # 添加文件内容
    # def addSource(self, tag):
       
    #     #清除原有组件
    #     for i in range(self.widget.layout().count()): 
    #         self.widget.layout().itemAt(i).widget().deleteLater()
        
    #     #加载保存数据到字典
    #     with open(file_path + r"\res\temp\asset.json") as js:
    #         asset_dir = json.load(js)
      

    #     # 添加所有子文件到列表中
    #     for key in asset_dir.keys():
    #         if (tag in asset_dir[key]["tags"]):
    #             if(asset_dir[key]["type"] in glonal_type):


    #                 self.addFile(key,asset_dir[key]["type"],asset_dir[key]["name"])
                
          
    # # 添加按钮
    # def addFile(self, path, type, name):
        

            
    #     myBtnWin = btnWin(path,type,name)
      
    #     # myBtnWin.btn_clicked_signal.connect(self.setView)
    #     self.widget.layout().addWidget(myBtnWin)

        



        

    # def getFileEnd(self, filename):
    #     """获取文件后缀"""
    #     return os.path.splitext(filename)[-1]


    # # 设置视图
    # def setView(self, type, name, path):
    #     self.type = type
    #     self.name = name
    #     self.path = path
    #     self.load_view_signal.emit()


