from Windows import MainWindow
from Qt.QtWidgets import QApplication,QSplashScreen
from Qt.QtGui import QPixmap, QImage
from Qt.QtCore import QSize,Qt
import sys
import time
import os
from settings.Setting import Data
filePath =  os.path.dirname(os.path.abspath(__file__))



def runAnimation():
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


if  __name__ == "__main__":
    app = QApplication(sys.argv)
    Col = MainWindow.MainController()

    # runAnimation()
    
    Col.view.showMaximized()
    
    app.exec_()
