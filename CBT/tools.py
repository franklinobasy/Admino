from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

def loadImage(image_path):
    try:
        with open(image_path):
            image = QLabel()
            pixmap = QPixmap(image_path)
            image.setPixmap(pixmap.scaled(200,200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
            return image
    except FileNotFoundError:
            print('image not found')
            return None


def loadStylesheet(file_path):
    with open(file_path) as obj:
        style_sheet = obj.read()
    return style_sheet
