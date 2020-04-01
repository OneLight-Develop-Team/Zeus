# <-- coding utf-8 -->

from Qt.QtWidgets import QVBoxLayout,QWidget,QMenu,QMainWindow,QDockWidget,QFileDialog,QFileSystemModel, QMessageBox
#from Qt.QtCompat import loadUi
from Qt.QtCore import Qt

from PySide2.QtUiTools import QUiLoader

import Center
import  User
import Parmers
reload(Parmers)
from Parmers import ParmerPanel

from Node import NodePanel
import  View
import Tag

try:
    from Zeus.settings.Setting import Data
except:
    from settings.Setting import Data

import os
import pymongo
import sys
MODULE = r"D:\houdini\houdini\python2.7libs"
if MODULE not in sys.path:
    sys.path.append(MODULE)

try:
    import hou
except:
    pass

reload(User)
reload(View)
reload(Center)
reload(Tag)


#链接数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")
tagdb = client["tagdb"]  #标签数据库
tagcol = tagdb["tagcol"]  #标签集合

#获取当前文件所在路径
current_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.dirname(current_path)

class MainView(QWidget):
    """主窗口视图类"""
    def __init__(self):
        super(MainView, self).__init__()

        self.setupUI()
        self.setControl()

    #设置ui界面
    def setupUI(self):
       
        #加载ui,并设置ui界面
        # loader = QUiLoader()
        #self.ui = loadUi(file_path + "\\res\\UI\\MainWindow.ui")

        loader = QUiLoader()
        self.ui = loader.load(file_path + "\\res\\UI\\MainWindow.ui")

        self.ui.setParent(self)
        
        #设置窗口名称
        self.setWindowTitle(u"资产浏览器")

        #设置布局
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setContentsMargins(0,0,0,0)

        self.resize(Data.getWindowWidth(), Data.getWindowHeight())
        
        self.addWindow()

    #设置控件
    def setControl(self):
        #获取控件
        self.menu_window = self.ui.findChild(QMenu, "menu_window")
        self.menu_file = self.ui.findChild(QMenu, "menu_file")
        self.menu_edit = self.ui.findChild(QMenu,"menu_edit")
        

        self.action_param_panel = self.menu_window.addAction(u"参数面板")
        self.action_node_panel = self.menu_window.addAction(u"节点面板")
        self.action_user_panel = self.menu_window.addAction(u"用户页")
        self.action_view_panel = self.menu_window.addAction(u"视口")
        self.action_reset_window = self.menu_window.addAction(u"重置窗口")

        self.action_open_file = self.menu_file.addAction(u"打开文件")

        self.action_get_LOD = self.menu_edit.addAction(u"生成低精度模型")

        # 设置点击产生对号
        self.action_node_panel.setCheckable(True)
        self.action_node_panel.setChecked(True)
        self.action_user_panel.setCheckable(True)
        self.action_user_panel.setChecked(True)
        self.action_param_panel.setCheckable(True)
        self.action_param_panel.setChecked(True)
        self.action_view_panel.setCheckable(True)
        self.action_view_panel.setChecked(True)
    
    def addWindow(self):
        """添加中心窗口"""
        self.centerWindow = Center.CenterWindow()  
        self.ui.setCentralWidget(self.centerWindow)
        self.ui.setLayout(QVBoxLayout())
        self.show()

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

class MainModel():
    """主窗口数据类"""

    def __init__(self):
        pass

    # 生成低精度模型
    def genteralLOD(self, input, output, level=50):

        output = output + r"\\obj.obj"
        obj = hou.node("obj")
        geo = obj.createNode("geo")
        fileImport = geo.createNode("file")
        fileImport.parm("file").set(input)
        
        polyreduce = geo.createNode("polyreduce")    
        polyreduce.setFirstInput(fileImport)
        polyreduce.parm("percentage").set(level)
        
        fileExport = geo.createNode("file")
        fileExport.setFirstInput(polyreduce)
        fileExport.parm("filemode").set(2)
        fileExport.parm("file").set(output)
        fileExport.setDisplayFlag(1)
        fileExport.parm("reload").pressButton()


        
