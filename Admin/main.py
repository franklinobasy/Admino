import sys

from PyQt5.QtWidgets import QApplication
from Admin.views import Window, SplashScreen

with open('Admin/stylesheet.css') as obj:
    stylesheet = obj.read()

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)

    window = Window()

    sys.exit(app.exec())