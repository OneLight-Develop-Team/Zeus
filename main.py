import os
import sys
def addModulePath(MODULE):
    MODULE = os.path.realpath(MODULE)
    if MODULE not in sys.path:
        # sys.path.append(MODULE)
        sys.path.insert(0,MODULE)

addModulePath(os.path.join(__file__,"..","_vendor"))
addModulePath(os.path.join(__file__,"..","_vendor","dayu_widgets"))
addModulePath(os.path.join(__file__,"..","_vendor","dayu_path"))
addModulePath(os.path.join(__file__,"..","_vendor","CefWidget"))

import CefWidget

from Windows import MainWindow
from Qt.QtWidgets import QApplication,QSplashScreen,QLabel
from Qt.QtGui import QPixmap, QImage
from Qt.QtCore import QSize,Qt
import time
from settings.Setting import Data
filePath =  os.path.dirname(os.path.abspath(__file__))

def runAnimation():

    Col = MainWindow.MainController()
      # 开机动画
    splash = QSplashScreen()
    scale = 0.5
    mgnWidth = int(Data.getWindowWidth()*scale)
    mgnHeight = int(Data.getWindowHeight() * scale)
    size = QSize(mgnWidth,mgnHeight)
    splash.show()
    for name in os.listdir(filePath + r"\res\ZeusDesign\startup_seq"):
        path = filePath + r"\res\ZeusDesign\startup_seq\\" + name
        image = QImage(path)
        pixmap = QPixmap.fromImage(image.scaled(size,Qt.IgnoreAspectRatio))
        splash.setPixmap(pixmap)
        
        
        time.sleep(0.01)
    splash.finish(Col.view)

@CefWidget.autoInitialize
def main():
    app = QApplication([])
    Col = MainWindow.MainController()
    

    runAnimation()

    Col.view.showMaximized()

    app.exec_()

if  __name__ == "__main__":
    main()
