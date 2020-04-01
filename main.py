from Windows import MainWindow
from Qt.QtWidgets import QApplication
import sys
reload(MainWindow)

if  __name__ == "__main__":
    app = QApplication(sys.argv)
    Col = MainWindow.MainController()
    app.exec_()