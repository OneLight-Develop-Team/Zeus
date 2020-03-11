# <-- coding utf-8 -->


from Windows.MainWindow import MainController
from PySide2.QtWidgets import QApplication
import sys
if __name__ == "__main__":
    app = QApplication(sys.argv)
    col = MainController()

    sys.exit(app.exec_())
    
