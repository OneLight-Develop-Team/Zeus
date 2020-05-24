# <-- coding utf-8 -->

from PySide import QtGui
from PySide import QtCore
from PySide.QtGui import QVBoxLayout, QMenu, QMainWindow, QDockWidget, QFileDialog, QFileSystemModel, \
     QMessageBox,QHBoxLayout,QToolBar,QPushButton
from Qt.QtCompat import loadUi
from PySide.QtCore import Qt
from PySide.QtGui import QPixmap

import Center
import User
import Parmers
import About
import Edit
reload(Edit)
import Tag
from settings.Setting import Data

import functools
import os
import pymongo
import sys

try:
    import hou
except:
    pass

from dayu_widgets.qt import QWidget, QVBoxLayout
from dayu_widgets.message import MMessage
from dayu_widgets import dayu_theme
import MenuBar
from dayu_widgets.drawer import MDrawer
from dayu_widgets.push_button import MPushButton
from dayu_widgets.qt import QFormLayout
from dayu_widgets.line_edit import MLineEdit


#链接数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")
tagdb = client["tagdb"]  #标签数据库
tagcol = tagdb["tagcol"]  #标签集合

#获取当前文件所在路径
current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.dirname(current_path)
ICONPATH = file_path + r"/res/image/ICON.png"
class MainView(QWidget):
    """主窗口视图类"""
    def __init__(self):
        super(MainView, self).__init__()
        self.setupUI()
      
    #设置ui界面
    def setupUI(self):
       
        self.setStyleSheet("color: #b1b1b1;background-color: #323232;")
        self.ui = loadUi(file_path + "\\res\\UI\\MainWindow.ui")
        self.ui.setParent(self)
        
        self.menubar = MenuBar.MenuTabWidgetExample()
        dayu_theme.apply(self.menubar)
        
        #设置窗口名称
        self.setWindowTitle(u"资源浏览器")

        #设置布局
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().addWidget(self.menubar)
        self.layout().addWidget(self.ui)
        
        self.addWindow()
        dayu_theme.apply(self)

        # 最小化************气泡** ************
        self.exitOnClose = False
        aMinimum = QtGui.QAction(QtGui.QIcon(), u"最小化到托盘", self)
        #aMinimum.triggered.connect(self.menubar)
        #self.menu_window.addAction(aMinimum)

        self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon(ICONPATH), self)
        #self.trayIcon.setContextMenu(self.menubar)
        self.trayIcon.activated.connect(self.trayIconActivated)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(ICONPATH), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.trayIcon.show()

    def addWindow(self):
        """添加中心窗口"""
        self.centerWindow = Center.CenterWindow()  
        self.ui.setCentralWidget(self.centerWindow)
        self.ui.setLayout(QVBoxLayout())
        

    def keyPressEvent(self, event):
        
        if (event.key() == Qt.Key_Shift):
            self.setKeyPress("shift",True)
        if (event.key() == Qt.Key_Control):
            self.setKeyPress("ctrl",True)
       

    def keyReleaseEvent(self, event):
        if (event.key() == Qt.Key_Shift):
            self.setKeyPress("shift",False)
        if (event.key() == Qt.Key_Control):
            self.setKeyPress("ctrl", False)

    # 传递键盘事件到中心窗口
    def setKeyPress(self, key, bool):
        try:
            self.centerWindow.widget.setKey(key, bool)

        except:
            pass
    

    
    def changeEvent(self, event):
        """
        重写窗口最小化事件
        """
        if event.type() == QtCore.QEvent.WindowStateChange:

            if self.windowState() & QtCore.Qt.WindowMinimized:
                QtCore.QTimer.singleShot(0, self.hide)

    def minimum(self):
        self.hide()

    def trayIconActivated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Context, QtGui.QSystemTrayIcon.DoubleClick):
            self.setWindowState(QtCore.Qt.WindowNoState)
            self.trayIcon.setIcon(QtGui.QIcon(ICONPATH))
            self.show()
            self.raise_()
        else:
            pass
    
        
