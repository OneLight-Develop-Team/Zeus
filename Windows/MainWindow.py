# <-- coding utf-8 -->

from Qt.QtWidgets import QVBoxLayout, QWidget, QMenu, QMainWindow, QDockWidget, QFileDialog, QFileSystemModel, \
    QPushButton,QSpinBox,QLineEdit,QDoubleSpinBox
from Qt.QtCompat import loadUi
from Qt.QtCore import Qt,Signal

from  functools import partial

import Center
import  User
from Parmers import ParmerPanel
import Node 
import  View
import Tag

try:
    from Zeus.settings.Setting import Data
except:
    from settings.Setting import Data

import os,json

import sys
sys.path.insert(0, r"D:\python2\Lib\site-packages\PIL")
sys.path.insert(1,r"D:\python2\Lib\site-packages\cv2")
from PIL import Image
import cv2


from shutil import copyfile



try:
    import hou
except:
    pass

reload(User)
reload(View)
reload(Center)
reload(Tag)
reload(Node)


#获取当前文件所在路径
current_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.dirname(current_path)




class MainView(QWidget):
    """主窗口视图类"""
    def __init__(self):
        super(MainView, self).__init__()

        self.setupUI()
        self.setControl()

    #设置ui界面
    def setupUI(self):
       
        #加载ui,并设置ui界面
        # loader = QUiLoader()
        self.ui = loadUi(file_path + "\\res\\UI\\MainWindow.ui")
        self.ui.setParent(self)
        
        #设置窗口名称
        self.setWindowTitle(u"资产浏览器")

        #设置布局
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setContentsMargins(0,0,0,0)

        self.resize(Data.getWindowWidth(), Data.getWindowHeight())
        
        self.addWindow()

    #设置控件
    def setControl(self):
        #获取控件
        self.menu_window = self.ui.findChild(QMenu, "menu_window")
        self.menu_file = self.ui.findChild(QMenu, "menu_file")
        self.menu_edit = self.ui.findChild(QMenu,"menu_edit")
        

        self.action_param_panel = self.menu_window.addAction(u"参数面板")
        self.action_node_panel = self.menu_window.addAction(u"节点面板")
        self.action_user_panel = self.menu_window.addAction(u"用户页")
        self.action_view_panel = self.menu_window.addAction(u"视口")
        self.action_reset_window = self.menu_window.addAction(u"重置窗口")

        self.action_open_file = self.menu_file.addAction(u"打开文件")

        self.action_get_LOD = self.menu_edit.addAction(u"生成低精度模型")
        self.action_rename = self.menu_edit.addAction(u"重命名图片")
        self.action_get_thumb = self.menu_edit.addAction(u"生成缩略图")
        self.action_get_video = self.menu_edit.addAction(u"生成视频")

        # 设置点击产生对号
        self.action_node_panel.setCheckable(True)
        self.action_node_panel.setChecked(True)
        self.action_user_panel.setCheckable(True)
        self.action_user_panel.setChecked(True)
        self.action_param_panel.setCheckable(True)
        self.action_param_panel.setChecked(True)
        self.action_view_panel.setCheckable(True)
        self.action_view_panel.setChecked(True)
    
    def addWindow(self):
        """添加中心窗口"""
        self.centerWindow = Center.CenterWindow()  
        self.ui.setCentralWidget(self.centerWindow)
        self.ui.setLayout(QVBoxLayout())
        self.show()

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Shift):
            self.setKeyPress("shift",True)
           
        if (event.key() == Qt.Key_Control):
            self.setKeyPress("ctrl",True)

       

    def keyReleaseEvent(self, event):
        if (event.key() == Qt.Key_Shift):
            self.setKeyPress("shift",False)
        if (event.key() == Qt.Key_Control):
            self.setKeyPress("ctrl", False)
            
    # 传递键盘事件到中心窗口
    def setKeyPress(self, key, bool):
        try:
            self.centerWindow.widget.setKey(key, bool)
       

        except:
            pass

