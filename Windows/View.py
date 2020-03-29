# using utf-8

from Qt.QtWidgets import QWidget, QDockWidget,QVBoxLayout,QPushButton,QLabel,QHBoxLayout
from Qt.QtCore import Qt
from Qt.QtCompat import loadUi
from Qt.QtGui import QPixmap


# from Zeus.CefWidget.CefWidget import CefBrowser
# from Zeus.CefWidget.CefWidget import autoCefEmbed

# import houdiniPlay.Command as hc
try:
    from Zeus.settings.Setting import Data
except:
    from settings.Setting import Data


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

      
       

    # 设置UI界面
    def setupUI(self):
     
        self.setFloating(False)

        self.widget = QWidget()

       

       
        self.widget.setMinimumSize(Data.getWindowWidth()/4,Data.getWindowHeight()/4)
       
        self.setWidget(self.widget)



        # #加载ui,并设置ui界面
        # loader = QUiLoader()
        # self.ui = loader.load(file_path + "\\res\\UI\\UserLogin.ui")
        # self.ui.setParent(self.widget)
        # #设置布局
        # self.widget.layout().addWidget(self.ui)
        # self.widget.layout().setContentsMargins(0,0,0,0)

        self.setWindowTitle(u"视口")

    
        


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





            
"""



class TestWidget(QWidget):

    @autoCefEmbed(468/5,url="https://www.baidu.com/")
    def __init__(self, parent = None):
        super(TestWidget, self).__init__(parent)
       

        self.view = CefBrowser(self)
      
        
        m_vbox = QVBoxLayout()
        # m_button = QPushButton("Change Url")
        # m_button.clicked.connect(lambda:self.view.loadUrl(r"http://editor.l0v0.com/"))
        # m_vbox.addWidget(m_button)

        # m_button = QPushButton("Change Url2")
        # m_button.clicked.connect(lambda:self.view.loadUrl(r"http://www.bing.com/"))
        # m_vbox.addWidget(m_button)
        
        # m_button = QPushButton("Reload Url")
        # m_button.clicked.connect(lambda:self.view.reload())
        # m_vbox.addWidget(m_button)

        # m_button = QPushButton("backNavigate Url")
        # m_button.clicked.connect(lambda:self.view.goBack())
        # m_vbox.addWidget(m_button)

        # m_button = QPushButton("forwardNavigate Url")
        # m_button.clicked.connect(lambda:self.view.goForward())
        # m_vbox.addWidget(m_button)
        
        # m_button = QPushButton("get Url")
        # m_button.clicked.connect(lambda:sys.stdout.write(self.view.getUrl()+"\n"))
        # m_vbox.addWidget(m_button)

        m_vbox.addWidget(self.view)

      
        container = QWidget()

        container.setLayout(m_vbox)
      

        layout = QHBoxLayout()
        layout.addWidget(container)

        self.setLayout(layout)

            """