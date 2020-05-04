# using utf-8

from Qt.QtWidgets import  QDockWidget, QVBoxLayout, QPushButton, QLineEdit, QHeaderView,\
    QLabel, QComboBox, QMessageBox, QRadioButton, QFileDialog, QSlider, QTableWidget,QTableWidgetItem,QHBoxLayout
#from Qt.QtCompat import loadUi
from Qt import QtCore, QtGui
from Qt.QtCore import Qt
from Qt.QtCompat import loadUi,setSectionResizeMode
from Qt.QtGui import QIcon

import os


import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')

import pymongo


import cv2

import functools

from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.tool_button import MToolButton
from dayu_widgets import dayu_theme
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.divider import MDivider
from dayu_widgets.breadcrumb import MBreadcrumb
from dayu_widgets.message import MMessage
from dayu_widgets.toast import MToast
from dayu_widgets.drawer import MDrawer
from dayu_widgets.qt import QFormLayout,MIcon
from dayu_widgets.button_group import MRadioButtonGroup
from dayu_widgets.slider import MSlider
from dayu_widgets.switch import MSwitch
from dayu_widgets.line_tab_widget import MLineTabWidget
from dayu_widgets.qt import QWidget,Qt
#获取当前文件所在路径
current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.dirname(current_path)



#储存头像的路径
hpPath = file_path + r"\res\headPortrial"

#链接数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")
userdb = client["userdb"]

try:
    from Zeus_Lin.settings.Setting import Data    
except:
    from settings.Setting import Data
