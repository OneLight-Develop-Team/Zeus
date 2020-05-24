import os
import sys
def addModulePath(MODULE):
    MODULE = os.path.realpath(MODULE)
    if MODULE not in sys.path:
        # sys.path.append(MODULE)
        sys.path.insert(0,MODULE)


addModulePath(os.path.join(__file__,"..","_vendor"))
# addModulePath(os.path.join(__file__,"..","_vendor","dayu_widgets"))
# addModulePath(os.path.join(__file__,"..","_vendor","dayu_path"))
# addModulePath(os.path.join(__file__,"..","_vendor","CefWidget"))

import time
import uuid
import json
import shutil
import signal
import ctypes
import socket
import platform
import subprocess
from functools import wraps

import CefWidget
import pymongo
import cv2
from PIL import Image

from PySide.QtSvg import QSvgRenderer
from PySide.QtGui import QApplication,QSplashScreen,QLabel
from PySide.QtGui import QPixmap, QImage
from PySide.QtCore import QSize,Qt
from PySide import QtUiTools
from PySide import QtXml
from PySide import QtCore
from PySide import QtGui
from PySide import QtSvg
from PySide import *
from PySide.QtGui import *
from PySide.QtCore import *
import PySide
from Windows import MainWindow

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