class MainModel():
    """主窗口数据类"""
    def __init__(self):
        pass

    # 生成低精度模型
    def genteralLOD(self, input, output, level=50):
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

    def rename(self, filelist, path,endName= ""):
        
        for file in filelist:
            if file.endswith('.jpg'):
                copyfile(file, path + "/" + (file.split("/"))[-1])

        i = 1
        # imglist = os.listdir(path)
		# filelist = os.listdir(path)
		# total_num = len(filelist)
        imglist = os.listdir(path)

        for item in imglist:
        
			if item.endswith('.jpg'):
                
				src = os.path.join(os.path.abspath(path), item)
               
				dst = os.path.join(os.path.abspath(path), endName + '0000' + format(str(i), '0>3s') + '.jpg')
				os.rename(src, dst)
				# print 'converting %s to %s ...' % (src, dst)
				i = i + 1

   
    def make_thumb(self, path, output, size1 = 500,size2 = 500,level=50):
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

        savePath = output + "//"+os.path.splitext(filename)[0] + ".jpg"
        # savePath = file_path + r"\res\images\thumbnail"  + "_" + "%sx%s" % (str(size), str(size)) + ".jpg"
        thumb = region.resize((size1, size2), Image.ANTIALIAS)
        if(level<0):
            level = 0
        elif(level>100):
            level = 100
        thumb.save(savePath, quality=level)  # 默认 JPEG 保存质量是 75, 可选值(0~100)
        

        return savePath
        
    def makevideo(self, files, path, name, width, high, fps):
        """ 将图片合成视频. path: 视频路径，fps: 帧率 """
        ZeusImagePath = path + "/" + "videoImageTemp"
        if not os.path.exists(ZeusImagePath):     #判断当前路径是否存在，没有则创建new文件夹
            os.makedirs(ZeusImagePath)
        ZeusImageSizePath = path + "/" + "ZeusImageSizePath"
        if not os.path.exists(ZeusImageSizePath):
            os.makedirs(ZeusImageSizePath)

        for file in files:
            if file.endswith('.jpg'):
                copyfile(file, ZeusImagePath + "/" + (file.split("/"))[-1])

        filelist = os.listdir(ZeusImagePath)
        i = 1

        for item in filelist:
            if item.endswith('.jpg'):
                src = os.path.join(os.path.abspath(ZeusImagePath), item)
                dst = os.path.join(os.path.abspath(ZeusImagePath), '0000' + format(str(i), '0>3s') + '.jpg')
                os.rename(src, dst)
                i = i + 1

        filelist = os.listdir(ZeusImagePath)
        i=0
        for item in filelist:
            
            self.make_thumb(ZeusImagePath + "/" + item, ZeusImageSizePath, width, high, 50)
            i = i+1
            
        command = file_path + r"\ffmpeg\bin\ffmpeg.exe -loop 1 -f image2 -i " \
            + ZeusImageSizePath + r"\%007d.jpg -vcodec libx264 -r " + str(fps) + " -t "+str(fps*i)+ " "+ path + "\\" + name \
            + ".mp4"
        print(command)
        os.system(command)

        filelist = os.listdir(ZeusImagePath)
        for item in filelist:
            os.remove(ZeusImagePath + "\\" + item)  # path是文件的路径，如果这个路径是一个文件夹，则会抛出OSError的错误，这时需用用rmdir()来删除
        os.rmdir(ZeusImagePath)  # path是文件夹路径，注意文件夹需要时空的才能被删除

        filelist = os.listdir(ZeusImageSizePath)
        for item in filelist:
            os.remove(ZeusImageSizePath + "\\" + item)  # path是文件的路径，如果这个路径是一个文件夹，则会抛出OSError的错误，这时需用用rmdir()来删除
        os.rmdir(ZeusImageSizePath)  # path是文件夹路径，注意文件夹需要时空的才能被删除