class UserPanel(QWidget):
    """用户面板"""

    login_signal = QtCore.Signal(str)#用户面板的登陆信号
    CorrectUserName = None
    def __init__(self):
        super(UserPanel, self).__init__()

        self.username = None  # 初始化用户名
        self.imgPath =  hpPath + "\\" + "default.jpg" #保存用户头像
        self.password = None
        self.rePassword = None
        self.key = None
        self.WM = False

        self.login_userName = None
        self.login_password = None

        
        self.setObjectName("UserPanel")

        self.setupUI()
        self.setTabOrder(self.btn_sign_up,self.line_edit_name)
        self.setTabOrder(self.line_edit_name, self.line_edit_password)
        self.setTabOrder(self.line_edit_password, self.btn_sign_in)
        self.setTabOrder(self.btn_sign_in, self.btn_sign_up)
        

    # 设置用户界面
    def setupUI(self):
        
        self.setMinimumSize(Data.getWindowWidth() / 4.7, Data.getWindowHeight() / 2)
        self.setMaximumSize(Data.getWindowWidth() / 4.7, Data.getWindowHeight() / 2)
        self.setWindowModality(Qt.ApplicationModal)
        Data.setWindowCenter(self)
        self.setLayout(QVBoxLayout())

        
        btn = MPushButton("SIGNAL IN")
        btn.setIcon(QIcon(file_path + r"\res\ZeusDesign\a.png"))
 
        self.layout().addWidget(btn)
        self.layout().addWidget(MDivider())

        self.line_edit_name = MLineEdit()
        self.line_edit_name.setPlaceholderText('username')
        self.line_edit_name.set_prefix_widget(MToolButton().svg('user_line.svg').icon_only())
        self.line_edit_password = MLineEdit()
        self.line_edit_password.setPlaceholderText('password')
        self.line_edit_password.setEchoMode(QLineEdit.Password)
        self.line_edit_password.set_prefix_widget(MToolButton().svg('confirm_line.svg').icon_only())
        
        self.layout().addWidget(self.line_edit_name)
        self.layout().addWidget(self.line_edit_password)
       
        self.layout().addWidget(MDivider())
        self.btn_sign_in = MPushButton(u'登录').large().primary()
        self.layout().addWidget(self.btn_sign_in)

        self.btn_sign_up = MPushButton(u'注册').large().primary()
        self.layout().addWidget(self.btn_sign_up)

        
        dayu_theme.background_color = "#262626"
        dayu_theme.apply(self)

        self.layout().setContentsMargins(20,40,20,40)

        self.btn_sign_up.clicked.connect(self.on_sigin_up_click)
        self.btn_sign_in.clicked.connect(self.on_sigin_in_click)


        

        self.setWindowTitle(u"登录界面")

    # 弹出信息提示窗口
    def slot_show_message(self, func, config):
        func(config, parent=self)

    # 登录按钮按下,加载登录界面
    def on_sigin_in_click(self):
        self.login_userName = self.line_edit_name.text()
        self.login_password = self.line_edit_password.text()
        if not self.login_userName:
            self.slot_show_message(MMessage.error,(u'请输入用户名'))
            return 0
        if not self.login_password:
            self.slot_show_message(MMessage.error,(u'请输入密码'))
            return 0

        collist = userdb.list_collection_names()
        if self.login_userName in collist:  # 判断该用户是否存在
            colUser = userdb[self.login_userName]

            # Todo: 从数据库读取数据，判断是否名字存在，密码是否正确，成功则执行login函数，失败提示
            # 从数据库提取密码
            for x in colUser.find({"_id": "Password"}, {"Password": 1}):
                if "Password" in x:
                    DBpassword = x["Password"]
            if not DBpassword:
                
                return 0
            if self.login_password == DBpassword:
                saveLoginTime(self.login_userName)  # 保存登陆时间
                self.login_signal.emit(self.login_userName)  # 发射登陆信号
                UserPanel.CorrectUserName = self.login_userName
                msg = MToast.loading(u'正在登录中', parent=self)
                msg.sig_closed.connect(functools.partial(MToast.success, u'登录成功', self))
                self.close()
            else:
                self.slot_show_message(MMessage.error,(u'密码错误'))
        else:
            self.slot_show_message(MMessage.error,(u'该用户名不存在'))
            return 0
       
        
    # 设置注册界面
    def setRegeditWindow(self):
        self.custom_widget = QWidget()
        custom_lay = QFormLayout()
        self.custom_widget.setLayout(custom_lay)
        self.btn_regedit_image = MPushButton(u'选择文件')
        self.line_edit_regedit_name = MLineEdit()
        self.line_edit_regedit_password = MLineEdit()
        self.line_edit_regedit_password2 = MLineEdit()
        self.switch_identity = MSwitch().large()
        self.line_edit_email = MLineEdit()

        custom_lay.addRow(u' 选择头像:  ',self.btn_regedit_image)
        custom_lay.addRow(u' 账号名称:  ', self.line_edit_regedit_name)
        custom_lay.addRow(u' 用户邮箱:  ', self.line_edit_email)
        custom_lay.addRow(u' 账号密码:  ', self.line_edit_regedit_password)
        custom_lay.addRow(u' 确认密码:  ', self.line_edit_regedit_password2)
        custom_lay.addRow(u' 管理权限： ', self.switch_identity)
        # custom_lay.addRow(u'管理钥匙： ',self.line_edit_key)
        # self.custom_widget.layout().addRow(MLabel)
        self.drawer = MDrawer('Regedit', parent=self)
        submit_button = MPushButton(u'注册').primary()
        cancel_button = MPushButton(u'取消')
        self.drawer.add_button(cancel_button)
        self.drawer.add_button(submit_button)
        
        self.drawer.setFixedWidth(Data.getWindowWidth() / 5)
        self.drawer.set_widget(self.custom_widget)
        


        self.line_edit_regedit_name.setText(self.username)
        self.line_edit_regedit_password.setText(self.password)
        self.line_edit_regedit_password2.setText(self.rePassword)
        
        self.switch_identity.clicked.connect(self.signUpManager)
        self.btn_regedit_image.clicked.connect(self.setHeadPorfie)

        
        submit_button.clicked.connect(self.regedit)
        cancel_button.clicked.connect(self.drawer.close)

    # 注册按钮按下
    def on_sigin_up_click(self):
        self.slot_new_account()
      
    # 注册
    def slot_new_account(self):
        self.setRegeditWindow()
        self.drawer.show()
        
        

    # 设置头像
    def setHeadPorfie(self):

        dialog = QFileDialog()
        dialog.setStyleSheet(Data.getQSS())
        #根据当前所在文件目录，设置默认打开文件格式
        dialog.setNameFilter(u"图片文件(*.jpg *.png *.jpeg);;")
        #加载对应的文件
        dialog.setFileMode(QFileDialog.ExistingFiles)
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
            # pixmap = QtGui.QPixmap(hpPath + "\\" + "buffer.jpg")
            # self.lab_headProfile.setPixmap(pixmap)

            # 打开头像编辑器
            self.hpw = headProfieWindow(self.imgPath)
            self.hpw.show()
            # self.hpw.hPOK_signal.connect(lambda: self.setPicture())

    # #保存用户头像路径
    # def setPicture(self):
    #     self.imgPath = file_path + r"\res\headPortrial\buffer.jpg"
      
    # 设置管理员权限
    def signUpManager(self):
        if (self.WM):
            self.WM = False

            # self.custom_widget.layout().deleteLater(self.custom_widget.layout().itemAt(1))
            # self.custom_widget.layout().removeWidget(self.line_edit_key)
            # self.custom_widget.layout().removeWidget(self.key_label)
            # .deleteLater()
          
          
            self.key_label.deleteLater()
            self.line_edit_key.deleteLater()
            # self.key_widget.close()
        else:
            self.WM = True 
            self.key_label = MLabel(u"管理密钥:")
            self.line_edit_key = MLineEdit()
            # self.key_widget = QWidget()
            # self.key_widget.setLayout(QHBoxLayout())
            # self.key_widget.layout().addWidget(self.key_label)
            # self.key_widget.layout().addWidget(self.line_edit_key)
            self.custom_widget.layout().addRow(self.key_label,self.line_edit_key)
            # self.custom_widget.layout().addWidget(self.key_widget)

    #点击完成注册
    def regedit(self):
        self.username = self.line_edit_regedit_name.text()
        self.password = self.line_edit_regedit_password.text()
        self.rePassword = self.line_edit_regedit_password2.text()
        self.emailPath = self.line_edit_email.text()
        self.key = None

        #判断是否输入信息
        if not self.username:
            self.slot_show_message(MMessage.error, (u'请输入用户名！'))
            return 0

        if not self.emailPath:
            self.slot_show_message(MMessage.error, (u'请输入邮箱地址！'))
            return 0

        if not self.password:
            self.slot_show_message(MMessage.error,(u'请输入密码！'))
            return 0


        if not self.rePassword:
            self.slot_show_message(MMessage.error,(u'请再次输入密码！'))
            return 0
        if self.rePassword == self.password:
            
            
            collist = userdb.list_collection_names()
            if self.username in collist:  # 判断该用户是否存在
                self.slot_show_message(MMessage.error,(u'该用户已经存在'))
                
                return 0
            else:
                if self.WM:    #注册管理员
                    self.key = self.line_edit_key.text()
                    if self.key == "IDO":   #管理员密钥
                        saveUsername(self.username)
                        savePassword(self.username, self.password)
                        saveUserID(self.username, "管理员")
                        saveRegisterTime(self.username)
                        if self.imgPath:    #如果设置了截图
                            saveHeadPorfile(self.username, hpPath + "\\" + "buffer.jpg")
                        else:
                            saveHeadPorfile(self.username, hpPath + "\\" + "default.jpg")
                        self.drawer.close()    #注册成功，关闭窗口
                    else:
                        self.slot_show_message(MMessage.error,(u'密钥错误'))
                        return 0
                else:   #注册普通用户
                    saveUsername(self.username)
                    savePassword(self.username, self.password)
                    saveUserID(self.username, "普通用户")
                    saveEmail(self.emailPath)
                    saveRegisterTime(self.username)
                    if self.imgPath:  # 如果设置了头像截图
                        saveHeadPorfile(self.username, self.imgPath)
                    msg = MToast.loading(u'正在注册中', parent=self)
                    msg.sig_closed.connect(functools.partial(MToast.success, u'注册成功', self))
                    
                    self.drawer.close()  # 注册成功，关闭窗口
        else:
            self.slot_show_message(MMessage.error,(u'两次输入密码不一致！'))
            return 0





    # 登录，显示登录界面
    def login(self,name):
        self.widget = QWidget()
        self.widget.setMinimumSize(Data.getWindowWidth() / 6, Data.getWindowHeight() / 4)

        # 加载ui,并设置ui界面
        #self.ui = loadUi(file_path + "\\res\\UI\\LoginIn.ui")

        self.ui = loadUi(file_path + "\\res\\UI\\LoginIn.ui")

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
        

        self.Userlogin_signal.emit()

        # Todo 点击头像，可以更换头像界面，然后把头像写入数据库



    

    # 设置头像
    def setHeadPortrait(self, username, QWidget):
        path = file_path + r"\res\headPortrial\default.jpg"
        nameList = os.listdir(file_path + r"\res\headPortrial")
        for name in nameList:
            if (username + ".jpg") == name:
                path = file_path + r"\res\headPortrial" + "\\" + username + ".jpg"

        pixmap = QtGui.QPixmap(path)
        QWidget.setPixmap(pixmap)

    # #获得用户名并加载登录后用户界面
    # def getUsername(self):
    #     self.username = self.loginWin.username
    #     self.login(self.username)

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

