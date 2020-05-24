from PySide.QtGui import QPixmap
from PySide.QtCore import Signal
import os
import functools

from dayu_widgets.badge import MBadge
from dayu_widgets.label import MLabel
from dayu_widgets.menu_tab_widget import MMenuTabWidget
from dayu_widgets.message import MMessage
from dayu_widgets.qt import QWidget, QVBoxLayout,QHBoxLayout
from dayu_widgets.tool_button import MToolButton


#获取当前文件所在路径
current_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.dirname(current_path)

class MenuTabWidgetExample(QWidget):

    file_signal = Signal()
    user_signal = Signal()
    edit_signal = Signal()
    about_siganl = Signal()
    def __init__(self, parent=None):
        super(MenuTabWidgetExample, self).__init__(parent)
        self.setWindowTitle('工具栏')
        self._init_ui()

    def _init_ui(self):
        # 工具
        item_list = [
            {'text': u'文件', 'svg': 'folder_line.svg',
             'clicked': self.openFile},
            {'text': u'编辑', 'svg': 'edit_line.svg',
             'clicked': self.editFile},
            {'text': u'关于', 'svg': 'warning_line.svg',
             'clicked': self.showAbout},
        ]
        tool_bar = MMenuTabWidget()
        tool_bar.tool_bar_insert_widget(MLabel('Zeus').h4().secondary().strong())
        self.user_toolButton = MToolButton().large()
        pixmap = QPixmap(file_path + "\\res\\headPortrial\\user_default.png")
        self.user_toolButton.setIcon(pixmap)
        tool_bar.tool_bar_append_widget(
            MBadge.dot(show=False, widget=self.user_toolButton))
        self.label = MLabel(u"未登录")
        tool_bar.tool_bar_append_widget(
            MBadge.dot(show=False, widget=self.label))
      
        for index, data_dict in enumerate(item_list):
            tool_bar.add_menu(data_dict, index)

        main_lay = QHBoxLayout()
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.addWidget(tool_bar)

        self.setLayout(main_lay)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.user_toolButton.clicked.connect(self.setUser)

    # 点击用户按钮，发射用户信息信号
    def setUser(self):
        self.user_signal.emit()
    
    #打开文件信号
    def openFile(self):
        self.file_signal.emit()

    
    #编辑信号
    def editFile(self):
        self.edit_signal.emit()

    # 关于信号
    def showAbout(self):
        self.about_siganl.emit()
