# using utf-8

from PySide2.QtWidgets import QWidget, QDockWidget,QVBoxLayout,QPushButton,QLineEdit,QLabel,QComboBox,QMessageBox,QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt
from PySide2 import QtGui
import os
import pymongo
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#获取当前文件所在路径
current_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.dirname(current_path)

#链接数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")
userdb = client["userdb"]


from settings.Setting import Data
class UserPanel(QDockWidget):
    """用户面板"""
    def __init__(self):
        super(UserPanel, self).__init__()

        self.username = None    #初始化用户名

        self.setObjectName("UserPanel")

        self.setupUI()

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
        self.label_headPortrial = self.ui.findChild(QLabel, "label_headPortrial")
        
        self.btn_sign_in.clicked.connect(self.on_sigin_in_click)
        self.btn_sign_up.clicked.connect(self.on_sigin_up_click)


        self.setWidget(self.widget)

        #设置默认头像
        path = file_path + r"\res\headPortrial\default.jpg"
        self.setHeadPortrait(path,self.label_headPortrial)
        

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
        self.label_headSignin = self.ui.findChild(QLabel, "label_headSignin")

        #设置默认头像
        path = file_path + r"\res\headPortrial\default.jpg"
        self.setHeadPortrait(path, self.label_headSignin)

        
        # Todo 设置密码为不可见
        self.lineEdit_passward.setEchoMode(QLineEdit.Password)
        
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

        if not name:
            msgBox = QMessageBox()
            msgBox.setText(u'请输入用户名！')
            msgBox.exec_()
            return 0
        if not passward:
            msgBox = QMessageBox()
            msgBox.setText(u'请输入密码！')
            msgBox.exec_()
            return 0

        collist = userdb.list_collection_names()
        if name in collist:  # 判断该用户是否存在
            colUser = userdb[name]

            # Todo: 从数据库读取数据，判断是否名字存在，密码是否正确，成功则执行login函数，失败提示
            # 从数据库提取密码
            for x in colUser.find({"_id":"Password"}, {"Password": 1}):
                if "Password" in x:
                    DBpassword = x["Password"]
            if not DBpassword:
                msgBox = QMessageBox()
                msgBox.setText(u'错误！找不到密码！')
                msgBox.exec_()
                return 0
            if passward == DBpassword:
                self.login(name)
                self.username = name
        else:
            msgBox = QMessageBox()
            msgBox.setText(u'用户不存在！')
            msgBox.exec_()
            return 0
        



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
        self.label_headLogin = self.ui.findChild(QLabel,"label_headLogin")

        saveLoginTime(name)#储存登陆时间
        # Todo 根据名字访问数据库里的信息，加载到界面

        self.label_name.setText(name)#显示用户名

        colUser = userdb[name]
        for x in colUser.find({"_id":"UserID"},{"UserID":1}):
            ID = x["UserID"]
            self.label_identity.setText(ID)#显示身份

        #设置默认头像
        path = file_path + r"\res\headPortrial\default.jpg"
        self.setHeadPortrait(path, self.label_headLogin)

        # Todo 点击头像，可以更换头像界面，然后把头像写入数据库



    # 注册界面的注册按钮按下：
    def signUp(self):
        name = self.lineEdit_sign_up_name.text()
        passward = self.lineEdit_passward.text()
        code = self.lineEdit_code.text()
        identity = self.comboBox.currentText()

        if not name:
            msgBox = QMessageBox()
            msgBox.setText(u'请输入用户名！')
            msgBox.exec_()
            return 0
        if not passward:
            msgBox = QMessageBox()
            msgBox.setText(u'请输入密码！')
            msgBox.exec_()
            return 0
        if identity == "管理员":
            if not (code == "111"):    #管理员密钥！！！！！！！！！！！！！！
                msgBox = QMessageBox()
                msgBox.setText(u'邀请码错误！请重新输入或者转为普通用户')
                msgBox.exec_()
                return 0

        # Todo: 写入注册信息到库
        collist = userdb.list_collection_names()
        if name in collist:  # 判断该用户是否存在
            msgBox = QMessageBox()
            msgBox.setText(u'该用户已经存在！')
            msgBox.exec_()
            return 0
        else:
            saveUsername(name)
            savePassword(name,passward)
            saveUserID(name,identity)
            saveRegisterTime(name)
            # 注册完自动转到已登录界面
            self.login(name)

    def setHeadPortrait(self,path,QWidget):
        # 设置头像
        defaultpath = file_path + r"\res\headPortrial\default.jpg"
        pixmap = QtGui.QPixmap(defaultpath)
        QWidget.setPixmap(pixmap)


    def findHeadPortrial(self):
        dialog = QFileDialog()
        # 根据当前所在文件目录，设置默认打开文件格式
        dialog.setNameFilter("图片文件(*.jpg *.png *.jpeg);")
        # 加载对应的文件
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setViewMode(QFileDialog.Detail)

        if dialog.exec_():
            self.paths = dialog.selectedFiles()






#保存用户名
def saveUsername(username):
    col = userdb[username]
    dict = {"_id": "UserName", "UserName":username}
    x= col.insert_one(dict)

#保存密码
def savePassword(username, password):
    col = userdb[username]
    dict = {"_id": "Password", "Password":password}
    col.insert_one(dict)

#保存身份
def saveUserID(username, userID):
    col = userdb[username]
    dict = {"_id": "UserID", "UserID": userID}
    col.insert_one(dict)

#保存注册时间
def saveRegisterTime(username):
    RTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    col = userdb[username]
    dict = {"_id": "RegisterTime", "Time": RTime}
    col.insert_one(dict)

#保存登陆时间
def saveLoginTime(username):
    RTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    col = userdb[username]
    dict = {"Operation": "Login", "Time": RTime}
    col.insert_one(dict)