# using utf-8

from Qt.QtWidgets import QWidget, QDockWidget,QPushButton,QHBoxLayout
from Qt.QtCore import Qt

try:
    from Zeus.settings.Setting import Data
except:
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
        self.setWindowTitle(u"节点编辑器")
