# <-- coding utf-8 -->

from PySide2.QtWidgets import QVBoxLayout,QWidget,QMenu,QMainWindow,QDockWidget,QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt

import Center
import FileTree
import  User
from Parmers import ParmerPanel
from Node import NodePanel
import  View
import Tag

from Zeus.settings.Setting import Data
import os

reload(User)
reload(View)
reload(FileTree)
reload(Center)
reload(Tag)



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
        loader = QUiLoader()
        self.ui = loader.load(file_path + "\\res\\UI\\MainWindow.ui")
        self.ui.setParent(self)
        
        #设置窗口名称
        self.setWindowTitle("资产浏览器")

        #设置布局
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setContentsMargins(0,0,0,0)

        self.resize(Data.getWindowWidth(),Data.getWindowHeight())

    #设置控件
    def setControl(self):
        #获取控件
        self.menu_window = self.ui.findChild(QMenu, "menu_window")
        self.menu_file = self.ui.findChild(QMenu, "menu_file")
        
        self.action_file_panel = self.menu_window.addAction(u"大纲视图")
        self.action_param_panel = self.menu_window.addAction(u"参数面板")
        self.action_node_panel = self.menu_window.addAction(u"节点面板")
        self.action_user_panel = self.menu_window.addAction(u"用户页")
        self.action_view_panel = self.menu_window.addAction(u"视口")
        self.action_reset_window = self.menu_window.addAction(u"重置窗口")

        self.action_open_file = self.menu_file.addAction(u"打开文件")

        # 设置点击产生对号
        self.action_file_panel.setCheckable(True)
        self.action_file_panel.setChecked(True)
        self.action_node_panel.setCheckable(True)
        self.action_node_panel.setChecked(True)
        self.action_user_panel.setCheckable(True)
        self.action_user_panel.setChecked(True)
        self.action_param_panel.setCheckable(True)
        self.action_param_panel.setChecked(True)
        self.action_view_panel.setCheckable(True)
        self.action_view_panel.setChecked(True)


class MainModel():
    """主窗口数据类"""
    def __init__(self):
        pass

        
class MainController():
    """主窗口连接类"""
    def __init__(self):
       
        self.view = MainView()

        self.model = MainModel()

        self.addWindow()
        self.setPanel()
        self.setActionConnect()
        self.setWindowsConnect()

    def addWindow(self):
        """添加中心窗口"""
        self.centerWindow = Center.CenterWindow()  
        self.view.ui.setCentralWidget(self.centerWindow)
        self.view.ui.setLayout(QVBoxLayout())
        self.view.show()


    #初始创建界面
    def setPanel(self):
        self.setUserPanel()
        self.setTreeView()
        self.setViewPanel()
        self.setParmPanel()
        self.setNodePanel()

    #设置工具栏上的按钮与子窗口连接
    def setActionConnect(self):
        self.view.action_file_panel.triggered.connect(self.setTreeView)
        self.view.action_node_panel.triggered.connect(self.setNodePanel)
        self.view.action_param_panel.triggered.connect(self.setParmPanel)
        self.view.action_user_panel.triggered.connect(self.setUserPanel)
        self.view.action_view_panel.triggered.connect(self.setViewPanel)
        self.view.action_reset_window.triggered.connect(self.resetPanel)
        self.view.action_open_file.triggered.connect(self.openFile)


    # 根据当前窗口是否存在大纲视图，不存在添加大纲视图，存在则删除大纲视图
    def setTreeView(self):
        self.treeView = self.view.ui.findChild(QDockWidget, "TreeView")
     
        if(self.treeView == None):

            self.treeView = FileTree.FileTreeWindow()
            self.view.ui.addDockWidget(Qt.LeftDockWidgetArea, self.treeView)
          

        else:
            self.treeView.close()
            self.view.ui.removeDockWidget(self.treeView)
            del(self.treeView)
            self.view.action_file_panel.setChecked(False)

    # 设置节点编辑面板
    def setNodePanel(self):
        self.nodePanel = self.view.ui.findChild(QDockWidget, "nodePanel") 
        if(self.nodePanel == None):

            self.nodePanel = NodePanel()
            self.view.ui.addDockWidget(Qt.RightDockWidgetArea,self.nodePanel)

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
            self.parmPanel = ParmerPanel()
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
            self.view.ui.addDockWidget(Qt.RightDockWidgetArea,self.nodePanel)

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
        
        self.treeView = self.view.ui.findChild(QDockWidget, "TreeView") 
        if(self.treeView != None):
            self.treeView.close()
            self.view.ui.removeDockWidget(self.treeView)
        self.treeView = FileTree.FileTreeWindow()
        self.view.ui.addDockWidget(Qt.LeftDockWidgetArea,self.treeView)
            
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
        self.parmPanel = ParmerPanel()
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
        dialog = QFileDialog() 
               
        #根据当前所在文件目录，设置默认打开文件格式
        dialog.setNameFilter("全部文件 (*);;图片文件(*.jpg *.png *.jpe g);;模型文件(*.obj)")
        #加载对应的文件
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setViewMode(QFileDialog.Detail)

        if dialog.exec_():
            self.paths = dialog.selectedFiles()

            # 创建标签选择窗口
            self.tagWidget = Tag.TagWidget(self.paths)
            self.tagWidget.show()

            if self.tagWidget.close():
                tags_add = self.tagWidget.getNewtag() # 获取新添加的标签
                self.setNewtag(tags_add)

                
                

    # 设置窗口之间的信号连接
    def setWindowsConnect(self):
        if self.treeView != None: # 设置大纲视图的按钮点击连接到中心窗口资源显示
            self.treeView.load_center_signal.connect(self.centerWindow.addSource)

        if self.viewPanel != None: # 设置中心窗口的按钮点击连接到视图窗口显示
            self.centerWindow.load_view_signal.connect(self.viewPanel.setView)


    def setNewtag(self,tags):
        print(tags)

Col = MainController()


    