class MainController():
    """主窗口连接类"""
    def __init__(self):
        
        self.view = MainView()

        self.model = MainModel()


        self.setPanel()
        self.setActionConnect()
        self.setWindowsConnect()


    #初始创建界面
    def setPanel(self):
        self.setUserPanel()
        self.setViewPanel()
        self.setParmPanel()
        self.setNodePanel()

    #设置工具栏上的按钮与子窗口连接
    def setActionConnect(self):
        self.view.action_node_panel.triggered.connect(self.setNodePanel)
        self.view.action_param_panel.triggered.connect(self.setParmPanel)
        self.view.action_user_panel.triggered.connect(self.setUserPanel)
        self.view.action_view_panel.triggered.connect(self.setViewPanel)
        self.view.action_reset_window.triggered.connect(self.resetPanel)
        self.view.action_open_file.triggered.connect(self.openFile)


        self.view.action_get_LOD.triggered.connect(self.getLOD)
        self.view.action_rename.triggered.connect(self.renamePic)
        self.view.action_get_thumb.triggered.connect(self.getThumb)
        self.view.action_get_video.triggered.connect(self.getVideo)


    

    
 
    # 设置用户面板
    def setUserPanel(self):
        self.userPanel = self.view.ui.findChild(QDockWidget, "UserPanel") 
        if(self.userPanel == None):
            self.userPanel =User.UserPanel()
            self.view.ui.addDockWidget(Qt.LeftDockWidgetArea,self.userPanel)

        else:
            self.userPanel.close()
            self.view.ui.removeDockWidget(self.userPanel)
            del(self.userPanel)
            self.view.action_user_panel.setChecked(False)
                
    # 设置视口
    def setViewPanel(self):
        self.viewPanel = self.view.ui.findChild(QDockWidget, "ViewPanel")
       
        if(self.viewPanel == None):
            self.viewPanel = View.ViewPanel()
            self.view.ui.addDockWidget(Qt.RightDockWidgetArea,self.viewPanel)

        else:
            self.viewPanel.close()
            self.view.ui.removeDockWidget(self.viewPanel)
            del (self.viewPanel)
            self.view.action_view_panel.setChecked(False)
            
    # 设置参数面板
    def setParmPanel(self):
        self.parmPanel = self.view.ui.findChild(QDockWidget, "parmPanel") 
        if(self.parmPanel == None):
            self.parmPanel = ParmerPanel()
            self.view.ui.addDockWidget(Qt.RightDockWidgetArea,self.parmPanel)

        else:
            self.parmPanel.close()
            self.view.ui.removeDockWidget(self.parmPanel)
            del(self.parmPanel)
            self.view.action_param_panel.setChecked(False)
            
    # 设置节点编辑面板
    def setNodePanel(self):
        self.nodePanel = self.view.ui.findChild(QDockWidget, "nodePanel") 
        if(self.nodePanel == None):

            self.nodePanel = Node.NodePanel()
            self.nodePanel.setParent(self.view)
            self.view.ui.addDockWidget(Qt.LeftDockWidgetArea,self.nodePanel)
           
        else:
            self.nodePanel.close()
            self.view.ui.removeDockWidget(self.nodePanel)
            del (self.nodePanel)
            self.view.action_node_panel.setChecked(False)
            
    #重置窗口布局
    def resetPanel(self):

        self.userPanel = self.view.ui.findChild(QDockWidget, "UserPanel") 
        if(self.userPanel != None):
            self.userPanel.close()
            self.view.ui.removeDockWidget(self.userPanel)
        self.userPanel = User.UserPanel()
        self.view.ui.addDockWidget(Qt.LeftDockWidgetArea, self.userPanel)
        
     
            
        self.viewPanel = self.view.ui.findChild(QDockWidget, "ViewPanel") 
        if(self.viewPanel != None):
            self.viewPanel.close()
            self.view.ui.removeDockWidget(self.viewPanel)
        self.viewPanel =View.ViewPanel()
        self.view.ui.addDockWidget(Qt.RightDockWidgetArea,self.viewPanel)
    

        self.parmPanel = self.view.ui.findChild(QDockWidget, "parmPanel") 
        if(self.parmPanel != None):
            self.parmPanel.close()
            self.view.ui.removeDockWidget(self.parmPanel)
        self.parmPanel = ParmerPanel()
        self.view.ui.addDockWidget(Qt.RightDockWidgetArea,self.parmPanel)
    
        self.nodePanel = self.view.ui.findChild(QDockWidget, "nodePanel") 
        if(self.nodePanel != None):
            self.nodePanel.close()
            self.view.ui.removeDockWidget(self.nodePanel)
        self.nodePanel = Node.NodePanel()
        self.view.ui.addDockWidget(Qt.RightDockWidgetArea,self.nodePanel)
        self.nodePanel.setParent(self.view)


        self.view.action_view_panel.setChecked(True)
        self.view.action_user_panel.setChecked(True)
        self.view.action_node_panel.setChecked(True)
        self.view.action_file_panel.setChecked(True)
        self.view.action_param_panel.setChecked(True)

    #打开文件
    def openFile(self):
        dialog = QFileDialog() 
               
        #根据当前所在文件目录，设置默认打开文件格式
        dialog.setNameFilter("全部文件 (*);;图片文件(*.jpg *.png *.jpe g);;模型文件(*.obj)")
        #加载对应的文件
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setViewMode(QFileDialog.Detail)

        if dialog.exec_():
            self.paths = dialog.selectedFiles()

            # 创建标签选择窗口
            self.tagWidget = Tag.TagWidget(self.paths)
            self.tagWidget.show()
            self.tagWidget.send_tag_signal.connect(self.cenWinAddTags) # 链接添加标签的信号到中心窗口添加标签方法
            
           
    # 中心窗口添加新按钮
    def cenWinAddTags(self, tags):
        
        # 获取新添加的标签
        tags_add = tags.split(",")

        for tag in tags_add:
            
            self.view.centerWindow.setTag(tag)


                
                

    # 设置窗口之间的信号连接
    def setWindowsConnect(self):
        

        if self.viewPanel != None: # 设置中心窗口的按钮点击连接到视图窗口显示
            self.view.centerWindow.load_view_signal.connect(self.viewPanel.setView)

        if self.parmPanel != None:
            self.view.centerWindow.load_view_signal.connect(self.parmPanel.setParm)

        # if self.nodePanel != None:
        #     self.view.centerWindow.load_node_signal.connect(self.nodePanel.setNode)

    # 打开选择低精度模型窗口
    def getLOD(self):

        self.LODpath = ""
        self.LODlevel = 50
        self.lodWidget = LODWidget()
        self.lodWidget.send_path_signal.connect(self.setLODpath)
        self.lodWidget.send_level_signal.connect(self.setLODLevel)
        self.lodWidget.genteral_LOD_signal.connect(self.generalLOD)
        self.lodWidget.show()


    # 生成低精度模型
    def generalLOD(self):
        if self.LODpath == "":
            return
        for file in self.view.centerWindow.widget.getFile():
            
            if(os.path.splitext(file)[-1] == ".obj" ):
                
                self.model.genteralLOD(file, self.LODpath, self.LODlevel)
        # 重置
        self.LODpath = ""
        self.LODlevel = 50

    def setLODpath(self, path):
        
        self.LODpath = path
    
    def setLODLevel(self, level):
        
        self.LODlevel = level

    def renamePic(self):
        self.picPath = ""
        self.endName = ""
        # self.endName = ""
        self.renameWidget = RenameWidget()
        self.renameWidget.show()
        self.renameWidget.send_path_signal.connect(self.setRenamePath)
        self.renameWidget.send_endName_signal.connect(self.setEndName)
        self.renameWidget.genteral_pic_signal.connect(self.rename)
        

            # # 更替数据库里的文件名
            # if file in asset_dir.keys():
            #     dir = asset_dir[file]
            #     del (asset_dir[file])
            #     dir["path"] = file

    def setRenamePath(self,path):
        self.picPath = path

    def setEndName(self,name):
        self.endName = name
    def rename(self):
        if self.picPath != "":
            self.model.rename(self.view.centerWindow.widget.getFile(),self.picPath,self.endName)
        self.picPath = ""
        self.endName = ""
    


    def getThumb(self):
        self.thumbPath = ""
        self.thumbLevel = 50
        self.thumbWidth = 0
        self.thumbHeight = 0
        self.thumbWidget = ThumbWidget()
        self.thumbWidget.send_path_signal.connect(self.setThumbPath)
        self.thumbWidget.send_level_signal.connect(self.setThumbLevel)
        self.thumbWidget.send_size_signal.connect(self.setThunmSize)
        self.thumbWidget.genteral_Thumb_signal.connect(self.genteralThumb)
        self.thumbWidget.show()



    def setThumbPath(self, path):
   
        self.thumbPath = path

    def setThumbLevel(self, level):
    
        self.thumbLevel = level

    def setThunmSize(self,width,height):
     
        self.thumbWidth  = width
        self.thumbHeight = height
    
    def genteralThumb(self):
 
        if self.thumbPath == "":
            return
        for file in self.view.centerWindow.widget.getFile():                
            self.model.make_thumb(file, self.thumbPath, self.thumbWidth,self.thumbHeight,self.thumbLevel)
        # 重置
        self.thumbPath = ""
        self.thumbLevel = 50
        self.thumbWidth = 0
        self.thumbHeight = 0


    def getVideo(self):
        self.video_path = ""
        self.name = ""
        self.video_width = 500
        self.video_high = 500
        self.fps = 1.0
        self.videoWidget = VideoWidget()

        self.videoWidget.send_path_signal.connect(self.setVideoPath)
        self.videoWidget.send_name_signal.connect(self.setVideoName)
        self.videoWidget.send_size_signal.connect(self.setVideoSize)
        self.videoWidget.send_fps_signal.connect(self.setVideoFps)
        self.videoWidget.genteral_video_signal.connect(self.genteralVideo)
        self.videoWidget.show()

    def setVideoPath(self,path):
        self.video_path = path
    
    def setVideoName(self, name):
        self.video_name = name
    def setVideoSize(self, width,height):
        self.video_width = width
        self.video_high = height
    def setVideoFps(self,fps):
        self.fps = fps
    
    def genteralVideo(self):
        if self.video_name != "" and self.video_path != "":
            self.model.makevideo(self.view.centerWindow.widget.getFile(),self.video_path,self.video_name,self.video_width,self.video_high,self.fps)  # 图片转视频
        self.video_name = ""
        self.video_path = ""
        self.video_width = 500
        self.video_high = 500
        self.fps = 1.0
