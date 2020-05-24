from PIL import Image
import os
from settings.Setting import Data

from PySide.QtGui import QIntValidator
from dayu_widgets.divider import MDivider
from dayu_widgets.label import MLabel
from dayu_widgets.line_tab_widget import MLineTabWidget
from dayu_widgets.qt import QWidget, QVBoxLayout, Qt,QHBoxLayout
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.browser import MClickBrowserFolderToolButton
from dayu_widgets.push_button import MPushButton
from dayu_widgets import dayu_theme

from PySide.QtCore import Signal
class EditWidget(QWidget):
    send_message_signal = Signal(str,str)
    def __init__(self, paths,parent=None):
        super(EditWidget, self).__init__(parent)
        self.setWindowTitle(u'资产编辑器')
        self.paths = paths
        self.isLoadPic = True   #导出的是图片
        self._init_ui()
        self.setConnect()

    def _init_ui(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.setMinimumSize(Data.getWindowWidth()/4.5,Data.getWindowHeight()/1.6)
        self.setMaximumSize(Data.getWindowWidth()/4.5,Data.getWindowHeight()/1.6)



        browser_4 = MClickBrowserFolderToolButton().huge()
        self.lineEdit  = MLineEdit(text='filepath')
        self.lineEdit.setReadOnly(True)
       
      
        browser_4.sig_folder_changed.connect(self.lineEdit.setText)
        lay_1 = QHBoxLayout()
        lay_1.addWidget(self.lineEdit)
        lay_1.addWidget(browser_4)

        self.tab = MLineTabWidget()
        widget = QWidget()
        widget.setLayout(QVBoxLayout())

             
        self.lineEdit_width  = MLineEdit()
        tool_button = MLabel(text=u'宽度').mark().secondary()
        tool_button.setAlignment(Qt.AlignCenter)
        tool_button.setFixedWidth(80)
        self.lineEdit_width.set_prefix_widget(tool_button)
        self.lineEdit_width.setText("1080")
        self.lineEdit_width.setValidator(QIntValidator())

        self.lineEdit_height  = MLineEdit()
        tool_button = MLabel(text=u'高度').mark().secondary()
        tool_button.setAlignment(Qt.AlignCenter)
        tool_button.setFixedWidth(80)
        self.lineEdit_height.set_prefix_widget(tool_button)
        self.lineEdit_height.setText("720")
        self.lineEdit_height.setValidator(QIntValidator())

        self.lineEdit_level  = MLineEdit()
        tool_button = MLabel(text=u'精度').mark().secondary()
        tool_button.setAlignment(Qt.AlignCenter)
        tool_button.setFixedWidth(80)
        self.lineEdit_level.set_prefix_widget(tool_button)
        self.lineEdit_level.setText("50")
        self.lineEdit_level.setValidator(QIntValidator())

        widget.layout().addWidget(MLabel(u'贴图大小'))
        widget.layout().addWidget(self.lineEdit_width)
        widget.layout().addWidget(self.lineEdit_height)
        widget.layout().addSpacing(10)
        widget.layout().addWidget(MLabel(u'贴图精度'))
        widget.layout().addWidget(self.lineEdit_level)

      
        self.tab.add_tab(widget, u'低精度图片')
   



       
        widget2 = QWidget()
        widget2.setLayout(QVBoxLayout())
        self.MlineEdit_level  = MLineEdit()
        tool_button = MLabel(text=u'精度').mark().secondary()
        tool_button.setAlignment(Qt.AlignCenter)
        tool_button.setFixedWidth(80)
        self.MlineEdit_level.set_prefix_widget(tool_button)
        self.MlineEdit_level.setText("50")
        self.MlineEdit_level.setValidator(QIntValidator())
        widget2.layout().addWidget(MLabel(u'模型精度'))
        widget2.layout().addWidget(self.MlineEdit_level)

        widget2.layout().addSpacing(100)
        self.tab.add_tab(widget2, u'低精度模型')

        btn_layout = QHBoxLayout()
        self.btn_ok = MPushButton(text=u'导出').primary()
        self.btn_ok.setFixedWidth(80)
       
        self.btn_cancel = MPushButton(text=u'取消').primary()
        self.btn_cancel.setFixedWidth(80)

        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)

        main_lay = QVBoxLayout()
        main_lay.addSpacing(20)
        main_lay.addWidget(MDivider(u'路径选择'))
        main_lay.addLayout(lay_1)
        main_lay.addWidget(MDivider(u'操作选择'))
        main_lay.addWidget(self.tab)
       
        main_lay.addWidget(MDivider(u''))
        main_lay.addLayout(btn_layout)
        main_lay.addSpacing(20)
       
        self.setLayout(main_lay)
        dayu_theme.background_color = "#262626"
        dayu_theme.apply(self)

    def setConnect(self):
        self.btn_ok.clicked.connect(self.on_btn_ok_click)
        self.btn_cancel.clicked.connect(self.on_btn_cancel_click)
        self.tab.tool_button_group.sig_checked_changed.connect(self.on_tab_change)
    
    def on_btn_ok_click(self):
        if (self.paths == []):
            self.send_message_signal.emit("warnning", u"请选择操作资产")
            self.close
            return
        
        if (self.lineEdit.text()) == "filepath":
            self.send_message_signal.emit("warnning", u"请选择导出的位置")
            return
        
        output = self.lineEdit.text()
        if self.isLoadPic == True:
            width = int(self.lineEdit_width.text())
            height = int(self.lineEdit_height.text())
            level = int(self.lineEdit_level.text())
            for path in self.paths:
                for name in os.listdir(path):
                    if name.split(".")[-1] == "jpg":

                        picpath = path + "/"+ name
                        self.make_thumb(picpath,output,width,height,level)
                   
            self.send_message_signal.emit("success", u"图片生成成功")
        
       
    
        else:
 
            level = int(self.MlineEdit_level.text())
            for path in self.paths:
                for name in os.listdir(path):
                    if name.split(".")[-1] == "obj" or name.split(".")[-1] == "fbx" :

                        modelpath = path + "/"+ name
                        self.genteralLOD(modelpath,output,level)
                   
          
        self.close()




    def on_btn_cancel_click(self):
        
        self.close()

    def on_tab_change(self):
        if self.isLoadPic == True:
            self.isLoadPic = False
        else:
            self.isLoadPic = True
        


    def make_thumb(self, path, output, size1 = 1080 ,size2 = 720 ,level=50):
        """
        缩略图生成程序
        size 参数传递要生成的尺寸
        返回缩略图地址
        """    

     
        try:  # 尝试打开文件

            im = Image.open(path)
  
        except IOError:
            return

        mode = im.mode
        if mode not in ('L', 'RGB'):
            if mode == 'RGBA':
                # 透明图片需要加白色底
                alpha = im.split()[3]
                bgmask = alpha.point(lambda x: 255-x)
                im = im.convert('RGB')
            
                im.paste((255,255,255), None, bgmask)
            else:
                im = im.convert('RGB')
                
        width, height = im.size
        if width == height:
            region = im
        else:
            if width > height:
                delta = (width - height)/2
                box = (delta, 0, delta+height, height)
            else:
                delta = (height - width)/2
                box = (0, delta, width, delta+width)            
            region = im.crop(box)


        filename = (path.split("/"))[-1]

        savePath = output + "//"+os.path.splitext(filename)[0] + "_thumb.jpg"
        # savePath = file_path + r"\res\images\thumbnail"  + "_" + "%sx%s" % (str(size), str(size)) + ".jpg"
        thumb = region.resize((size1, size2), Image.ANTIALIAS)
        if(level<0):
            level = 0
        elif(level>100):
            level = 100
        thumb.save(savePath, quality=level)  # 默认 JPEG 保存质量是 75, 可选值(0~100)
        
    # 生成低精度模型
    def genteralLOD(self, input, output, level=50):
        try:
            import hou
            name = (input.split("/"))[-1]
        
            name = (name.split("."))[0]
        
            output = output + "//" + name + "_" + str(level) + ".obj"
            
        
            obj = hou.node("obj")
            geo = obj.createNode("geo")
            fileImport = geo.createNode("file")
            fileImport.parm("file").set(input)
            
            polyreduce = geo.createNode("polyreduce")    
            polyreduce.setFirstInput(fileImport)
            polyreduce.parm("percentage").set(level)
            
            fileExport = geo.createNode("file")
            fileExport.setFirstInput(polyreduce)
            fileExport.parm("filemode").set(2)
            fileExport.parm("file").set(output)
            fileExport.setDisplayFlag(1)
            fileExport.parm("reload").pressButton()
            self.send_message_signal.emit("success", u"模型生成成功")

        except:
            self.send_message_signal.emit("warnning", u"该功能仅在houdini内部可以调用")
            