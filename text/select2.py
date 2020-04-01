# -*- coding: utf-8 -*-

import sys
MODULE = r"."
if MODULE not in sys.path:
    sys.path.append(MODULE)

from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QPainter, QBrush, QColor
from Windows import layouitflow
from functools import partial

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30,30,600,400)
        self.pos1 = [None,None]
        self.pos2 = [None, None]
        self.width = 0
        self.height = 0
        self.setLayout(layouitflow.FlowLayout())
        self.layout().setSpacing(20)
        self.setStyleSheet("QPushButton{background-color:white}")
        self.selectMore = False 
        self.selectLess = False
        for i in range(100):
            btn = QtWidgets.QPushButton(str(i))
            
            self.layout().addWidget(btn)
        self.show()
        


    def paintEvent(self, event):
        try:
            self.width = self.pos2[0]-self.pos1[0]
            self.height = self.pos2[1] - self.pos1[1]     
            qp = QPainter()
            qp.begin(self)         
            qp.fillRect(self.pos1[0], self.pos1[1], self.width, self.height, QColor(50, 200, 200, 120))           
                
            qp.end()

        except:
            pass
        
    
    def mouseMoveEvent(self, event):
        if(self.pos1[0] != None):
            self.pos2[0], self.pos2[1] = event.pos().x(), event.pos().y()
        
            self.update()

    def mousePressEvent(self, event):
        self.pos1[0], self.pos1[1] = event.pos().x(), event.pos().y()


    def mouseReleaseEvent(self, event):
        if(self.pos1[0]!= None and self.pos2[0]!= None):
            self.getSelect(self.pos1[0], self.pos1[1], self.pos2[0], self.pos2[1])
            self.pos1[0],self.pos1[1] = None,None
            self.pos2[0], self.pos2[1] = None,None

            self.update()
        
    def keyPressEvent(self, event):
        if (event.key() == QtCore.Qt.Key_Shift):
            self.selectMore = True
        if (event.key() == QtCore.Qt.Key_Control):
            self.selectLess = True

    def keyReleaseEvent(self, event):
        if (event.key() == QtCore.Qt.Key_Shift):
            self.selectMore = False
        if (event.key() == QtCore.Qt.Key_Control):
            self.selectLess = False


    def getSelect(self, x1, y1, x2, y2):
        
        if(self.selectMore == False):
            for btn in self.findChildren(QtWidgets.QPushButton):
                btn.setStyleSheet("QPushButton{background-color:white}")

        if (x1 > x2): x1, x2 = x2, x1
        if (y1 > y2): y1, y2 = y2, y1
        
        rect = QtCore.QRect(x1, y1, x2-x1, y2-y1)



        for btn in self.findChildren(QtWidgets.QPushButton):
            if(self.IsInRect(btn,rect) and self.selectLess == False):

                btn.setStyleSheet("QPushButton{background-color:lightgreen}")
            elif (self.IsInRect(btn, rect) and self.selectLess == True):
                btn.setStyleSheet("QPushButton{background-color:white}")
                                                    
    # 判断一个控件是否在矩形里面
    def IsInRect(self, btn, rect):
        topLeft = QtCore.QPoint(btn.x(), btn.y())
        bottomLeft = QtCore.QPoint(btn.x(), btn.y() + btn.height())
        topRight = QtCore.QPoint(btn.x() + btn.width(), btn.y())
        bottomRight = QtCore.QPoint(btn.x() + btn.width(), btn.y() + btn.height())
        if (self.PointInRect(topLeft, rect) or self.PointInRect(bottomLeft, rect) or \
              self.PointInRect(topRight, rect) or self.PointInRect(bottomRight, rect)):
              return True
      
        else:
            return False

                            
    # 判断一个点是否在矩形里面
    def PointInRect(self, point, rect):
        if point.x() > rect.topLeft().x() and point.x() < rect.bottomRight().x() and \
            point.y() > rect.topLeft().y() and point.y() < rect.bottomRight().y():
            return True

        else:
            return False




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
  

    # app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())


