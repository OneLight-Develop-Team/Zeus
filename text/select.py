from PySide2.QtWidgets import QWidget, QApplication
from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter,QColor
import sys

class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()

    def mousePressEvent(self, event):

        if (event.buttons() == Qt.LeftButton):
            self.x1 = event.x()
            self.y1 = event.y()
            print("开始选择")

    def mouseMoveEvent(self, event):
        if (event.buttons() == Qt.LeftButton):
            self.x2 = event.x()
            self.y2 = event.y()
            self.update()
            


    def mouseReleaseEvent(self, event):
        if (event.buttons() == Qt.LeftButton):
            
            print("结束选择")
            self.x2 = event.x()
            self.y2 = event.y()

            self.update()

    def paintEvent(self, event):
        try:
            print("draw")
            painter = QPainter()
 
            painter.setAttributte(Qt.WA_TranslucentBackground, True)
 
            painter.setBrush(QColor(255,0,0,0)) 
 
            painter.drawRect(self.x1,self.y1,self.x2,self.y2)
        except:
            pass

if __name__ == "__main__":
	app = QApplication(sys.argv)
	myWidget = MyWidget()
	myWidget.show()
	app.exec_()