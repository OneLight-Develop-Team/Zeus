from Qt.QtGui import QPixmap
from Qt.QtWidgets import QWidget, QVBoxLayout, QToolButton, QTextEdit,QLabel
from Qt.QtCompat import loadUi


from Qt.QtCore import Slot, Signal, Qt, QEvent
from Qt.QtGui import QCursor
import os



from settings.Setting import Data





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
      

        # 根据图片类型设置图片
        if (type == "jpg" or type == "jpeg" or type == "png"):
            self.setPic(path,name)

        elif (type == "obj" or type == "fbx"):
            self.setObjPic()





    def setUI(self):
        """设置界面"""
         #加载ui
        
        #self.ui = loadUi(btnWin_ui)


        self.ui = loadUi(btnWin_ui)

        self.ui.setParent(self)
        
        #设置布局
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(1.5,1.5,1.5,1.5)
        self.layout().addWidget(self.ui)

    def deleteWin(self):
        """关闭窗口"""
        self.close()







    def setPic(self,filePath, fileName):
        """为toolButton设置图片图标"""
        
        # try:

        #     thumbPath = file_path + "\\res\\image\\thumbnail\\"+fileName
        #     pixmap = QPixmap(thumbPath)
            
        # except:
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
        self.btn_clicked_signal.emit(self.type, self.name, self.path)
        
 
"""
    # 鼠标进入时显示信息窗口
    def enterEvent(self, event):
        
        pos = QCursor().pos()

     
        self.btnInfoWidget = BtnInfoWidget(self.path,self.type,self.name)
        self.btnInfoWidget.move(pos.x()+50,pos.y()+50)
        self.btnInfoWidget.move(self.width() + self.geometry().x() + self.parent().parent().geometry().x(), \
            self.height() + self.geometry().y() +self.parent().parent().geometry().y())
        
        self.btnInfoWidget.show()
        
        super(btnWin, self).enterEvent(event)
        
    # 鼠标离开时关闭信息窗口
    def leaveEvent(self, e):
     
        self.btnInfoWidget.close()
     
        super(btnWin, self).leaveEvent(e)
"""


class BtnInfoWidget(QTextEdit):
    """信息窗口类"""
   
    def __init__(self,path,type,name):
        super(BtnInfoWidget,self).__init__()

      
        styleSheet = """ 

         
            QTextEdit
            {
                color: #b1b1b1;
                background-color: #323232;
                border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
            }
        """

        self.setStyleSheet(styleSheet)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        self.resize(Data.getWindowWidth()/4,Data.getWindowHeight()/4)
     
        self.setReadOnly(True)

       
 
        filepath = os.path.dirname(path)
        filename = filepath.split("/")[-1]
        type = "obj"
        for name in os.listdir(filepath):
            if (name.split(".")[-1] == "obj"):
                type == "obj"
            elif (name.split(".")[-1] == "fbx"):
                type == "fbx"
        
        self.setText(u"资产名  :" + filename + "\n"+u"文件格式:" + type + "\n"+u"资产路径:"+"\n" + filepath + "\n")
 
