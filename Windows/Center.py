# <-- coding utf-8 -->

from PySide.QtGui import QWidget, QVBoxLayout, QPushButton, QRadioButton, QLineEdit, \
    QComboBox, QSlider, QTableWidget, QTableWidgetItem, QHeaderView, QToolButton,QHBoxLayout
from PySide.QtCore import Signal, QRect, QPoint
from PySide import QtGui
from PySide import QtCore
from Qt.QtCompat import loadUi,setSectionResizeMode

import layouitflow
import btnWin
from settings.Setting import Data
import User

import os,json,re,difflib
import pymongo
import time
import functools

from dayu_widgets.loading import MLoadingWrapper
from dayu_widgets.item_view import MTableView
from dayu_widgets.item_model import MTableModel,MSortFilterModel
from dayu_widgets.drawer import MDrawer
from dayu_widgets.qt import QFormLayout
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets import dayu_theme
from dayu_widgets.slider import MSlider
from dayu_widgets.qt import Qt,QThread
from dayu_widgets.tool_button import MToolButton
from dayu_widgets.push_button import MPushButton
from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets.loading import MLoading
from dayu_widgets.message import MMessage
#获取当前文件所在路径
current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.dirname(current_path)

#链接数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")
tagdb = client["tagdb"]  #标签数据库
tagcol = tagdb["tagcol"]  #标签集合
#链接用户数据库
userdb = client["userdb"]
#链接标签文件数据库
tagfiledb = client["tagFiledb"]  #标签文件数据库
alldocdb = client["alldocdb"]  #文件类型总库
alldoccol = alldocdb["alldoccol"]  #文件类型集合

