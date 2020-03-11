# using utf-8

from PySide2.QtWidgets import QWidget, QDockWidget,QPushButton,QHBoxLayout
from PySide2.QtCore import Qt
from settings.Setting import Data
class NodePanel(QDockWidget):
    """节点视图"""
    def __init__(self):
        super(NodePanel, self).__init__()

        self.setObjectName("nodePanel")

        self.setupUI()

      
    # 设置UI界面
    def setupUI(self):
        # self.setStyleSheet("background-color:rgb(25,222,255)")
        self.setFloating(False)

        self.widget = QWidget()
        self.widget.setMinimumSize(Data.getWindowWidth()/4,Data.getWindowHeight()/4)

        self.setWidget(self.widget)
        self.setWindowTitle("节点编辑器")
