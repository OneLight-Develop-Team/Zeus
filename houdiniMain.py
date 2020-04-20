import os
import sys

MODULE = os.path.join(__file__,"..","_vendor")
print MODULE
if MODULE not in sys.path:
    sys.path.append(MODULE)

# import PySide2
# from PySide2 import QtWidgets
# from Qt import QtWidgets

from Windows import MainWindow

reload(MainWindow)

Col = MainWindow.MainController()

Col.view.showMaximized()