class LODWidget(QWidget):

    send_path_signal = Signal(str)
    send_level_signal = Signal(int)
    genteral_LOD_signal = Signal()
    def __init__(self):
        super(LODWidget, self).__init__()

        self.setWindowModality(Qt.ApplicationModal)

        self.ui = loadUi(file_path + "\\res\\UI\\LOD.ui")
        self.ui.setParent(self)

        
        #设置窗口名称
        self.setWindowTitle(u"LOD选择窗口")

        #设置布局
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setMargin(0)
        self.setMinimumSize(Data.getWindowWidth()/5,Data.getWindowHeight()/6)
        self.setMaximumSize(Data.getWindowWidth()/5,Data.getWindowHeight()/6)

        self.btn = self.ui.findChild(QPushButton,"pushButton")
        self.btn_ok = self.ui.findChild(QPushButton, "pushButton_ok")
        self.btn_cancel = self.ui.findChild(QPushButton,"pushButton_cancel")
        self.spinbox = self.ui.findChild(QSpinBox,"spinBox")
       

        self.lineEdit = self.ui.findChild(QLineEdit,"lineEdit")
        self.btn.clicked.connect(self.setSavePath)
        self.btn_ok.clicked.connect(self.on_btn_ok_click)
        self.btn_cancel.clicked.connect(self.on_btn_cancel_click)


        self.spinbox.setValue(50)

    # 设置保存路径
    def setSavePath(self):
        dialog = QFileDialog() 
        
        
        # self.path = dialog.getOpenFileName(self,'选择文件','')
        self.path = dialog.getExistingDirectory(self,
                                    "选取文件夹",
                                    "C:/")                                 #起始路径
        
        self.lineEdit.setText(self.path)

   


    def on_btn_ok_click(self):
        self.send_path_signal.emit(self.lineEdit.text())
        self.send_level_signal.emit(self.spinbox.value())
        self.genteral_LOD_signal.emit()
        self.close()

    def on_btn_cancel_click(self):
        self.close()




