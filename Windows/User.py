# using utf-8

from PySide2.QtWidgets import QWidget, QDockWidget,QVBoxLayout,QPushButton,QLineEdit,QLabel,QComboBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt
import os

import sys
reload(sys)
sys.setdefaultencoding('utf8')

#获取当前文件所在路径
current_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.dirname(current_path)

from Zeus.settings.Setting import Data
class UserPanel(QDockWidget):
    """用户面板"""
    def __init__(self):
        super(UserPanel, self).__init__()

        self.setObjectName("UserPanel")

        self.setupUI()
        # self.show()

    # 设置UI界面
    def setupUI(self):
        # self.setStyleSheet("background-color:rgb(20,222,255)")
        self.setFloating(False)
        self.setFeatures(QDockWidget.DockWidgetVerticalTitleBar|QDockWidget.AllDockWidgetFeatures)

        self.widget = QWidget()
        self.widget.setMinimumSize(Data.getWindowWidth() / 6, Data.getWindowHeight() / 4)

        

        #加载ui,并设置ui界面
        loader = QUiLoader()
        self.ui = loader.load(file_path + "\\res\\UI\\UserLogin.ui")
        self.ui.setParent(self.widget)

        self.widget.setLayout(QVBoxLayout())
        #设置布局
        self.widget.layout().addWidget(self.ui)
        self.widget.layout().setContentsMargins(0,0,0,0)

        # 获取控件
        self.btn_sign_in = self.ui.findChild(QPushButton, "btn_sign_in")
        self.btn_sign_up = self.ui.findChild(QPushButton, "btn_sign_up")
        
        self.btn_sign_in.clicked.connect(self.on_sigin_in_click)
        self.btn_sign_up.clicked.connect(self.on_sigin_up_click)


        self.setWidget(self.widget)


        

        self.setWindowTitle("用户界面")

    # 登录按钮按下,加载登录界面
    def on_sigin_in_click(self):

        self.widget = QWidget()
        self.widget.setMinimumSize(Data.getWindowWidth() / 6, Data.getWindowHeight() / 4)

        

        #加载ui,并设置ui界面
        loader = QUiLoader()
        self.ui = loader.load(file_path + "\\res\\UI\\SignIn.ui")
        self.ui.setParent(self.widget)

        self.widget.setLayout(QVBoxLayout())
        #设置布局
        self.widget.layout().addWidget(self.ui)
        self.setWidget(self.widget)

        self.lineEdit_name = self.ui.findChild(QLineEdit,"lineEdit_name")
        self.lineEdit_passward = self.ui.findChild(QLineEdit, "lineEdit_passward")
        
        # Todo 设置密码为不可见
        
        self.btn_login = self.ui.findChild(QPushButton,"btn_login")

        self.btn_login.clicked.connect(self.on_btn_login)

    # 注册按钮按下
    def on_sigin_up_click(self):
        self.widget = QWidget()
        self.widget.setMinimumSize(Data.getWindowWidth() / 6, Data.getWindowHeight() / 4)

        

        #加载ui,并设置ui界面
        loader = QUiLoader()
        self.ui = loader.load(file_path + "\\res\\UI\\SignUp.ui")
        self.ui.setParent(self.widget)

        self.widget.setLayout(QVBoxLayout())
        #设置布局
        self.widget.layout().addWidget(self.ui)
        self.setWidget(self.widget)

        self.btn_sign_up = self.ui.findChild(QPushButton, "btn_signUp")
        self.lineEdit_sign_up_name = self.ui.findChild(QLineEdit,"lineEdit_name")
        self.lineEdit_passward = self.ui.findChild(QLineEdit,"lineEdit_passward")
        self.lineEdit_code = self.ui.findChild(QLineEdit, "lineEdit_code")
        self.comboBox =self.ui.findChild(QComboBox,"comboBox")

        self.comboBox.addItem("普通用户")
        self.comboBox.addItem("管理员")
        
        



        self.btn_sign_up.clicked.connect(self.signUp)


    # 登录界面里的登录按钮按下：
    def on_btn_login(self):
        name = self.lineEdit_name.text()
        passward = self.lineEdit_passward.text()

     
        print (name)
        print (passward)
        
        # Todo: 从数据库读取数据，判断是否名字存在，密码是否正确，成功则执行login函数，失败提示
        self.login(name)


    # 登录，显示登录界面
    def login(self,name):
        self.widget = QWidget()
        self.widget.setMinimumSize(Data.getWindowWidth() / 6, Data.getWindowHeight() / 4)
        

        #加载ui,并设置ui界面
        loader = QUiLoader()
        self.ui = loader.load(file_path + "\\res\\UI\\LoginIn.ui")
        self.ui.setParent(self.widget)

        self.widget.setLayout(QVBoxLayout())
        #设置布局
        self.widget.layout().addWidget(self.ui)
        self.setWidget(self.widget)

        self.label_name = self.ui.findChild(QLabel,"label_name")
        self.label_identity = self.ui.findChild(QLabel,"label_identity")
        self.label_head = self.ui.findChild(QLabel,"label_head")

        # Todo 根据名字访问数据库里的信息，加载到界面

        

        # Todo 点击头像，可以更换头像界面，然后把头像写入数据库



    # 注册界面的注册按钮按下：
    def signUp(self):
        name = self.lineEdit_sign_up_name.text()
        passward = self.lineEdit_passward.text()
        code = self.lineEdit_code.text()
        identity = self.comboBox.currentText()


        print (name)
        print (passward)
        print (code)
        print (identity)
        
        
        #Todo: 写入注册信息到库

        # 注册完自动转到已登录界面
        self.login(name)