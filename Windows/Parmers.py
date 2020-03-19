# using utf-8

from Qt.QtWidgets import QWidget, QDockWidget
from Qt.QtCore import Qt

try:
    from Zeus.settings.Setting import Data
except:
    from settings.Setting import Data
class ParmerPanel(QDockWidget):
    """参数面板类"""
    def __init__(self):
        super(ParmerPanel, self).__init__()

        self.setObjectName("parmPanel")
        # self.setFeatures(Qt.DockWidgetVerticalTitleBar)
        self.setupUI()
        # self.show()

    # 设置UI界面
    def setupUI(self):
        # self.setStyleSheet("background-color:rgb(205,2,255)")
        self.setFloating(False)

        self.widget = QWidget()
        self.widget.setMinimumSize(Data.getWindowWidth()/4,Data.getWindowHeight()/4)
        self.setWidget(self.widget)

        self.setWindowTitle(u"参数面板")