class ThumbWidget(QWidget):
    """缩略图设置窗口"""
    send_path_signal = Signal(str)
    send_level_signal = Signal(int)
    send_size_signal = Signal(int, int)
    genteral_Thumb_signal = Signal()
    def __init__(self):
        super(ThumbWidget, self).__init__()
    
        self.setWindowModality(Qt.ApplicationModal)

        self.ui = loadUi(file_path + "\\res\\UI\\Thumb.ui")
        self.ui.setParent(self)

        
        #设置窗口名称
        self.setWindowTitle(u"Thumb选择窗口")

        #设置布局
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setMargin(0)
        self.setMinimumSize(Data.getWindowWidth()/5,Data.getWindowHeight()/5)
        self.setMaximumSize(Data.getWindowWidth()/5,Data.getWindowHeight()/5)

        self.btn = self.ui.findChild(QPushButton,"pushButton")
        self.btn_ok = self.ui.findChild(QPushButton, "pushButton_2")
        self.btn_cancel = self.ui.findChild(QPushButton,"pushButton_3")
        self.spinbox_width = self.ui.findChild(QSpinBox, "spinBox")
        self.spinbox_height = self.ui.findChild(QSpinBox, "spinBox_2")
        
        self.spinbox_level = self.ui.findChild(QSpinBox,"spinBox_3")
       

        self.lineEdit = self.ui.findChild(QLineEdit,"lineEdit")
        self.btn.clicked.connect(self.setSavePath)
        self.btn_ok.clicked.connect(self.on_btn_ok_click)
        self.btn_cancel.clicked.connect(self.on_btn_cancel_click)


        self.spinbox_width.setValue(500)
        self.spinbox_height.setValue(500)
        self.spinbox_level.setValue(50)

    # 设置保存路径
    def setSavePath(self):
        dialog = QFileDialog() 
        
        
        # self.path = dialog.getOpenFileName(self,'选择文件','')
        self.path = dialog.getExistingDirectory(self,
                                    "选取文件夹",
                                    "C:/")                                 #起始路径
        
        self.lineEdit.setText(self.path)


    def on_btn_ok_click(self):
        self.send_path_signal.emit(self.lineEdit.text())
        self.send_level_signal.emit(self.spinbox_level.value())
        self.send_size_signal.emit(self.spinbox_width.value(),self.spinbox_height.value())
        self.genteral_Thumb_signal.emit()
      
        self.close()

    def on_btn_cancel_click(self):
        self.close()


