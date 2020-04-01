# using utf-8

from Qt.QtWidgets import QWidget, QDockWidget, QVBoxLayout, QPushButton, QLineEdit, \
    QLabel, QComboBox, QMessageBox, QRadioButton, QFileDialog, QSlider, QTableWidget
#from Qt.QtCompat import loadUi
from Qt import QtCore, QtGui

from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets

import os
import pymongo
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')
import cv2

#获取当前文件所在路径
current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.dirname(current_path)


#储存头像的路径
hpPath = file_path + r"\res\headPortrial"

#链接数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")
userdb = client["userdb"]

try:
    from Zeus.settings.Setting import Data
except:
    from settings.Setting import Data
class UserPanel(QDockWidget):
    """用户面板"""

    Userlogin_signal = QtCore.Signal()#用户面板的登陆信号

    def __init__(self):
        super(UserPanel, self).__init__()

        self.username = None  # 初始化用户名
        self.loginWin = loginWindow()  # 生成登陆界面实例
        # 链接登陆信号
        self.loginWin.login_signal.connect(lambda: self.getUsername())

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
        # loader = QUiLoader()
        #self.ui = loadUi(file_path + "\\res\\UI\\UserLogin.ui")

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
        self.label_headProfile = self.ui.findChild(QLabel, "label_headProfile")

        self.btn_sign_in.clicked.connect(self.on_sigin_in_click)
        self.btn_sign_up.clicked.connect(self.on_sigin_up_click)


        self.setWidget(self.widget)

        # 设置默认头像
        path = file_path + r"\res\headPortrial\default.jpg"
        pixmap = QtGui.QPixmap(path)
        self.label_headProfile.setPixmap(pixmap)


        

        self.setWindowTitle(u"用户界面")

    # 登录按钮按下,加载登录界面
    def on_sigin_in_click(self):
        self.loginWin.show()

        # self.widget = QWidget()
        # self.widget.setMinimumSize(Data.getWindowWidth() / 6, Data.getWindowHeight() / 4)
        #
        #
        #
        # #加载ui,并设置ui界面
        # self.ui = loadUi(file_path + "\\res\\UI\\SignIn.ui")
        # self.ui.setParent(self.widget)
        #
        # self.widget.setLayout(QVBoxLayout())
        # #设置布局
        # self.widget.layout().addWidget(self.ui)
        # self.setWidget(self.widget)
        #
        # self.lineEdit_name = self.ui.findChild(QLineEdit,"lineEdit_name")
        # self.lineEdit_passward = self.ui.findChild(QLineEdit, "lineEdit_passward")
        #
        # # Todo 设置密码为不可见
        #
        # self.btn_login = self.ui.findChild(QPushButton,"btn_login")
        #
        # self.btn_login.clicked.connect(self.on_btn_login)

    # 注册按钮按下
    def on_sigin_up_click(self):
        self.registerWin = registerWindow()
        self.registerWin.show()

        # self.widget = QWidget()
        # self.widget.setMinimumSize(Data.getWindowWidth() / 6, Data.getWindowHeight() / 4)
        #
        #
        #
        # #加载ui,并设置ui界面
        # self.ui = loadUi(file_path + "\\res\\UI\\SignUp.ui")
        # self.ui.setParent(self.widget)
        #
        # self.widget.setLayout(QVBoxLayout())
        # #设置布局
        # self.widget.layout().addWidget(self.ui)
        # self.setWidget(self.widget)
        #
        # self.btn_sign_up = self.ui.findChild(QPushButton, "btn_signUp")
        # self.lineEdit_sign_up_name = self.ui.findChild(QLineEdit,"lineEdit_name")
        # self.lineEdit_passward = self.ui.findChild(QLineEdit,"lineEdit_passward")
        # self.lineEdit_code = self.ui.findChild(QLineEdit, "lineEdit_code")
        # self.comboBox =self.ui.findChild(QComboBox,"comboBox")
        #
        # self.comboBox.addItem("普通用户")
        # self.comboBox.addItem("管理员")
        #
        #
        #
        #
        #
        # self.btn_sign_up.clicked.connect(self.signUp)


    # 登录界面里的登录按钮按下：
    def on_btn_login(self):
        pass
        # name = self.lineEdit_name.text()
        # passward = self.lineEdit_passward.text()
        #
        #
        # print (name)
        # print (passward)
        #
        # # Todo: 从数据库读取数据，判断是否名字存在，密码是否正确，成功则执行login函数，失败提示
        # self.login(name)


    # 登录，显示登录界面
    def login(self,name):
        self.widget = QWidget()
        self.widget.setMinimumSize(Data.getWindowWidth() / 6, Data.getWindowHeight() / 4)

        # 加载ui,并设置ui界面
        #self.ui = loadUi(file_path + "\\res\\UI\\LoginIn.ui")

        loader = QUiLoader()
        self.ui = loader.load(file_path + "\\res\\UI\\LoginIn.ui")

        self.ui.setParent(self.widget)

        self.widget.setLayout(QVBoxLayout())
        # 设置布局
        self.widget.layout().addWidget(self.ui)
        self.setWidget(self.widget)

        # 获取控件
        self.label_name = self.ui.findChild(QLabel, "label_name")
        self.label_identity = self.ui.findChild(QLabel, "label_identity")
        self.label_headLogin = self.ui.findChild(QLabel, "label_headLogin")
        self.btn_editUser = self.ui.findChild(QPushButton, "btn_editUser")

        self.tableWidget_operationNode = self.ui.findChild(QTableWidget, "tableWidget_operationNode")
        # 设置默认值
        self.tableWidget_operationNode.setHorizontalHeaderLabels(['操作', '文件名', '时间'])


        # 链接信号与槽函数
        self.btn_editUser.clicked.connect(lambda: self.editUser(name))

        #saveLoginTime(name)  # 储存登陆时间
        # Todo 根据名字访问数据库里的信息，加载到界面

        self.label_name.setText(name)  # 显示用户名

        colUser = userdb[name]
        for x in colUser.find({"_id": "UserID"}, {"UserID": 1}):
            ID = x["UserID"]
            self.label_identity.setText(ID)  # 显示身份

        # 设置头像
        self.setHeadPortrait(name, self.label_headLogin)

        #设置操作记录
        # 设置资产操作记录表：
        userlist = colUser.find({}, {"FileName": 1, "Operation": 1, "Time": 1})
        i = 0
        for xdir in userlist:

            if "Operation" in xdir:
                str1 = xdir["Operation"]
                print(str1)
                newItem1 = QtWidgets.QTableWidgetItem(str1)
                self.tableWidget_operationNode.setItem(i, 0, newItem1)

            if "FileName" in xdir:
                str2 = xdir["FileName"]
                newItem2 = QtWidgets.QTableWidgetItem(str2)
                self.tableWidget_operationNode.setItem(i, 1, newItem2)

            if "Time" in xdir:
                str3 = xdir["Time"]
                newItem3 = QtWidgets.QTableWidgetItem(str3)
                self.tableWidget_operationNode.setItem(i, 2, newItem3)
                i += 1


        self.Userlogin_signal.emit()

        # Todo 点击头像，可以更换头像界面，然后把头像写入数据库



    # 注册界面的注册按钮按下：
    def signUp(self):
        pass
        # name = self.lineEdit_sign_up_name.text()
        # passward = self.lineEdit_passward.text()
        # code = self.lineEdit_code.text()
        # identity = self.comboBox.currentText()
        #
        #
        # print (name)
        # print (passward)
        # print (code)
        # print (identity)
        #
        #
        # #Todo: 写入注册信息到库
        #
        # # 注册完自动转到已登录界面
        # self.login(name)

    # 设置头像
    def setHeadPortrait(self, username, QWidget):
        path = file_path + r"\res\headPortrial\default.jpg"
        nameList = os.listdir(file_path + r"\res\headPortrial")
        for name in nameList:
            if (username + ".jpg") == name:
                path = file_path + r"\res\headPortrial" + "\\" + username + ".jpg"

        pixmap = QtGui.QPixmap(path)
        QWidget.setPixmap(pixmap)

    #获得用户名并加载登录后用户界面
    def getUsername(self):
        self.username = self.loginWin.username
        self.login(self.username)

    #编辑用户信息
    def editUser(self, username):
        self.editUserWin = editUserWinodw(username)
        self.editUserWin.show()
        self.editUserWin.editUser_signal.connect(lambda: self.reSetUserInformation(username))#链接确认编辑信号与槽函

    #重新设置用户信息
    def reSetUserInformation(self, username):
        self.setHeadPortrait(username, self.label_headLogin)
        colUser = userdb[username]
        for x in colUser.find({"_id": "UserID"}, {"UserID": 1}):
            ID = x["UserID"]
            self.label_identity.setText(ID)  # 显示身份


