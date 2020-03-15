from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolButton,QLabel
import PySide2.QtUiTools as QLoader
from PySide2.QtCore import Slot,Signal,SIGNAL
import os

# import houdiniPlay.Command as hc



#获取当前文件所在文件目录
current_path = os.path.dirname(os.path.abspath(__file__))


#获取资源文件路径
file_path = os.path.dirname(current_path)

#加载ui
btnWin_ui = file_path + r"\res\UI\btnWin.ui"

class btnWin(QWidget):
    """
    资源视图的按钮窗口
    type - 类型
    name - 名称
    path - 路径
    """    
    btn_clicked_signal = Signal(str,str,str)


    def __init__(self,path,type,name):
        super(btnWin, self).__init__()

        self.type = type
        self.name = name
        self.path = path
        self.setUI()

        self.toolButton = self.ui.findChild(QToolButton, "toolButton")
        self.label = self.ui.findChild(QLabel,"label")

        self.ChildWin = None


        self.toolButton.clicked.connect(self.btnClicked)
        # self.toolButton.clicked.connect(lambda:self.showInfoWindow(type,name,searchPath))

        

        self.setLabel(name)



        #根据图片类型设置图片
        if (type == ".jpg" or type == ".jpeg" or type == ".png"):
            self.setPic(path)

        elif (type == ".obj"):
            self.setObjPic()


     



    def setUI(self):
        """设置界面"""
         #加载ui
        loader = QLoader.QUiLoader()
        self.ui = loader.load(btnWin_ui)
        self.ui.setParent(self)
        
        #设置布局
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.ui)

    def deleteWin(self):
        """关闭窗口"""
        self.close()



    
    def setLabel(self, name):
        """将部件上的按钮名称设置为窗口名称"""
        self.label.setText(name)



    def setPic(self, filePath):
        """为toolButton设置图片图标"""
        pixmap = QPixmap(filePath)
        self.toolButton.setIcon(pixmap)
        self.toolButton.setIconSize(self.size())


    def setObjPic(self):
        """加载的是obj模型，设置obj的图片"""
        pixmap = QPixmap(file_path + r"\res\image\objimg.jpg")
        self.toolButton.setIcon(pixmap)
        self.toolButton.setIconSize(self.size())




 

    #点击按钮时发射自定义的信号到CenterWindow
    def btnClicked(self):
        self.btn_clicked_signal.emit(self.type,self.name,self.path)
