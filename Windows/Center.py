# <-- coding utf-8 -->

from Qt.QtWidgets import QWidget, QVBoxLayout, QPushButton, QRadioButton, QLineEdit, \
    QComboBox, QSlider, QTableWidget, QTableWidgetItem, QHeaderView,QToolButton
    
from Qt.QtCompat import loadUi,setSectionResizeMode
from Qt.QtCore import Signal, QRect, Qt,QPoint
from Qt import QtGui  



# from setting.Setting import Data
import layouitflow
import os,json,re,difflib

import btnWin
reload(btnWin)
reload(layouitflow)
# glonal_type = [".png",".jpg",".jpeg",".obj"]

try:
    from Zeus.settings.Setting import Data
except:
    from settings.Setting import Data


#获取当前文件所在路径
current_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.dirname(current_path)



class CenterWindow(QWidget):
    """中心窗口类"""

    load_view_signal = Signal(str,str,str)
    load_node_signal = Signal(list,list,list)
    # load_node_signal = Signal()

   

    def __init__(self):

        super(CenterWindow,self).__init__()

        self.setObjectName("CenterWindow")
      
        self.fileList = [] # 保存当前选择标签下的文件列表
        self.tag = ""  # 保存当前标签

        self.tableWidget_show = False  # tableWidget窗口是否显示
        
        self.row = 0  # 定位添加标签
        self.column = 0
        
        self.setupUI()

        self.lineEdit = self.ui.findChild(QLineEdit, "lineEdit")
        self.searchBtn = self.ui.findChild(QPushButton, "pushButton")
       
        self.slider =self.ui.findChild(QSlider,"horizontalSlider")
        self.tableWidget = self.ui.findChild(QTableWidget,"tableWidget")
        self.toolButton = self.ui.findChild(QToolButton, "toolButton")
        self.toolButton_delTag = self.ui.findChild(QToolButton,"toolButton_2")

        self.searchBtn.clicked.connect(self.on_searchBtn_click)

        self.slider.setMaximum(200)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(self.changeBtnSize)
        
        self.setTableWidget()
        self.toolButton.clicked.connect(self.showTableWidget)
        self.toolButton_delTag.clicked.connect(self.deleteTag)


        

    # 设置UI界面
    def setupUI(self):

        self.setWindowTitle("浏览窗口")

       
        #加载ui,并设置ui界面
        # loader = QUiLoader()
        self.ui = loadUi(file_path + "\\res\\UI\\CenterWidget.ui")
        self.ui.setParent(self)

        #设置布局
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setContentsMargins(0,0,0,0)


        self.child_widget = self.ui.findChild(QWidget, "widget")
        
        # 设置选择窗口
        self.widget = SelWidget()
        layout = QVBoxLayout()
        layout.setMargin(0)
        self.child_widget.setLayout(layout)
        self.child_widget.layout().addWidget(self.widget)
        self.flowLayout = layouitflow.FlowLayout()
        self.widget.setLayout(self.flowLayout)
        self.widget.setDefaultColor()

    # Todo: 根据标签从数据库读取文件内容
    def addSource(self, tag):
        
        # 清楚当前窗口的文件列表
        self.fileList = []
        self.tag = tag



        #清除原有组件
        for i in range(self.widget.layout().count()): 
            self.widget.layout().itemAt(i).widget().deleteLater()
        
        #加载保存数据到字典
        with open(file_path + r"\res\temp\asset.json") as js:
            asset_dir = json.load(js)
      

        # 添加所有子文件到列表中
        for key in asset_dir.keys():
            if (tag in asset_dir[key]["tags"]):
                
                
                self.addFile(key,asset_dir[key]["type"],asset_dir[key]["name"])

                self.fileList.append(key)




                
               

    
        
    # 添加按钮
    def addFile(self, path, type, name):
        
        myBtnWin = btnWin.btnWin(path,type,name)

        myBtnWin.setMaximumSize(self.slider.value() + 100, self.slider.value() + 100)
        
        myBtnWin.btn_clicked_signal.connect(self.setView)
        
        self.widget.layout().addWidget(myBtnWin)



    # 按钮点击，发送信号到主窗口
    def setView(self, type, name, path):
     
        self.load_view_signal.emit(type,name,path)


    # 搜索按钮按下
    def on_searchBtn_click(self):

        #清除原有组件
        for i in range(self.widget.layout().count()): 
            self.widget.layout().itemAt(i).widget().deleteLater()

        #获取输入
        search_text = self.lineEdit.text()


        # search_word = []
        # for p in search_text.split():
        #     search_word.append(
        #         re.compile(
        #             r".*"  + p + r".*"
        #         )
        #     )

       

        # 获取与输入比较的文件名字
        matches = []
        dir_index = {}  # 用于保存文件名和它的对应索引
        index = 0  # 文件对应的索引值，用于排序
        
        # Todo 加载保存数据到字典
        with open(file_path + r"\res\temp\asset.json") as js:
            asset_dir = json.load(js)

        # 添加所有子文件名称到列表中
        for key in self.fileList:
            name =asset_dir[key]["name"]
            matches.append(name)
            dir_index[name] = index
            index += 1

        # 根据搜索相关性重新排列
        ratio = lambda x, y: difflib.SequenceMatcher(None, x, y).ratio()
        matches = sorted(matches, key=lambda x: ratio(x, search_text), reverse=True)

        # 按照排列重新添加资源
        for name in matches:
            key = self.fileList[dir_index[name]]
            self.addFile(key,asset_dir[key]["type"],asset_dir[key]["name"])
       





    # 滑动Slider,改变按钮大小
    def changeBtnSize(self):
       
        btnList = self.widget.findChildren(btnWin.btnWin)  

        for btn in btnList:
            btn.setMinimumSize(self.slider.value() + 100, self.slider.value() + 100)
            btn.setMaximumSize(self.slider.value() + 100, self.slider.value() + 100)
            
    
    # 设置TableWidget
    def setTableWidget(self):
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(10)
        setSectionResizeMode(self.tableWidget.horizontalHeader(),QHeaderView.Stretch) # 自适应
        setSectionResizeMode(self.tableWidget.verticalHeader(),QHeaderView.Stretch)
        self.tableWidget.setMaximumHeight(0)
        self.tableWidget.cellClicked.connect(self.setCenter)
        # self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers) # 设置只读
        
        

        # todo 从数据库读取标签加载到TableWidget
        #加载标签数据到字典
        with open(file_path + r"\res\temp\setting.json") as js:
            setting_json = json.load(js)
        # 根据标签添加按钮
        for tag in setting_json["Tags"]:
            self.setTag(tag)

        
    # 获取标签之后设置中心窗口资源
    def setCenter(self, row, column):
        try: #只能打开已经设置标签的，否则报错
            self.addSource(self.tableWidget.item(row, column).text())
        except:
            return
        
    # 设置标签
    def setTag(self,tag):
        newItem = QTableWidgetItem(tag)
        newItem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(self.row, self.column, newItem)
        if (self.column == 9 and self.row == 9):
            return
        elif (self.column == 9):
            self.row += 1
            self.column = 0
        else:
            self.column += 1



    # 设置tableWidget的显示与隐藏
    def showTableWidget(self):
        if (self.tableWidget_show == False):
            self.tableWidget.setMaximumHeight(Data.getWindowHeight()/4)
            self.tableWidget_show = True
        else:
            self.tableWidget.setMaximumHeight(0)
            self.tableWidget_show = False
    
    # 删除标签
    def deleteTag(self):
        print(self.tag)
        with open(file_path + r"\res\temp\setting.json") as js:
            setting_json = json.load(js)

        try:
            setting_json["Tags"].remove(self.tag)
        except:
            return

        self.tableWidget.clearContents()
        
        self.row, self.column = 0,0
        # 根据标签添加按钮
        for tag in setting_json["Tags"]:
            
            self.setTag(tag)

        #写入标签数据到json文件中
        with open(file_path + r"\res\temp\setting.json", 'w') as json_file:
            json.dump(setting_json, json_file, indent=4)

      
        
        #加载资产数据到字典
        with open(file_path + r"\res\temp\asset.json") as js:
            asset_json = json.load(js)

        
        #遍历打开的文件路径，加载到json中
        for path in asset_json.keys():
            if self.tag in asset_json[path]["tags"]:
                asset_json[path]["tags"].remove(self.tag)

        for path in asset_json.keys():
            if asset_json[path]["tags"] == []:

                del asset_json[path]


        #写入标签数据到json文件中
        with open(file_path + r"\res\temp\asset.json", 'w') as json_file:
            json.dump(asset_json, json_file, indent=4)

        

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
        self.setDefaultColor()

        self.fileList = [] # 用于存储选择的文件路径
 
    def setDefaultColor(self):
        for btn in self.findChildren(btnWin.btnWin):
            btn.setStyleSheet("QToolButton{border: 1.5px solid black;}")

            self.fileList = []
    
    def paintEvent(self, event):
        try:
            self.width = self.pos2[0]-self.pos1[0]
            self.height = self.pos2[1] - self.pos1[1]     
            qp = QtGui.QPainter()
            qp.begin(self)         
            qp.fillRect(self.pos1[0], self.pos1[1], self.width, self.height, QtGui.QColor(10, 45, 45, 120))           
      
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
            

    def getSelect(self, x1, y1, x2, y2):

        if(self.selectMore == False):
            for btn in self.findChildren(btnWin.btnWin):
                btn.setStyleSheet("QToolButton{border: 1.5px solid black;}")
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
                btn.setStyleSheet("QToolButton{border: 1.5px solid black;}")
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
        
           
        return self.fileList


   