class loginWindow(QWidget):
    """
    登录窗口类
    """
    login_signal = QtCore.Signal(str)

    def __init__(self):
        super(loginWindow, self).__init__()
        # 加载ui,并设置ui界面
        #self.ui = loadUi(file_path + r"\res\UI\loginWindow.ui")

        loader = QUiLoader()
        self.ui = loader.load(file_path + r"\res\UI\loginWindow.ui")

        self.ui.setParent(self)

        # 设置窗口名称
        self.setWindowTitle("登录")

        self.username = None
        self.password = None

        # 获取UI控件
        self.btn_register = self.ui.findChild(QPushButton, "btn_register")
        self.btn_login = self.ui.findChild(QPushButton, "btn_login")
        self.let_userName = self.ui.findChild(QLineEdit, "let_userName")
        self.let_password = self.ui.findChild(QLineEdit, "let_password")
        self.lab_headProfile = self.ui.findChild(QLabel, "lab_headProfile")

        # 设置默认值
        self.let_password.setEchoMode(QLineEdit.Password)
        path = file_path + r"\res\headPortrial\default.jpg"
        pixmap = QtGui.QPixmap(path)
        self.lab_headProfile.setPixmap(pixmap)

        # 链接信号与槽
        self.btn_register.clicked.connect(lambda: self.register())
        self.btn_login.clicked.connect(lambda: self.login())

    def login(self):

        self.username = self.let_userName.text()
        self.password = self.let_password.text()

        if not self.username:
            msgBox = QMessageBox()
            msgBox.setText(u'请输入用户名！')
            msgBox.exec_()
            return 0
        if not self.password:
            msgBox = QMessageBox()
            msgBox.setText(u'请输入密码！')
            msgBox.exec_()
            return 0

        collist = userdb.list_collection_names()
        if self.username in collist:  # 判断该用户是否存在
            colUser = userdb[self.username]

            # Todo: 从数据库读取数据，判断是否名字存在，密码是否正确，成功则执行login函数，失败提示
            # 从数据库提取密码
            for x in colUser.find({"_id": "Password"}, {"Password": 1}):
                if "Password" in x:
                    DBpassword = x["Password"]
            if not DBpassword:
                msgBox = QMessageBox()
                msgBox.setText(u'错误！找不到密码！')
                msgBox.exec_()
                return 0
            if self.password == DBpassword:
                saveLoginTime(self.username)  # 保存登陆时间
                self.login_signal.emit(self.username)  # 发射登陆信号
                self.close()
        else:
            msgBox = QMessageBox()
            msgBox.setText(u'用户不存在！')
            msgBox.exec_()
            return 0

    # 注册按钮按下
    def register(self):

        self.registerWin = registerWindow()
        self.registerWin.show()

        self.close()

