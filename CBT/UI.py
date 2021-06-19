from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QDesktopWidget, \
    QLineEdit, QCheckBox, QGroupBox, QMessageBox, QGridLayout, QTextEdit)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

from CBT.properties import *

class WelcomeLayer(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setObjectName('main')

    def load(self):
        #text on screen
        title = QLabel()
        title.setText(WINDOW_TITLE)
        title.setFont(QFont(L_FONT, 40))
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName('main')

        self.button = QPushButton('Continue >>')
        self.button.setFont(QFont(B_FONT, 12))
        self.button.resize(12,4)
        self.button.setObjectName('welcome')

        footer = QLabel()
        footer.setText(FOOTER_TEXT)
        footer.setFont(QFont(L_FONT, 8,))
        footer.setAlignment(Qt.AlignCenter)
        footer.setObjectName('footer')

        self.layout.setSpacing(30)
        #add widgets to home widget layout
        self.layout.addStretch(6)
        self.layout.addStretch(8)
        self.layout.addWidget(title)
        self.layout.addStretch()
        self.layout.addWidget(self.button, alignment= Qt.AlignCenter)
        self.layout.addStretch(8)
        self.layout.addWidget(footer, alignment= Qt.AlignCenter)

class LoginLayer(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setObjectName('main')
        self.setMaximumHeight(300)
        self.setMinimumHeight(300)
        self.setMinimumWidth(500)
        self.setMaximumWidth(500)

    def load(self):
        def view_password(state):
            if state == Qt.Checked:
                self.password_entry.setEchoMode(QLineEdit.Normal)
            else:
                self.password_entry.setEchoMode(QLineEdit.Password)
        title = QLabel()
        title.setText("LOGIN")
        title.setFont(QFont(L_FONT, 20))

        self.username_entry = QLineEdit(self)
        self.username_entry.resize(QLINEDIT_WIDTH,QLINEDIT_HEIGHT)
        self.username_entry.setPlaceholderText('Username')
        self.username_entry.setObjectName('login')
        self.username_entry.setAlignment(Qt.AlignCenter)

        self.password_entry = QLineEdit(self)
        self.password_entry.resize(QLINEDIT_WIDTH,QLINEDIT_HEIGHT)
        self.password_entry.setPlaceholderText('Password')
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setObjectName('login')
        self.password_entry.setAlignment(Qt.AlignCenter)

        self.password_cb = QCheckBox(self)
        self.password_cb.setText('Show Password')
        self.password_cb.stateChanged.connect(view_password)

        self.login_button = QPushButton('Login')
        

        container = QGroupBox()
        container.setObjectName('login')
        container.setMaximumHeight(GROUPBOX_HEIGHT)
        container.setMaximumWidth(GROUPBOX_WIDTH)

        container_layout = QVBoxLayout()
        container_layout.addWidget(title, alignment=Qt.AlignCenter)
        container_layout.addStretch(1)
        container_layout.addWidget(self.username_entry)
        container_layout.addWidget(self.password_entry)
        container_layout.addWidget(self.password_cb)
        container_layout.addStretch(1)
        container_layout.addWidget(self.login_button , alignment=Qt.AlignCenter)

        container.setLayout(container_layout)
        self.layout.addWidget(container)

class InstructionLayer(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setObjectName('main')

    def load(self):
        instruction_lb = QLabel()
        instruction_lb.setText("Instructions")
        instruction_lb.setObjectName('instruction')
        instruction_lb.setFont(QFont(L_FONT, 20))

        instruction = QTextEdit()
        instruction.setObjectName('instruction')
        instruction.setText(INSTRUCTIONS)
        instruction.setFont(QFont('Ariel', 15))
        #instruction.setWordWrap(True)
        instruction.setReadOnly(True)
        instruction.setMaximumSize(720, 350)
        instruction.setMinimumSize(720, 350)

        self.button = QPushButton('Proceed')

        self.layout.addWidget(instruction_lb, alignment= Qt.AlignLeft)
        self.layout.addWidget(instruction, alignment= Qt.AlignCenter)
        self.layout.addWidget(self.button, alignment= Qt.AlignRight)

class PreTestSection(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setObjectName('main')

    def load(self):
        pass