class MainController():
    """主窗口连接类"""
    def __init__(self):
        
        self.view = MainView()
        
        self.userName = None  #保存用户名称
        self.hasLogin = False  #是否已经登录

        self.setActionConnect()
        self.view.centerWindow.load_view_signal.connect(self.addDrawer)
      
    #设置工具栏上的按钮与子窗口连接
    def setActionConnect(self):
        self.view.menubar.file_signal.connect(self.openFile)
        self.view.menubar.user_signal.connect(self.showUserPanel)
        self.view.menubar.edit_signal.connect(self.editFile)
        self.view.menubar.about_siganl.connect(self.showAbout)

    # 显示用户页
    def showUserPanel(self):
        if self.hasLogin:
            self.userInfo = User.editUserWinodw(self.userName)
            self.userInfo.show()
            self.userInfo.editUser_signal.connect(lambda:self.setUserName(self.userName))
        else:
            self.userPanel = User.UserPanel()
            self.userPanel.show()
            self.userPanel.login_signal.connect(self.setUserName)

    
    #设置用户信息
    def setUserName(self, username):
        self.userName = username
        MainController.userNameMT = self.userPanel.username  # 获取用户名
        self.hasLogin = True
        pixmap = QPixmap(file_path + "\\res\\headPortrial\\"+username + ".jpg")
        self.view.menubar.user_toolButton.setIcon(pixmap)
        self.view.menubar.label.setText(self.userName)


    # 弹出信息提示窗口
    def slot_show_message(self, func, config):
        func(config, parent=self.view)
        
    #打开文件
    def openFile(self):
 
        if self.hasLogin:
            dialog = QFileDialog()
            # dayu_theme.apply(dialog)
            dialog.setStyleSheet(Data.getQSS())
            #根据当前所在文件目录，设置默认打开文件格式
            dialog.setNameFilter(u"资源文件(*.png);;图片文件(*.jpg *.png *.jpeg);;")
            #加载对应的文件
            dialog.setFileMode(QFileDialog.ExistingFiles)
            dialog.setViewMode(QFileDialog.Detail)
            self.paths = None
            if dialog.exec_():
                self.paths = dialog.selectedFiles()
            if self.paths == None:
                return
            
            # 创建标签选择窗口
            self.tagWidget = Tag.TagWidget(self.paths, self.userName)
            self.tagWidget.show()
            Data.setWindowCenter(self.tagWidget)
            self.tagWidget.send_tag_signal.connect(self.cenWinAddTags) # 链接添加标签的信号到中心窗口添加标签方法
            self.tagWidget.load_file_signal.connect(self.slot_show_loading)

        else:
            
            self.slot_show_message(MMessage.info,(u'请先登录账号！'))
       

    # 中心窗口添加新按钮
    def cenWinAddTags(self, tags):
        
        # 获取新添加的标签
        tags_add = tags.split(",")
        
        for tag in tags_add:
            if tag.isspace() == False:
                
                self.view.centerWindow.addTag(tag)

    
    # 加载资源动画
    def slot_show_loading(self):
        msg = MMessage.loading(u'正在导入资源', parent=self.view)
        msg.sig_closed.connect(functools.partial(MMessage.success, u'资源导入成功', self.view))


    # 添加参数面板

    def addDrawer(self,type, name, path):
        if (self.userName == None):
            self.slot_show_message(MMessage.warning,u"请先登录账号")
            return
        self.parmerPanel = Parmers.ParmerPanel(self.userName)
        self.parmerPanel.setParam(type, name, path)
        self.parmerPanel.send_message_signal.connect(self.setMessageBox)
        self.custom_widget = QWidget()
        custom_lay = QFormLayout()
        self.custom_widget.setLayout(custom_lay)
        custom_lay.setContentsMargins(0,0,0,0)
        custom_lay.addWidget(self.parmerPanel)
      
        self.drawer = MDrawer(u'参数面板', parent=self.view.centerWindow)
        self.drawer.layout().setContentsMargins(0,0,0,0)
        self.drawer.setFixedWidth(Data.getWindowWidth()/3)
        self.drawer.set_widget(self.custom_widget)
        # self.drawer.layout().addWidget(self.custom_widget)
        
        dayu_theme.apply(self.drawer)

        self.drawer.show()

        # self.parmerPanel.model_widget.setMinimumSize(Data.getWindowHeight()/3,Data.getWindowHeight()/3)
        # self.view.centerWindow.layout().addWidget(self.parmerPanel.model_widget)
        self.parmerPanel.model_widget.embed() 
        self.parmerPanel.setModelWidget(path)   #设置3d视图
        
    def setMessageBox(self, s, str_get):
        if (s == "warnning"):
            MMessage.warning(str_get, parent=self.view)
        elif(s == "info"):
            MMessage.info(str_get, parent=self.view)
        elif (s == "success"):
            MMessage.success(str_get, parent=self.view)
        elif (s == "error"):
            MMessage.error(str_get, parent= self.view)

    
    def editFile(self):
        if self.hasLogin:
            paths = []
            for file in self.view.centerWindow.widget.fileList:
                paths.append(os.path.dirname(file))
            self.editPanel = Edit.EditWidget(paths)
            self.editPanel.send_message_signal.connect(self.setMessageBox)
            self.editPanel.show()
        else:
            self.slot_show_message(MMessage.info, (u'请先登录账号！'))
            
    def showAbout(self):
        self.aboutWidget = About.AboutWidget()
        self.aboutWidget.show()