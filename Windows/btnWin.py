from Qt.QtGui import QPixmap
from Qt.QtWidgets import QWidget,QVBoxLayout,QToolButton,QTextEdit
from Qt.QtCompat import loadUi
from Qt.QtCore import Slot, Signal, Qt, QEvent
from Qt.QtGui import QCursor
import os,json



try:
    from Zeus.settings.Setting import Data
except:
    from settings.Setting import Data


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
        

        self.ChildWin = None


        self.toolButton.clicked.connect(self.btnClicked)
        # self.toolButton.clicked.connect(lambda:self.showInfoWindow(type,name,searchPath))

        

    


        # Todo：读取数据库
        #加载资产数据到字典
        with open(file_path + r"\res\temp\asset.json") as js:
            asset_dir = json.load(js)
        




        #根据图片类型设置图片
        if (type == ".jpg" or type == ".jpeg" or type == ".png"):
            self.setPic(path)

        elif (type == ".obj"):
            self.setObjPic()


     



    def setUI(self):
        """设置界面"""
         #加载ui
        
        self.ui = loadUi(btnWin_ui)
        self.ui.setParent(self)
        
        #设置布局
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.ui)

    def deleteWin(self):
        """关闭窗口"""
        self.close()







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


    # 鼠标进入时显示信息窗口
    def enterEvent(self, event):
        
        pos = QCursor().pos()

        self.btnInfoWidget = BtnInfoWidget()
        self.btnInfoWidget.move(pos)
        self.btnInfoWidget.setText(self.path,self.type,self.name)
        self.btnInfoWidget.show()
        
        
        super(btnWin, self).enterEvent(event)
      
        
    # 鼠标离开时关闭信息窗口
    def leaveEvent(self,e):
        self.btnInfoWidget.close()
        
        super(btnWin, self).leaveEvent(e)



class BtnInfoWidget(QWidget):
    """信息窗口类"""
    def __init__(self):
        super(BtnInfoWidget,self).__init__()

        self.setUI()
    def setUI(self):
        styleSheet = """ 
            QWidget
            {
                color: #b1b1b1;
                background-color: #323232;
            }
            
            QWidget:item:hover
            {
                background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #ca0619);
                color: #000000;
            }
            
            QWidget:item:selected
            {
                background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
            }
            QTextEdit:focus
            {
                border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
            }
        """

        self.setStyleSheet(styleSheet)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        self.resize(Data.getWindowWidth()/4,Data.getWindowHeight()/4)
        self.setLayout(QVBoxLayout())
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.layout().addWidget(self.textEdit)

    # 设置文本内容
    def setText(self,path,type,name):
        
        self.textEdit.setText("文件名  :" + name + "\n"+"文件格式:" + type + "\n"+"保存路径:" + path + "\n")
 

    