class MainController():
    """主窗口连接类"""
    userNameMT = None
    def __init__(self):

        # 初始化用户名
        self.username = None
        
        self.view = MainView()

        self.model = MainModel()


        self.setPanel()
        self.setActionConnect()
        self.setWindowsConnect()


    #初始创建界面
    def setPanel(self):
        self.setUserPanel()
        self.setViewPanel()

        self.setParmPanel()

        self.setNodePanel()

    #设置工具栏上的按钮与子窗口连接
    def setActionConnect(self):
        self.view.action_node_panel.triggered.connect(self.setNodePanel)
        self.view.action_param_panel.triggered.connect(self.setParmPanel)
        self.view.action_user_panel.triggered.connect(self.setUserPanel)
        self.view.action_view_panel.triggered.connect(self.setViewPanel)
        self.view.action_reset_window.triggered.connect(self.resetPanel)
        self.view.action_open_file.triggered.connect(self.openFile)


        self.view.action_get_LOD.triggered.connect(self.getLOD)

    # 设置节点编辑面板
    def setNodePanel(self):
        self.nodePanel = self.view.ui.findChild(QDockWidget, "nodePanel") 
        if(self.nodePanel == None):

            self.nodePanel = NodePanel()
            self.view.ui.addDockWidget(Qt.LeftDockWidgetArea,self.nodePanel)

        else:
            self.nodePanel.close()
            self.view.ui.removeDockWidget(self.nodePanel)
            del (self.nodePanel)
            self.view.action_node_panel.setChecked(False)
    

    
 
    # 设置用户面板
    def setUserPanel(self):
        self.userPanel = self.view.ui.findChild(QDockWidget, "UserPanel") 
        if(self.userPanel == None):
            self.userPanel =User.UserPanel()
            self.view.ui.addDockWidget(Qt.LeftDockWidgetArea,self.userPanel)

            # 登陆信号，获取用户名
            self.userPanel.Userlogin_signal.connect(lambda: self.getUNARS())

        else:
            self.userPanel.close()
            self.view.ui.removeDockWidget(self.userPanel)
            del(self.userPanel)
            self.view.action_user_panel.setChecked(False)
                
    # 设置视口
    def setViewPanel(self):
        self.viewPanel = self.view.ui.findChild(QDockWidget, "ViewPanel")
       
        if(self.viewPanel == None):
            self.viewPanel = View.ViewPanel()
            self.view.ui.addDockWidget(Qt.RightDockWidgetArea,self.viewPanel)

        else:
            self.viewPanel.close()
            self.view.ui.removeDockWidget(self.viewPanel)
            del (self.viewPanel)
            self.view.action_view_panel.setChecked(False)
            
    # 设置参数面板
    def setParmPanel(self):
        self.parmPanel = self.view.ui.findChild(QDockWidget, "parmPanel")
        if(self.parmPanel == None):
            self.parmPanel = ParmerPanel(self.username)
            self.view.ui.addDockWidget(Qt.RightDockWidgetArea,self.parmPanel)

        else:
            self.parmPanel.close()
            self.view.ui.removeDockWidget(self.parmPanel)
            del(self.parmPanel)
            self.view.action_param_panel.setChecked(False)
            
    # 设置节点编辑面板
    def setNodePanel(self):
        self.nodePanel = self.view.ui.findChild(QDockWidget, "nodePanel") 
        if(self.nodePanel == None):

            self.nodePanel = NodePanel()
            self.view.ui.addDockWidget(Qt.LeftDockWidgetArea,self.nodePanel)

        else:
            self.nodePanel.close()
            self.view.ui.removeDockWidget(self.nodePanel)
            del (self.nodePanel)
            self.view.action_node_panel.setChecked(False)
            
    #重置窗口布局
    def resetPanel(self):

        self.userPanel = self.view.ui.findChild(QDockWidget, "UserPanel") 
        if(self.userPanel != None):
            self.userPanel.close()
            self.view.ui.removeDockWidget(self.userPanel)
        self.userPanel = User.UserPanel()
        self.view.ui.addDockWidget(Qt.LeftDockWidgetArea, self.userPanel)

     
            
        self.viewPanel = self.view.ui.findChild(QDockWidget, "ViewPanel") 
        if(self.viewPanel != None):
            self.viewPanel.close()
            self.view.ui.removeDockWidget(self.viewPanel)
        self.viewPanel =View.ViewPanel()
        self.view.ui.addDockWidget(Qt.RightDockWidgetArea,self.viewPanel)
    

        self.parmPanel = self.view.ui.findChild(QDockWidget, "parmPanel") 
        if(self.parmPanel != None):
            self.parmPanel.close()
            self.view.ui.removeDockWidget(self.parmPanel)
        self.parmPanel = ParmerPanel(self.username)
        self.view.ui.addDockWidget(Qt.RightDockWidgetArea,self.parmPanel)
    
        self.nodePanel = self.view.ui.findChild(QDockWidget, "nodePanel") 
        if(self.nodePanel != None):
            self.nodePanel.close()
            self.view.ui.removeDockWidget(self.nodePanel)
        self.nodePanel = NodePanel()
        self.view.ui.addDockWidget(Qt.RightDockWidgetArea,self.nodePanel)


        self.view.action_view_panel.setChecked(True)
        self.view.action_user_panel.setChecked(True)
        self.view.action_node_panel.setChecked(True)
        self.view.action_file_panel.setChecked(True)
        self.view.action_param_panel.setChecked(True)

    #打开文件
    def openFile(self):

        self.getUsername()
        if self.username:  # 如果用户名存在，即已登陆
            dialog = QFileDialog()

            #根据当前所在文件目录，设置默认打开文件格式
            dialog.setNameFilter("全部文件 (*);;图片文件(*.jpg *.png *.jpe g);;模型文件(*.obj)")
            #加载对应的文件
            dialog.setFileMode(QFileDialog.ExistingFiles)
            dialog.setViewMode(QFileDialog.Detail)

            if dialog.exec_():
                self.paths = dialog.selectedFiles()

                # 创建标签选择窗口
                self.tagWidget = Tag.TagWidget(self.paths, self.username)
                self.tagWidget.show()
                self.tagWidget.send_tag_signal.connect(self.cenWinAddTags) # 链接添加标签的信号到中心窗口添加标签方法


        else:
            msgBox = QMessageBox()
            msgBox.setText(u'请先登陆！')
            msgBox.exec_()
            
           
    # 中心窗口添加新按钮
    def cenWinAddTags(self, tags):
        
        # 获取新添加的标签
        tags_add = tags.split(",")

        for tag in tags_add:
            
            self.view.centerWindow.setTag(tag)


                
                

    # 设置窗口之间的信号连接
    def setWindowsConnect(self):
        

        if self.viewPanel != None: # 设置中心窗口的按钮点击连接到视图窗口显示
            self.view.centerWindow.load_view_signal.connect(self.viewPanel.setView)

        if self.parmPanel != None: # 设置中心窗口的按钮点击连接到视图窗口显示
            self.view.centerWindow.load_view_signal.connect(self.parmPanel.setParam)

    # 生成低精度图片
    def getLOD(self):

   
        dialog = QFileDialog() 
        
        
        # self.path = dialog.getOpenFileName(self,'选择文件','')
        self.path = dialog.getExistingDirectory(self.view,
                                    "选取文件夹",
                                    "C:/")                                 #起始路径
      


        self.model.genteralLOD(r"E:\media\obj\cone.obj",self.path,5)

    def getUsername(self):
        self.username = self.userPanel.username  # 获取用户名

    def getUNARS(self):
        self.username = self.userPanel.username  # 获取用户名
        MainController.userNameMT = self.userPanel.username  # 获取用户名


        # self.parmPanel = self.view.ui.findChild(QDockWidget, "parmPanel")
        # if (self.parmPanel != None):
        #     self.parmPanel.close()
        #     self.view.ui.removeDockWidget(self.parmPanel)
        # self.parmPanel = ParmerPanel(self.username)
        # self.view.ui.addDockWidget(Qt.RightDockWidgetArea, self.parmPanel)

        #self.resetPanel()




Col = MainController()