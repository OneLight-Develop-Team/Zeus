# using utf-8

from PySide2.QtWidgets import QWidget, QDockWidget
from PySide2.QtCore import Qt
from settings.Setting import Data
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
        self.widget.setMinimumSize(Data.getWindowWidth() / 6, Data.getWindowHeight() / 8)
        self.widget.setMaximumHeight(Data.getWindowHeight()/8)
        self.setWidget(self.widget)

        self.setWindowTitle("用户界面")