class RenameWidget(QWidget):
    """重命名窗口"""
    genteral_pic_signal = Signal()
    
    send_path_signal = Signal(str)

    send_endName_signal = Signal(str)

    def __init__(self):
        super(RenameWidget, self).__init__()
        

  
    
        self.setWindowModality(Qt.ApplicationModal)

        self.ui = loadUi(file_path + "\\res\\UI\\Rename.ui")
        self.ui.setParent(self)

        
        #设置窗口名称
        self.setWindowTitle(u"重命名选择窗口")

        #设置布局
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setMargin(0)
        self.setMinimumSize(Data.getWindowWidth()/5,Data.getWindowHeight()/5)
        self.setMaximumSize(Data.getWindowWidth()/5,Data.getWindowHeight()/5)

        self.btn = self.ui.findChild(QPushButton,"pushButton")
        self.btn_ok = self.ui.findChild(QPushButton, "pushButton_2")
        self.btn_cancel = self.ui.findChild(QPushButton, "pushButton_3")
        self.lineEdit = self.ui.findChild(QLineEdit,"lineEdit")
        self.lineEdit_endName = self.ui.findChild(QLineEdit,"lineEdit_2")

        self.btn.clicked.connect(self.setSavePath)
        self.btn_ok.clicked.connect(self.on_btn_ok_click)
        self.btn_cancel.clicked.connect(self.on_btn_cancel_click)

        
            # 设置保存路径
    def setSavePath(self):
        dialog = QFileDialog() 
        
        
        # self.path = dialog.getOpenFileName(self,'选择文件','')
        self.path = dialog.getExistingDirectory(self,
                                    "选取文件夹",
                                    "C:/")                                 #起始路径
        
        self.lineEdit.setText(self.path)


    def on_btn_ok_click(self):
        self.send_path_signal.emit(self.lineEdit.text())
        self.send_endName_signal.emit(self.lineEdit_endName.text())
        self.genteral_pic_signal.emit()
      
        self.close()

    def on_btn_cancel_click(self):
        self.close()