class CenterWindow(QWidget):
    """中心窗口类"""
    load_view_signal = Signal(str, str, str)  #加载参数面板的信号
    
    def __init__(self):
        super(CenterWindow,self).__init__()
        self.setObjectName("CenterWindow")
      
        self.fileList = []       # 保存当前选择标签下的文件列表
        self.tag = ""  # 保存当前标签
        
        self.tableWidget_show = True  # tableWidget窗口是否显示
        self.row = 0  # 定位添加标签
        self.column = 0
       
        self.setupUI()

        # 设置tablewidget
        self.tableWidget = self.ui.findChild(QTableWidget, "tableWidget")
        
        self.tableWidget.setMaximumHeight(Data.getWindowHeight()/5)
        self.setTableWidget()
        self.tableWidget.setStyleSheet(Data.getQSS())
        self.tableWidget.setStyleSheet("background-color: #323232")

        self.searchWidget = self.ui.findChild(QWidget, "widget_2")
        self.search_engine_line_edit = MLineEdit().search_engine().large()
        dayu_theme.apply(self.search_engine_line_edit)
        self.searchWidget.setLayout(QHBoxLayout())
        self.searchWidget.layout().addWidget(self.search_engine_line_edit)

        self.slider = MSlider(Qt.Horizontal)
        self.slider.setMaximumWidth(Data.getWindowWidth()/4)
        self.slider.setValue(50)
        self.slider.setRange(1, 100)
        dayu_theme.apply(self.slider)
        self.searchWidget.layout().addWidget(self.slider)

       
        self.button_tag = MToolButton().svg('detail_line.svg').icon_only()
        self.button_tag.setEnabled(True)
        self.button_del = MToolButton().svg('trash_line.svg').icon_only()
        self.button_del.setCheckable(True)
        dayu_theme.apply(self.button_del)
        dayu_theme.apply(self.button_tag)

        self.searchWidget.layout().addWidget(self.button_tag)
        self.searchWidget.layout().addWidget(self.button_del)

        self.slider.valueChanged.connect(self.changeBtnSize)
        self.button_tag.clicked.connect(self.showTableWidget)
        self.button_del.clicked.connect(self.deleteTag)
        self.search_engine_line_edit.returnPressed.connect(self.on_searchBtn_click)
        self.setThread()
      
        
    # 设置UI界面
    def setupUI(self):

        self.setWindowTitle("浏览窗口")
     
        self.ui = loadUi(file_path + "\\res\\UI\\CenterWidget.ui")
        self.ui.setParent(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setContentsMargins(0,0,0,0)


        self.child_widget = self.ui.findChild(QWidget, "widget")
       
        # 设置选择窗口
        self.widget = SelWidget()
        layout = QVBoxLayout()
        self.child_widget.setLayout(layout)
     
        self.child_widget.layout().addWidget(self.widget)
        self.flowLayout = layouitflow.FlowLayout()
        self.widget.setLayout(self.flowLayout)  #瀑布流布局
        self.widget.layout().setSpacing(0)  #设置间距
     

    # 设置TableWidget
    def setTableWidget(self):
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(10)
        # QHeaderView.setSectionResizeMode(self.tableWidget.horizontalHeader(),QHeaderView.Stretch) # 自适应
        # QHeaderView.setSectionResizeMode(self.tableWidget.verticalHeader(),QHeaderView.Stretch)
        setSectionResizeMode(self.tableWidget.horizontalHeader(),QHeaderView.Stretch) # 自适应
        setSectionResizeMode(self.tableWidget.verticalHeader(),QHeaderView.Stretch)

        self.tableWidget.cellClicked.connect(self.setCenter)
      
        
        #从标签数据库加载数据
        colTag = tagdb["tagcol"]
        try:
            for x in colTag.find({}, {"Tag": 1}):
                tag = x["Tag"]
                self.setTag(tag)
        except:
            pass
    

    # 获取标签之后设置中心窗口资源
    def setCenter(self, row, column):
        try: #只能打开已经设置标签的
            self.addSource(self.tableWidget.item(row, column).text())
        except:
            return
        
    #  根据标签从数据库读取文件内容
    def addSource(self, tag):

        # 清除当前窗口的文件列表
        self.fileList = []
        self.tag = tag

        #清除原有组件
        for i in range(self.widget.layout().count()): 
            self.widget.layout().itemAt(i).widget().deleteLater()
        
       

        collist = tagfiledb.list_collection_names()  # 标签文件数据库里集合名列表
        for tagx in collist:
           
            if tag == tagx:
                tagfilecolx = tagfiledb[tag]
                filenamelistx = tagfilecolx.find({}, {"FileName":1})
                for x in filenamelistx:
                   
                    filename = x["FileName"]
                    filetype = filename.split(".")[-1]
                    assetdb = client[filetype]
                    collist = assetdb.list_collection_names()  # 资产数据库里集合名列表
                    
                    for file in collist:  # 取出资产数据库里单个列表名，即为文件名
                        assetPathlist = assetdb[file].find({"_id": "Path"}, {"Path": 1})
                        pathdic = assetPathlist[0]
                        path = pathdic["Path"]
                        if(path.split("/")[-1] == filename):
                           

                            self.addFile(path, filetype, file)
                            self.fileList.append(path)
                            break

    # 添加按钮
    def addFile(self, path, type, name):

        myBtnWin = btnWin.btnWin(path,type,name)
        value = (float(self.slider.value()) + 50) / 100
        width = height = value * Data.getWindowWidth() / 8

        myBtnWin.setMinimumSize(width, height)
        myBtnWin.setMaximumSize(width, height)

        myBtnWin.btn_clicked_signal.connect(self.setView)
        self.widget.layout().addWidget(myBtnWin)

    # 设置标签
    def setTag(self, tag):
       
        if(tag.isspace()==False and tag !=""):
            newItem = QTableWidgetItem(tag)
            newItem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(self.row, self.column, newItem)
            if (self.column == 9 and self.row == 5):
                return
            elif (self.column == 9):
                self.row += 1
                self.column = 0
            else:
                self.column += 1
    # 添加标签
    def addTag(self, tag):
        tags = []
        for row in range(0, 4):
            for column in range(0, 9):
                try:
                    tags.append(self.tableWidget.item(row, column).text())
                except:
                    continue
      
        if(tag.isspace()==False and tag not in tags and tag !=""):
            newItem = QTableWidgetItem(tag)
            newItem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(self.row, self.column, newItem)
            if (self.column == 9 and self.row == 5):
                return
            elif (self.column == 9):
                self.row += 1
                self.column = 0
            else:
                self.column += 1
   

    # 滑动Slider,改变按钮大小
    def changeBtnSize(self):
       
        btnList = self.widget.findChildren(btnWin.btnWin)
        value = (float(self.slider.value()) + 50) / 100
        width = height = value * Data.getWindowWidth() / 8

        for btn in btnList:
            btn.setMinimumSize(width, height)
            btn.setMaximumSize(width, height)

    
    # 设置tableWidget的显示与隐藏
    def showTableWidget(self):
        if (self.tableWidget_show == False):
            self.tableWidget.setMaximumHeight(Data.getWindowHeight() / 5)
            
            self.tableWidget_show = True
        else:
            self.tableWidget.setMaximumHeight(0)
            self.tableWidget_show = False
        
    # 搜索按钮按下
    def on_searchBtn_click(self):
        self.search_engine_line_edit.returnPressed.disconnect(self.on_searchBtn_click)
        #清除原有组件
        for i in range(self.widget.layout().count()): 
            self.widget.layout().itemAt(i).widget().deleteLater()

        import time
        time.sleep(2)

        self.thread.start()
        
    
    # 重新根据搜索加载按钮
    def endthread(self):
        #获取输入
        search_text = self.search_engine_line_edit.text()

        # 获取与输入比较的文件名字
        matches = []
        dir_index = {}  # 用于保存文件名和它的对应索引
        index = 0  # 文件对应的索引值，用于排序
        file_asset = []
        typelist = alldoccol.find({}, {"Type":1})
        for alltype in typelist:    #读取文件类型库里文件类型名
            typename = alltype["Type"]

            assetdb = client[typename]  #获得文件类型名对应的资产数据库
            collist = assetdb.list_collection_names()   #资产数据库里集合名列表
            for file in collist:  #取出资产数据库里单个列表名，即为文件名
                assetcol = assetdb[file]
                filePathList = assetcol.find({"_id": "Path"}, {"Path": 1})
                for filePathTup in filePathList:
                    if "Path" in filePathTup:
                        filePath = filePathTup["Path"]
                        file_asset.append(filePath)
       
        for file in self.fileList:
            name = file.split("/")[-1]
            matches.append(name)
            dir_index[name] = index
            index += 1

       
        # 根据搜索相关性重新排列
        ratio = lambda x, y: difflib.SequenceMatcher(None, x, y).ratio()
        matches = sorted(matches, key=lambda x: ratio(x, search_text), reverse=True)

        # 按照排列重新添加资源
        for name in matches:
         
            key = self.fileList[dir_index[name]]
            filename = os.path.basename(key)
            type = filename.split(".")[-1]
            self.addFile(key, type, filename)
         
        self.search_engine_line_edit.returnPressed.connect(self.on_searchBtn_click)

    #设置一个新的线程来显示加载动画
    def setThread(self): #防止多次调用线程

        self.thread = MFetchDataThread(self)
        self.thread.started.connect(self.addCircle)
        self.thread.finished.connect(self.removeCircle)
        self.thread.finished.connect(self.endthread)

    def addCircle(self):
       
       
        try:
            self.win = QWidget()
                
            self.win.setMinimumSize(self.child_widget.width()/1.05,self.child_widget.height()/1.1)

            self.loading_wrapper = MLoading.huge()

            self.win.setLayout(QHBoxLayout())
            self.win.layout().addWidget(self.loading_wrapper)

            self.widget.layout().addWidget(self.win)
        except:
            pass
    
    def removeCircle(self):
        try:
            self.win.deleteLater()
            import time
            time.sleep(2)
        except:
            pass

    def deleteTag(self):

        username = User.UserPanel.CorrectUserName
        userID = None


        if username == None:
            self.slot_show_message(MMessage.error, (u'请先登陆！'))
            return 0
        else:
            usercol = userdb[username]

            userIDlist = usercol.find({"_id": "UserID"}, {"UserID": 1})
            for userIDDic in userIDlist:
                if "UserID" in userIDDic:
                    userID = userIDDic["UserID"]
                else:
                    userID = None

            if userID == u"管理员":
                delDic = {"Tag":self.tag}
                tagcol.delete_one(delDic)   #删除标签库里的该标签

                tagfilecol = tagfiledb[self.tag]

                RTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

                filenamelist = tagfilecol.find({}, {"FileName":1})
                for filenameDic in filenamelist:
                    if "FileName" in filenameDic:
                        filename = filenameDic["FileName"]
                        type = filename.split(".")[-1]

                        assetdb = client[type]
                        assetcol = assetdb[filename]
                        assetcol.delete_one(delDic)  #删除所有含有该标签的文件里的该标签。
                        dict = {"Time": RTime, "Operation": u"删除标签", "UserName": username}  #保存删除记录到资产数据库

                        assettaglist = assetcol.find({}, {"Tag": 1})
                        taglist = []
                        for x in assettaglist:
                            if "Tag" in x:
                                taglist.append(x)
                        if len(taglist) == 0:
                            assetcol.drop()


                tagfilecol.drop()   #删除标签文件库里的该标签集合

                dict = {"Time": RTime, "Operation": u"删除标签", "FileName": self.tag}
                usercol.insert_one(dict)    #保存删除记录到用户数据库



                self.slot_show_message(MMessage.error, (u'删除成功'))
                self.resetTableWidget()





            else:
                self.slot_show_message(MMessage.error, (u'只有管理员才可以删除标签'))

    # 弹出信息提示窗口
    def slot_show_message(self, func, config):
        func(config, parent=self)



    # 按钮点击，发送信号到主窗口
    def setView(self, type, name, path):
        
        self.load_view_signal.emit(type,name,path)
    
    def resetTableWidget(self):
        tagdb = client["tagdb"]  # 标签数据库
        tagcol = tagdb["tagcol"]  # 标签集合
        taglist = tagcol.find({}, {"Tag": 1})
        tags = []
        for tagdic in taglist:
            if "Tag" in tagdic:
                tags.append(tagdic["Tag"])

        # 重新设置标签
        self.tableWidget.clearContents()
        self.row, self.column = 0, 0
        # 根据标签添加按钮
        for tag in tags:
            
            self.setTag(tag)
  
       

class MFetchDataThread(QThread):
    def __init__(self, parent=None):
        super(MFetchDataThread, self).__init__(parent)

    def run(self, *args, **kwargs):
        import time
        time.sleep(2)
        
     
    
  
            
    
   
   
        
  







class SelWidget(QWidget):
    """子中心窗口，用于处理鼠标事件"""

    def __init__(self):
        super(SelWidget,self).__init__()
        
        self.pos1 = [None,None]
        self.pos2 = [None, None]
        self.width = 0
        self.height = 0
        self.selectMore = False 
        self.selectLess = False
       

        self.fileList = [] # 用于存储选择的文件路径
 
 
    
    def paintEvent(self, event):
        try:
            self.width = self.pos2[0]-self.pos1[0]
            self.height = self.pos2[1] - self.pos1[1]     
            qp = QtGui.QPainter()
            
            qp.begin(self)
            #绘制选框
            qp.fillRect(self.pos1[0], self.pos1[1], self.width, self.height, QtGui.QColor(30, 56, 100, 120))           
      
            qp.end()
            
        except:
            pass
        
    
    def mouseMoveEvent(self, event):
        if(self.pos1[0] != None):
            self.pos2[0], self.pos2[1] = event.pos().x(), event.pos().y()
          
            self.update()

    def mousePressEvent(self, event):

        self.pos1[0], self.pos1[1] = event.pos().x(), event.pos().y()


    def mouseReleaseEvent(self, event):
        if(self.pos1[0]!= None and self.pos2[0]!= None):
            self.getSelect(self.pos1[0], self.pos1[1], self.pos2[0], self.pos2[1])
            self.pos1[0],self.pos1[1] = None,None
            self.pos2[0], self.pos2[1] = None,None

            self.update()
            
    # 获取选择的按钮，高亮显示
    def getSelect(self, x1, y1, x2, y2):

        if(self.selectMore == False):
            for btn in self.findChildren(btnWin.btnWin):
                btn.setStyleSheet("QToolButton{}")
                self.fileList = []

        if (x1 > x2): x1, x2 = x2, x1
        if (y1 > y2): y1, y2 = y2, y1
        
        rect = QRect(x1, y1, x2-x1, y2-y1)

        for btn in self.findChildren(btnWin.btnWin):
            if(self.IsInRect(btn,rect) and self.selectLess == False):
                btn.setStyleSheet("QToolButton{border: 1.5px solid orange;}")
                if (btn.path not in self.fileList):
                    self.fileList.append(btn.path)
                
            elif (self.IsInRect(btn, rect) and self.selectLess == True):
                btn.setStyleSheet("QToolButton{}")
                if (btn.path in self.fileList):
                    self.fileList.remove(btn.path)
              
                                                    
    # 判断一个控件是否在矩形里面
    def IsInRect(self, btn, rect):
        topLeft = QPoint(btn.x(), btn.y())
        bottomLeft = QPoint(btn.x(), btn.y() + btn.height())
        topRight = QPoint(btn.x() + btn.width(), btn.y())
        bottomRight = QPoint(btn.x() + btn.width(), btn.y() + btn.height())
        if (self.PointInRect(topLeft, rect) or self.PointInRect(bottomLeft, rect) or \
              self.PointInRect(topRight, rect) or self.PointInRect(bottomRight, rect)):
              return True

    # 判断一个点是否在矩形里面
    def PointInRect(self, point, rect):
        if point.x() > rect.topLeft().x() and point.x() < rect.bottomRight().x() and \
            point.y() > rect.topLeft().y() and point.y() < rect.bottomRight().y():
            return True

        else:
            return False


    def setKey(self, key, bool):
        if (key == "shift"):
            if (bool):
                self.selectMore = True
            else:
                self.selectMore = False

        elif (key == "ctrl"):
            if (bool):
                self.selectLess = True
            else:
                self.selectLess = False

    # 获取选择文件
    def getFile(self):
        if self.fileList == []:
            return False
        return self.fileList


   

