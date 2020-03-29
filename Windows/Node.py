# using utf-8

from Qt.QtWidgets import QWidget, QDockWidget,QPushButton,QHBoxLayout
from Qt.QtCore import Qt
from Zeus.NodeConnect import NodeGraphQt
reload(NodeGraphQt)

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
      
        self.setFloating(False)

        self.nodeWidget = NodeGraphQt.BackWidget()
       
        self.nodeWidget.setMinimumSize(Data.getWindowWidth()/4,Data.getWindowHeight()/4)

        self.setWidget(self.nodeWidget)
        self.setWindowTitle(u"节点编辑器")



    def getCenterSource(self):
        return self.parent().parent().centerWindow.fileList