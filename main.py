import sys

from PyQt5.QtWidgets import (QApplication)
from CBT import CBTApp
from CBT.tools import loadStylesheet

filepath = "CBT/data/stylesheet.css"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(loadStylesheet(filepath))
    ui = CBTApp()
    sys.exit(app.exec_())