class registerWindow(QWidget):
    """
    注册窗口类
    """
    def __init__(self):
        super(registerWindow, self).__init__()
        # 加载ui,并设置ui界面
        #self.ui = loadUi(file_path + r"\res\UI\signUpWindow.ui")

        loader = QUiLoader()
        self.ui = loader.load(file_path + r"\res\UI\signUpWindow.ui")

        self.ui.setParent(self)

        # 设置窗口名称
        self.setWindowTitle("注册")

        self.username = None
        self.password = None
        self.rePassword = None
        self.imgPath = None
        self.WM = False

        #获取控件
        self.let_username = self.ui.findChild(QLineEdit, "let_username")
        self.let_password = self.ui.findChild(QLineEdit, "let_password")
        self.let_rePassword = self.ui.findChild(QLineEdit, "let_rePassword")
        self.let_managerKey = self.ui.findChild(QLineEdit, "let_managerKey")
        self.lab_headProfile = self.ui.findChild(QLabel, "lab_headProfile")

        self.rbtn_ordinaryUser = self.ui.findChild(QRadioButton, "rbtn_ordinaryUser")
        self.rbtn_manager = self.ui.findChild(QRadioButton, "rbtn_manager")

        self.btn_signUp = self.ui.findChild(QPushButton, "btn_signUp")
        self.btn_setHeadPorfile = self.ui.findChild(QPushButton, "btn_setHeadPorfile")

        #设置默认值
        self.let_password.setEchoMode(QLineEdit.Password)
        self.let_rePassword.setEchoMode(QLineEdit.Password)
        self.rbtn_ordinaryUser.setChecked(True)

        # 设置头像
        defaultpath = file_path + r"\res\headPortrial\default.jpg"
        pixmap = QtGui.QPixmap(defaultpath)
        self.lab_headProfile.setPixmap(pixmap)

        #链接信号与槽函数
        self.btn_signUp.clicked.connect(lambda: self.signUp())
        self.rbtn_manager.toggled.connect(lambda: self.signUpManager())
        self.rbtn_ordinaryUser.toggled.connect(lambda: self.signUpOri())
        self.btn_setHeadPorfile.clicked.connect(lambda: self.setHeadPorfie())


    def signUp(self):
        self.username = self.let_username.text()
        self.password = self.let_password.text()
        self.rePassword = self.let_rePassword.text()
        self.key = None

        #判断是否输入信息
        if not self.username:
            msgBox = QMessageBox()
            msgBox.setText(u'请输入用户名！')
            msgBox.exec_()
            return 0
        if not self.password:
            msgBox = QMessageBox()
            msgBox.setText(u'请输入密码！')
            msgBox.exec_()
            return 0
        if not self.rePassword:
            msgBox = QMessageBox()
            msgBox.setText(u'请再次输入密码！')
            msgBox.exec_()
            return 0
        if self.rePassword == self.password:

            collist = userdb.list_collection_names()
            if self.username in collist:  # 判断该用户是否存在
                msgBox = QMessageBox()
                msgBox.setText(u'该用户已经存在！')
                msgBox.exec_()
                return 0
            else:
                if self.WM:    #注册管理员
                    self.key = self.let_managerKey.text()
                    if self.key == "IDO":   #管理员密钥
                        saveUsername(self.username)
                        savePassword(self.username, self.password)
                        saveUserID(self.username, "管理员")
                        saveRegisterTime(self.username)
                        if self.imgPath:    #如果设置了截图
                            saveHeadPorfile(self.username, hpPath + "\\" + "buffer.jpg")
                        else:
                            saveHeadPorfile(self.username, hpPath + "\\" + "default.jpg")
                        self.close()    #注册成功，关闭窗口
                    else:
                        msgBox = QMessageBox()
                        msgBox.setText(u'密钥错误！')
                        msgBox.exec_()
                        return 0
                else:   #注册普通用户
                    saveUsername(self.username)
                    savePassword(self.username, self.password)
                    saveUserID(self.username, "普通用户")
                    saveRegisterTime(self.username)
                    if self.imgPath:  # 如果设置了头像截图
                        saveHeadPorfile(self.username, self.imgPath)
                    self.close()  # 注册成功，关闭窗口
        else:
            msgBox = QMessageBox()
            msgBox.setText(u'两次输入的密码不一致！')
            msgBox.exec_()
            return 0

    def signUpManager(self):
        self.WM = True

    def signUpOri(self):
        self.WM = False

    def setHeadPorfie(self):
        # imgPath = r"C:\Users\Administrator\Pictures\Camera Roll\1.jpg"
        # img = cv2.imread(imgPaths)  # 读取本地图片，目前OpevCV支持bmp、jpg、png、tiff
        # cv2.imshow("Image", img)  # 显示图片
        # cv2.waitKey(0)  # 等待输入,这里主要让图片持续显示。
        # # cv2.waitKey(parameter)，parameter = NONE & 0表示一直显示，除此之外表示显示的毫秒数
        # cv2.destroyAllWindows()  # 释放窗口

        dialog = QFileDialog()
        # 根据当前所在文件目录，设置默认打开文件格式
        dialog.setNameFilter("图片文件(*.jpg *.png *.jpeg);")
        # 加载对应的文件
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setViewMode(QFileDialog.Detail)

        if dialog.exec_():
            imgPaths = dialog.selectedFiles()
            self.imgPath = imgPaths[0]


            img = cv2.imread(self.imgPath)
            flag = min(img.shape[0], img.shape[1])
            newimg = img[((img.shape[0] - flag) // 2):((img.shape[0] + flag) // 2),
                     ((img.shape[1] - flag) // 2):((img.shape[1] + flag) // 2)]
            newimg = cv2.resize(newimg, (150, 150), interpolation=cv2.INTER_AREA)
            cv2.imwrite(hpPath + "\\" + "buffer.jpg", newimg)#将图片作为缓存存入指定文件内
            pixmap = QtGui.QPixmap(hpPath + "\\" + "buffer.jpg")
            self.lab_headProfile.setPixmap(pixmap)

            self.hpw = headProfieWindow(self.imgPath)
            self.hpw.show()
            self.hpw.hPOK_signal.connect(lambda: self.setPicture())

    def setPicture(self):
        pixmap = QtGui.QPixmap(file_path + r"\res\headPortrial\buffer.jpg")
        self.lab_headProfile.setPixmap(pixmap)

class headProfieWindow(QWidget):
    """
    头像编辑窗口
    """
    hPOK_signal = QtCore.Signal()   #确认头像信号
    def __init__(self,imgPath):
        super(headProfieWindow, self).__init__()
        # 加载ui,并设置ui界面
        #self.ui = loadUi(file_path + r"\res\UI\HeadProfileWindow.ui")

        loader = QUiLoader()
        self.ui = loader.load(file_path + r"\res\UI\HeadProfileWindow.ui")

        self.ui.setParent(self)

        self.imgPath = imgPath

        #获取控件：
        self.label_view = self.ui.findChild(QLabel, "label_view")
        self.hSlider_scale = self.ui.findChild(QSlider, "hSlider_scale")
        self.hSlider_moveH = self.ui.findChild(QSlider, "hSlider_moveH")
        self.hSlider_moveV = self.ui.findChild(QSlider, "hSlider_moveV")
        self.btn_ok = self.ui.findChild(QPushButton, "btn_ok")

        #设置默认值：
        self.hSlider_scale.setRange(0, 100)
        self.hSlider_moveH.setRange(0, 100)
        self.hSlider_moveV.setRange(0, 100)
        self.hSlider_scale.setValue(0)  #初始值
        self.hSlider_moveH.setValue(50)
        self.hSlider_moveV.setValue(50)

        #获取初始值
        self.scale = self.hSlider_scale.value()
        self.mh = self.hSlider_moveH.value()
        self.mv = self.hSlider_moveV.value()
        #原图大小
        img = cv2.imread(self.imgPath)
        self.oiX = img.shape[0]
        self.oiY = img.shape[1]

        #设置初始头像
        self.editPicture(self.scale, self.mh, self.mv)
        self.setPicteruView()

        #链接信号与槽
        self.hSlider_scale.valueChanged.connect(lambda: self.scaleEdit())
        self.hSlider_moveH.valueChanged.connect(lambda: self.moveHEdit())
        self.hSlider_moveV.valueChanged.connect(lambda: self.moveVEdit())
        self.btn_ok.clicked.connect(lambda: self.ok())


    def editPicture(self,sn, mhn, mvn):

        img = cv2.imread(self.imgPath)  #每一次都是用原图编辑
        flag = min(img.shape[0], img.shape[1])

        sx = (flag - 150) * 0.01 * sn   #缩放的变化量
        hn = (img.shape[0] - 150) * 0.01 * (mhn - 50)* 0.01 * sn  #水平移动变化量
        vn = (img.shape[1] - 150) * 0.01 * (mvn - 50)* 0.01 * sn  #垂直移动变化量

        if (((img.shape[0] - flag) + sx + hn) // 2) < 0 or (((img.shape[1] - flag) + sx) // 2) < 0:
            newimg = img[(int((img.shape[0] - flag) + sx) // 2): (int((img.shape[0] + flag) - sx) // 2),
                     (int((img.shape[1] - flag) + sx) // 2):(int((img.shape[1] + flag) - sx) // 2)]
        else:
            newimg = img[(int((img.shape[0] - flag) + sx + hn) // 2): (int((img.shape[0] + flag) - sx + hn) // 2),
                     (int((img.shape[1] - flag) + sx + vn) // 2):(int((img.shape[1] + flag) - sx + vn) // 2)]




        # newimg = img[(int((img.shape[0] - flag) + sx) // 2): (int((img.shape[0] + flag) - sx) // 2),
        #          (int((img.shape[1] - flag) + sx) // 2):(int((img.shape[1] + flag) - sx) // 2)]

        newimg = cv2.resize(newimg, (150, 150), interpolation=cv2.INTER_AREA)
        cv2.imwrite(hpPath + "\\" + "buffer.jpg", newimg)  # 将图片作为缓存存入指定文件内


    def setPicteruView(self):
        imgPath = hpPath + "\\" + "buffer.jpg"
        pixmap = QtGui.QPixmap(imgPath)
        self.label_view.setPixmap(pixmap)

    def scaleEdit(self):
        self.scale = self.hSlider_scale.value()
        self.editPicture(self.scale, self.mh, self.mv)
        self.setPicteruView()

    def moveHEdit(self):
        self.mh = self.hSlider_moveH.value()
        self.editPicture(self.scale, self.mh, self.mv)
        self.setPicteruView()

    def moveVEdit(self):
        self.mv = self.hSlider_moveV.value()
        self.editPicture(self.scale, self.mh, self.mv)
        self.setPicteruView()

    def ok(self):
        self.hPOK_signal.emit()
        self.close()

class editUserWinodw(QWidget):
    """
    编辑用户信息窗口类
    """
    editUser_signal = QtCore.Signal()  #确认头像信号
    def __init__(self, username):
        super(editUserWinodw, self).__init__()
        #self.ui = loadUi(file_path + r"\res\UI\EditUserWindow.ui")

        loader = QUiLoader()
        self.ui = loader.load(file_path + r"\res\UI\EditUserWindow.ui")

        self.ui.setParent(self)

        self.username = username
        self.key = None
        self.wchp = False
        self.wcun = False
        self.wcpw = False
        self.wcid = False

        # 设置窗口名称
        self.setWindowTitle("登录")

        # 获取UI控件
        self.btn_changeHead = self.ui.findChild(QPushButton, "btn_changeHead")
        self.btn_changeUsername = self.ui.findChild(QPushButton, "btn_changeUsername")
        self.btn_changeID = self.ui.findChild(QPushButton, "btn_changeID")
        self.btn_changePassword = self.ui.findChild(QPushButton, "btn_changePassword")
        self.btn_ok = self.ui.findChild(QPushButton, "btn_ok")
        self.btn_cancel = self.ui.findChild(QPushButton, "btn_cancel")
        self.label_headProfile = self.ui.findChild(QLabel, "label_headProfile")
        self.let_username = self.ui.findChild(QLineEdit, "let_username")
        self.let_ID = self.ui.findChild(QLineEdit, "let_ID")
        self.let_password = self.ui.findChild(QLineEdit, "let_password")
        self.let_key = self.ui.findChild(QLineEdit, "let_key")


        #设置默认值
        pixmap = QtGui.QPixmap(hpPath + "\\" + self.username + ".jpg")
        self.label_headProfile.setPixmap(pixmap)
        self.let_username.setText(self.username)
        self.let_username.setReadOnly(True)#只读
        self.let_ID.setReadOnly(True)  # 只读
        self.let_password.setReadOnly(True)  # 只读
        self.let_password.setEchoMode(QLineEdit.Password)#输入密码形式
        #
        colUser = userdb[self.username]
        # 从数据库提取ID
        for x in colUser.find({"_id": "UserID"}, {"UserID": 1}):
            ID = x["UserID"]
            self.let_ID.setText(ID)  # 显示身份

        self.let_password.setText("**********")


        #链接信号与槽
        self.btn_changeHead.clicked.connect(lambda: self.editHeadProfile())
        self.btn_ok.clicked.connect(lambda: self.ok())
        self.btn_cancel.clicked.connect(lambda: self.cancel())
        self.btn_changePassword.clicked.connect(lambda: self.changePassword())
        self.btn_changeID.clicked.connect(lambda: self.setID())

    #修改头像
    def editHeadProfile(self):
        dialog = QFileDialog()
        # 根据当前所在文件目录，设置默认打开文件格式
        dialog.setNameFilter("图片文件(*.jpg *.png *.jpeg);")
        # 加载对应的文件
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setViewMode(QFileDialog.Detail)

        if dialog.exec_():
            imgPaths = dialog.selectedFiles()
            imgPath = imgPaths[0]

            self.editHeadProfileWin = headProfieWindow(imgPath)
            self.editHeadProfileWin.show()
            self.editHeadProfileWin.hPOK_signal.connect(lambda: self.setPicture())#选中图片，更新头像
            self.editHeadProfileWin.hPOK_signal.connect(lambda: self.setWCHP())
    #设置头像图片
    def setPicture(self):
        pixmap = QtGui.QPixmap(file_path + r"\res\headPortrial\buffer.jpg")
        self.label_headProfile.setPixmap(pixmap)


    def ok(self):
        # 保存头像
        if self.wchp:
            saveHeadPorfile(self.username, file_path + r"\res\headPortrial\buffer.jpg")
        if self.wcpw:
            self.setPassword()
            self.saveChangePasswordNode(self.username)
        if self.wcid:
            colUser = userdb[self.username]
            # 从数据库提取ID
            for x in colUser.find({"_id": "UserID"}, {"UserID": 1}):
                ID = x["UserID"]
            oldD = {"UserID": ID}
            newD = {"$set": {"UserID": self.let_ID.text()}}
            x = colUser.update_many(oldD, newD)
        self.editUser_signal.emit()#发射确认修改信号
        self.close()

    def cancel(self):
        self.close()

    def setWCHP(self):
        self.wchp = True

    def changePassword(self):
        self.let_password.setReadOnly(False)
        self.wcpw = True

    def setPassword(self):
        newPassword = self.let_password.text()
        if not newPassword:
            msgBox = QMessageBox()
            msgBox.setText(u'请输入密码！')
            msgBox.exec_()
            return 0
        colUser = userdb[self.username]
        # 从数据库提取密码
        for x in colUser.find({"_id": "Password"}, {"Password": 1}):
            if "Password" in x:
                DBpassword = x["Password"]
        oldD = {"Password": DBpassword}
        newD = {"$set": {"Password": newPassword}}
        x = colUser.update_many(oldD, newD)

    def setID(self):
        self.key = self.let_key.text()
        if self.key == "IDO":
            if self.let_ID.text() == "普通用户":
                self.let_ID.setText("管理员")
            elif self.let_ID.text() == "管理员":
                self.let_ID.setText("普通用户")
            self.wcid = True

    def saveChangePasswordNode(self, username):
        RTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # 将浏览信息存入用户数据库
        col = userdb[username]
        dict = {"Operation": "ChangePassword", "Time": RTime}
        col.insert_one(dict)

    # def changeUsername(self):
    #     self.let_username.setReadOnly(False)
    #     self.wcun = True

    # def setUsername(self):
    #     newname = self.let_username.text()
    #     collist = userdb.list_collection_names()
    #     if newname in collist:
    #         print("The username already exists")
    #         return 0

#路径里不能出现中文？？？
def saveHeadPorfile(username,imgPath):
    img = cv2.imread(imgPath)  # 读取本地图片，目前OpevCV支持bmp、jpg、png、tiff
    # cv2.imshow("Image", img)  # 显示图片
    # cv2.waitKey(0)  # 等待输入,这里主要让图片持续显示。
    # cv2.destroyAllWindows()  # 释放窗口
    flag = min(img.shape[0], img.shape[1])  # flag为较小的边的像素个数
    newimg = img[((img.shape[0] - flag) // 2):((img.shape[0] + flag) // 2),
             ((img.shape[1] - flag) // 2):((img.shape[1] + flag) // 2)]
    # newimg为原图把较长的边取中间，裁剪成正方形的图。
    newimg = cv2.resize(newimg, (150, 150), interpolation=cv2.INTER_AREA)
    #newimg为缩小至150*150大小的图片
    cv2.imwrite(hpPath + "\\" + username + ".jpg", newimg)


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
    dict = {"_id": "RegisterTime", "Time": RTime, "Operation":"Register"}
    col.insert_one(dict)

#保存登陆时间
def saveLoginTime(username):
    RTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    col = userdb[username]
    dict = {"Operation": "Login", "Time": RTime}
    col.insert_one(dict)