class VideoWidget(QWidget):
    """视频窗口"""
    genteral_video_signal = Signal()
    
    send_path_signal = Signal(str)

    send_name_signal = Signal(str)

    send_fps_signal = Signal(float)
    send_size_signal = Signal(int, int)

    def __init__(self):
        super(VideoWidget, self).__init__()
        

  
    
        self.setWindowModality(Qt.ApplicationModal)

        self.ui = loadUi(file_path + "\\res\\UI\\Video.ui")
        self.ui.setParent(self)

        
        #设置窗口名称
        self.setWindowTitle(u"视频选择窗口")

        #设置布局
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setMargin(0)
        self.setMinimumSize(Data.getWindowWidth()/5,Data.getWindowHeight()/5)
        self.setMaximumSize(Data.getWindowWidth()/5,Data.getWindowHeight()/5)

        self.btn = self.ui.findChild(QPushButton,"pushButton")
        self.btn_ok = self.ui.findChild(QPushButton, "pushButton_2")
        self.btn_cancel = self.ui.findChild(QPushButton, "pushButton_3")
        self.lineEdit = self.ui.findChild(QLineEdit, "lineEdit")
        self.lineEdit_name = self.ui.findChild(QLineEdit, "lineEdit_2")
        self.spinbox_width = self.ui.findChild(QSpinBox, "spinBox")
        self.spinbox_height = self.ui.findChild(QSpinBox, "spinBox_2")
        self.spinbox_fps = self.ui.findChild(QDoubleSpinBox,"doubleSpinBox")

        self.btn.clicked.connect(self.setSavePath)
        self.btn_ok.clicked.connect(self.on_btn_ok_click)
        self.btn_cancel.clicked.connect(self.on_btn_cancel_click)

        
        self.spinbox_width.setValue(500)
        self.spinbox_height.setValue(500)
        self.spinbox_fps.setValue(1.0)
        
            # 设置保存路径
    def setSavePath(self):
        dialog = QFileDialog() 
        
        
        # self.path = dialog.getOpenFileName(self,'选择文件','')
        self.path = dialog.getExistingDirectory(self,
                                    "选取文件夹",
                                    "C:/")                                 #起始路径
        
        self.lineEdit.setText(self.path)


    def on_btn_ok_click(self):
        self.send_path_signal.emit(self.lineEdit.text())
        self.send_name_signal.emit(self.lineEdit_name.text())
        self.send_size_signal.emit(self.spinbox_width.value(),self.spinbox_height.value())
        self.send_fps_signal.emit(self.spinbox_fps.value())  
        self.genteral_video_signal.emit()

        self.close()

    def on_btn_cancel_click(self):
        self.close()