#todo:保存邮箱地址
def saveEmail(email):
    print(email)

#保存登陆时间
def saveLoginTime(username):
    RTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    col = userdb[username]
    dict = {"Operation": "Login", "Time": RTime}
    col.insert_one(dict)
  


class headProfieWindow(QWidget):
    """
    头像编辑窗口
    """
    hPOK_signal = QtCore.Signal()   #确认头像信号
    def __init__(self,imgPath):
        super(headProfieWindow, self).__init__()
        # 加载ui,并设置ui界面
        #self.ui = loadUi(file_path + r"\res\UI\HeadProfileWindow.ui")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle(u"头像编辑器")
        
        # self.ui = loadUi(file_path + r"\res\UI\HeadProfileWindow.ui")

        # self.ui.setParent(self)

        self.imgPath = imgPath
        self.setLayout(QVBoxLayout())
        self.label_view = MLabel()
        self.label_view.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.label_view)
        
        self.layout().addWidget(MDivider(u'缩放'))
        self.hSlider_scale = MSlider(Qt.Horizontal)
        self.layout().addWidget(self.hSlider_scale)
        
        self.layout().addWidget(MDivider(u'垂直位移'))
        self.hSlider_moveH = MSlider(Qt.Horizontal)
        self.layout().addWidget(self.hSlider_moveH)

        self.layout().addWidget(MDivider(u'水平位移'))
        self.hSlider_moveV = MSlider(Qt.Horizontal)
        self.layout().addWidget(self.hSlider_moveV)
        self.layout().addStretch()
        
        self.btn_save_image = MPushButton(u'保存图片').large().primary()
        self.layout().addWidget(self.btn_save_image)

        dayu_theme.apply(self)
        self.setMinimumSize(Data.getWindowWidth() / 4.5, Data.getWindowHeight() / 1.7)
        self.setMaximumSize(Data.getWindowWidth() / 4.5, Data.getWindowHeight() / 1.7)
        self.layout().setContentsMargins(20,40,20,40)
        Data.setWindowCenter(self)


        self.hSlider_scale.setRange(0, 100)
        self.hSlider_moveH.setRange(0, 100)
        self.hSlider_moveV.setRange(0, 100)
        self.hSlider_scale.setValue(0)  #初始值
        self.hSlider_moveH.setValue(50)
        self.hSlider_moveV.setValue(50)

        #原图大小
        img = cv2.imread(self.imgPath)
        self.oiX = img.shape[0]
        self.oiY = img.shape[1]


        #获取初始值
        self.scale = self.hSlider_scale.value()
        self.mh = self.hSlider_moveH.value()
        self.mv = self.hSlider_moveV.value()


        #设置初始头像
        self.editPicture(self.scale, self.mh, self.mv)
        self.setPicteruView()

        # #链接信号与槽
        self.hSlider_scale.valueChanged.connect(lambda: self.scaleEdit())
        self.hSlider_moveH.valueChanged.connect(lambda: self.moveHEdit())
        self.hSlider_moveV.valueChanged.connect(lambda: self.moveVEdit())
        self.btn_save_image.clicked.connect(lambda: self.ok())


       

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
    
        self.setWindowModality(Qt.ApplicationModal)
 

        self.setMinimumSize(Data.getWindowHeight() / 1.5, Data.getWindowHeight() / 3)


        # self.setMinimumSize(Data.getWindowWidth() / 3, Data.getWindowHeight() / 3)
        # self.setMaximumSize(Data.getWindowWidth() / 3, Data.getWindowHeight() / 3)
        self.username = username
        self.key = None
        self.wchp = False
        self.wcun = False
        self.wcpw = False
        self.wcid = False

        # 设置窗口名称
        self.setWindowTitle(u"用户窗口")

            
        self.tab = MLineTabWidget()
        widget = QWidget()
        widget_child = QWidget()
        widget_child_2 = QWidget()
        widget.setLayout(QHBoxLayout())
        widget_child.setLayout(QVBoxLayout())
        widget_child_2.setLayout(QVBoxLayout())

        self.label_headProfile = MLabel()
        self.label_headProfile.setAlignment(Qt.AlignHCenter)
        self.btn_changeHead = MPushButton(u'选择新头像')
             
        widget_child.layout().addWidget(self.label_headProfile)
        widget_child.layout().addWidget(self.btn_changeHead)
        # widget_child.layout().addStretch()
        

        self.let_username  = MLineEdit(text='username')
        tool_button = MLabel(text=u'用户名').mark().secondary()
        tool_button.setAlignment(Qt.AlignCenter)
        tool_button.setFixedWidth(80)
        self.let_username.set_prefix_widget(tool_button)

        widget_child_2.layout().addWidget(self.let_username)

        self.let_ID = MLineEdit(text='identity')
        self.btn_changeID = MPushButton(text=u'修改身份').primary()
        self.btn_changeID.setFixedWidth(80)
        self.let_ID.set_suffix_widget(self.btn_changeID)
        widget_child_2.layout().addWidget(self.let_ID)

        self.let_key  = MLineEdit(text='')
        tool_button = MLabel(text=u'密钥').mark().secondary()
        tool_button.setAlignment(Qt.AlignCenter)
        tool_button.setFixedWidth(80)
        self.let_key.set_prefix_widget(tool_button)
        widget_child_2.layout().addWidget(self.let_key)
        

        self.let_password = MLineEdit(text='***********')
        self.btn_changePassword = MPushButton(text=u'修改密码').primary()
        self.btn_changePassword.setFixedWidth(80)
        self.let_password.set_suffix_widget(self.btn_changePassword)
        widget_child_2.layout().addWidget(self.let_password)
   
     
        self.btn_ok = MPushButton(u'确定').large().primary()
        self.btn_cancel = MPushButton(u'取消').large().primary()
        layout = QHBoxLayout()
        layout.addWidget(self.btn_ok)
        layout.addWidget(self.btn_cancel)

        widget_child_2.layout().addLayout(layout)

        widget.layout().addWidget(widget_child)
        widget.layout().addWidget(widget_child_2)

        self.tab.add_tab(widget, u'用户信息')

        widget2 = QWidget()
        self.ui = loadUi(file_path + r"\res\UI\EditUserWindow.ui")

        self.ui.setParent(widget2)
        widget2.setLayout(QVBoxLayout())
      
       
        widget2.layout().addWidget(self.ui)
        self.tableWidget_operationNode = self.ui.findChild(QTableWidget,"tableWidget_operationNode")

       
      
        self.tableWidget_operationNode.setStyleSheet(Data.getQSS())

       

        setSectionResizeMode(self.tableWidget_operationNode.horizontalHeader(), QHeaderView.Stretch)  # 自适应
        # widget2.layout().addSpacing(100)
        self.tab.add_tab(widget2, u'操作记录')
        
        btn_layout = QHBoxLayout()
      

        main_lay = QVBoxLayout()
        main_lay.addSpacing(20)
       
        main_lay.addWidget(self.tab)
       
        main_lay.addWidget(MDivider(u''))
        main_lay.addLayout(btn_layout)
        main_lay.addSpacing(20)
       
        self.setLayout(main_lay)
        dayu_theme.background_color = "#262626"
        dayu_theme.apply(self)
     

        
     
  
        # 设置默认值
        self.tableWidget_operationNode.setHorizontalHeaderLabels([u'操作', u'文件名', u'时间'])
        # 设置资产操作记录表：
      
      
        colUser = userdb[self.username]
        userlist = colUser.find({}, {"FileName": 1, "Operation": 1, "Time": 1})
     
        i = 0
        for xdir in userlist:
        
            if "Operation" in xdir:
                str1 = xdir["Operation"]
                
                newItem1 = QTableWidgetItem(str1)
                self.tableWidget_operationNode.setItem(i, 0, newItem1)

            if "FileName" in xdir:
                str2 = xdir["FileName"]
                newItem2 = QTableWidgetItem(str2)
                self.tableWidget_operationNode.setItem(i, 1, newItem2)

            if "Time" in xdir:
                str3 = xdir["Time"]
                newItem3 = QTableWidgetItem(str3)
                self.tableWidget_operationNode.setItem(i, 2, newItem3)
                i += 1

        #设置默认值
        pixmap = QtGui.QPixmap(hpPath + "\\" + self.username + ".jpg")
        self.label_headProfile.setPixmap(pixmap)
        self.let_username.setText(self.username)
        self.let_username.setReadOnly(True)#只读
        self.let_ID.setReadOnly(True)  # 只读
        self.let_password.setReadOnly(True)  # 只读
        self.let_password.setEchoMode(QLineEdit.Password)#输入密码形式
      
        
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
        dialog.setStyleSheet(Data.getQSS())
        #根据当前所在文件目录，设置默认打开文件格式
        dialog.setNameFilter(u"图片文件(*.jpg *.png *.jpeg);;")
        #加载对应的文件
        dialog.setFileMode(QFileDialog.ExistingFiles)
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
        self.slot_show_message(MMessage.success,(u'成功修改用户信息'))
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
            if self.let_ID.text() == u"普通用户":
                self.let_ID.setText(u"管理员")
            elif self.let_ID.text() == u"管理员":
                self.let_ID.setText(u"普通用户")
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
    
    # 弹出信息提示窗口
    def slot_show_message(self, func, config):
        func(config, parent=self)
