
from dayu_widgets.card import MCard, MMeta
from dayu_widgets.label import MLabel
from dayu_widgets.divider import MDivider
from dayu_widgets.flow_layout import MFlowLayout
from dayu_widgets.qt import QWidget, QApplication, MPixmap, QHBoxLayout,QVBoxLayout, Qt
from dayu_widgets import dayu_theme
from dayu_widgets.push_button import MPushButton
from dayu_widgets import dayu_theme
class AboutWidget(QWidget):
    def __init__(self, parent=None):
        super(AboutWidget, self).__init__(parent)
        self.setMaximumSize(440, 455)
        self.setMinimumSize(440,455)
        self._init_ui()

    def _init_ui(self):

        self.setWindowModality(Qt.ApplicationModal)
        meta_card_lay = QHBoxLayout()
        meta_card_lay.setSpacing(20)
        for setting in [
           {
                'title': u'ZEUS',
                'cover': MPixmap(r'C:\Users\huangPeiXin\Documents\houdini17.5\python2.7libs\Zeus_Lin\res\ZeusDesign\zeus.png')
            },
            {
                'title': u'IDO',
                'cover': MPixmap(r'C:\Users\huangPeiXin\Documents\houdini17.5\python2.7libs\Zeus_Lin\res\ZeusDesign\ido.png')
            },
        ]:
            meta_card = MMeta()
            meta_card.setup_data(setting)
            meta_card_lay.addWidget(meta_card)


        left_lay = QVBoxLayout()
     
        left_lay.addWidget(MDivider('About Zeus'))
        left_lay.addLayout(meta_card_lay)
        left_lay.addWidget(MDivider(''))
        left_lay.setSpacing(20)
        label_1 = MLabel(u"Zues是由一灯工作室开发的一个软件")
        label_1.setAlignment(Qt.AlignHCenter)
        label_2 = MLabel(u"用于管理CG开发的相关资源")
        label_2.setAlignment(Qt.AlignHCenter)
        left_lay.addWidget(label_1)
        left_lay.addWidget(label_2)
        btn = MPushButton(u"确定")
        btn.clicked.connect(self.close)
        left_lay.addWidget(btn)
        left_lay.addStretch()
        
        self.setLayout(left_lay)



        dayu_theme.background_color = "#262626"

        dayu_theme.apply(self)