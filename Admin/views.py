id# -*- coding:utf-8 -*-
from .properties import *
from .database import *

from PyQt5.QtCore import (
    Qt,
    QTimer,
    QRect,
)

from PyQt5.QtGui import (
    QFont,
    QPixmap,
)

from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget
)

class Window(QMainWindow):
    '''
    This is the main window of the admin application.
    It is the parent of every other widget in the application
    '''
    def __init__(self, parent= None):
        '''
        This is the constructor of the main window class
        it initialises the window size, title, central widegt, main window's
        layout and calls the login widget(name of the method that displays loginwidget is "self.displayLogin")

        NB: This constructor also calls the splash screen window
        '''
        super().__init__(parent)
        self.setObjectName('WindowColor')
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(WINDOW_WIDTH + 50, WINDOW_HEIGHT + 50)
        self.setWindowTitle('ADMINO')

        splash_screen = SplashScreen(self)    # Splash screen object, using the SplashScreen class
        QTimer().singleShot(4000, self.show)  # timer to display mainwindow after splash screen goes off

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.displayLogin()   # Display login section

    def displayLogin(self):
        '''
        This method displays login interface
        '''
        self.login_layer = AdminLogin(self)  # login interface object created using AdminLogin class
        self.login_layer.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_layer, alignment= Qt.AlignCenter)
        
    def login(self):
        '''
        This method performs login validation
        '''
        conn = sql_connection()                            # imported from database module, creates connection with 'admin.db' file
        userid = self.login_layer.userid_entry.text()
        password = self.login_layer.password_entry.text()
        if fetchUser(conn, userid, password):              #imported from database module, checks if userid and password is value, returns True if test passes
            QMessageBox.information(self, 'Success', 'Login Validated', QMessageBox.Ok)
            self.interaction_window = InteractionWindow(self)  # after, login validation, the interaction window is created from InteractionWindow class
            self.layout.itemAt(0).widget().deleteLater()       # deletes login interface from main window's layout
            self.layout.addWidget(self.interaction_window)     # adds the newly created interaction window to main window's layout
        else:
            QMessageBox.information(self, 'Login Error', 'Incorrect userid or password', QMessageBox.Ok)
    
    def logout(self):
        '''
        This method logs user out of the interaction window
        '''
        answer = QMessageBox.question(self, 'Log Out', 'Are you sure you want to log out?',
                                        QMessageBox.Yes | QMessageBox.Cancel)
        
        if answer == QMessageBox.Yes:
            self.layout.itemAt(0).widget().deleteLater()   #deletes the interaction window out from the manin window's layout
            self.displayLogin()                            #displays login interface again
            self.login_layer.userid_entry.setText('')
            self.login_layer.password_entry.setText('')
        else:
            pass
        

class SplashScreen(QWidget):
    '''
    This is the spalsh screen window that appears when app is launched
    '''
    def __init__(self, parent= None):
        super().__init__(parent)
        self.setObjectName('WindowColor')

        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)

        self.resize(250, 100)
        self.setMinimumSize(400, 200)
        pixmap = QPixmap('Admin/images/admino.png')
        pixmap_label = QLabel()
        pixmap_label.setPixmap(pixmap.scaled(150, 75, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        layout = QVBoxLayout()
        layout.addWidget(pixmap_label, alignment= Qt.AlignCenter)

        self.setLayout(layout)
        self.show()
        QTimer().singleShot(4000, self.destroy)  #Destroys the window after 4seconds using QTimer
        

class AdminLogin(QGroupBox):
    '''
    This class provides the structure of the login widgets
    '''
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setMaximumSize(GROUPBOX_WIDTH, GROUPBOX_HEIGHT)
        self.setMinimumSize(GROUPBOX_WIDTH, GROUPBOX_HEIGHT)
        self.setupWidgets()

    def setupWidgets(self):
        '''
        This methods creates every other widget with the login section
        '''
        def view_password(state):
            '''This function hides/shows characters on the password text widget'''
            if state == Qt.Checked:
                self.password_entry.setEchoMode(QLineEdit.Normal)
            else:
                self.password_entry.setEchoMode(QLineEdit.Password)
        title = QLabel()
        title.setText("LOGIN")
        title.setFont(QFont(L_FONT, 20))
        title.setStyleSheet('color: white')

        self.userid_entry = QLineEdit(self)
        self.userid_entry.resize(QLINEDIT_WIDTH,QLINEDIT_HEIGHT)
        self.userid_entry.setPlaceholderText('Username')
        self.userid_entry.setObjectName('login')
        self.userid_entry.setAlignment(Qt.AlignCenter)

        self.password_entry = QLineEdit(self)
        self.password_entry.resize(QLINEDIT_WIDTH,QLINEDIT_HEIGHT)
        self.password_entry.setPlaceholderText('Password')
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setObjectName('login')
        self.password_entry.setAlignment(Qt.AlignCenter)

        self.password_cb = QCheckBox(self)
        self.password_cb.setText('Show Password')
        self.password_cb.stateChanged.connect(view_password)

        self.login_button = QPushButton('Login')    # Login button

        layout = QVBoxLayout()
        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(self.userid_entry)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.password_cb)
        layout.addStretch(1)
        layout.addWidget(self.login_button , alignment=Qt.AlignCenter)

        self.setLayout(layout)
        

class InteractionWindow(QWidget):
    '''This provides the interaction interface of admino'''
    def __init__(self, parent= None):
        super().__init__(parent)
        self.parent = parent
        conn = sql_connection()
        create_SubjectsTable(conn)
        self.setObjectName('WindowColor')
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setupWidgets()

    def setupWidgets(self):
        '''This method sets up main widgets on the interaction window'''
        layout = QVBoxLayout()
        pixmap = QPixmap('Admin/images/programmer.png')
        pixmap_label = QLabel()
        pixmap_label.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        log_out_button = QPushButton('Log-Out')           # Logout button
        log_out_button.clicked.connect(self.parent.logout)
        
        layout.addStretch()
        layout.addWidget(pixmap_label, alignment=Qt.AlignLeft)
        layout.addWidget(log_out_button, alignment=Qt.AlignLeft)
        layout.addStretch()

        #Tabs
        tab_widget = QTabWidget()
        tab_widget.setObjectName('TabWidget')

        self.subject_widget = QWidget()                # Subject Tab, to add subjects
        self.subject_widget.setObjectName('TabWidget')
        self.q_o_widegt = QWidget()                    # Question and Options Tab, to add questions, options, answers, etc
        self.q_o_widegt.setObjectName('TabWidget')
        self.property_widget = QWidget()               # set rules tab
        self.property_widget.setObjectName('TabWidget')

        tab_widget.addTab(self.subject_widget, 'SUBJECTS')
        tab_widget.addTab(self.q_o_widegt, 'Add Questions And Others')
        tab_widget.addTab(self.property_widget, 'Set Rules')


        self.layout.addLayout(layout, 0, 0)
        self.layout.addWidget(tab_widget, 0, 1)

        self.setUp_subject_widget()
    
    def setUp_subject_widget(self):
        '''This method setsup all widgets within the SUBJECTS tab'''
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 10, 30, 25)

        inner_layout = QHBoxLayout()
        inner_layout.setContentsMargins(5, 5, 30, 10)

        buttons_layout = QVBoxLayout()
        buttons_layout.setContentsMargins(10, 10, 10, 10)

        top_text = QLabel('Add Examination Subjects Here:')
        top_text.setFont(QFont('Arial', 15))
        top_text.setObjectName('TopText')

        self.subject_list = CustomQListWidget(self)             # QListWidget that displays a list of subjects
        self.subject_list.setObjectName('SubjectList')
        self.subject_list.setGeometry(0, 0, 250, 50)
        self.subject_list.setDragEnabled(True)

        #For Question and Option Tab
        self.subject_list_1 = None

        # Load already existing subjects into the QlistWidget that displays a list of subjects
        conn = sql_connection()            #create a connection the app's database 'admino.db'
        subjects = load_subjects(conn)     #imported from database module, it loads existing subject names from the subjects table in admino.db  
        if subjects:
            for subject in subjects:
                list_item = QListWidgetItem()
                list_item.setText(subject)
                self.subject_list.addItem(list_item)
        else:
            pass
        #self.subject_list.setAcceptDrops(True)

        add_subject = QPushButton('+ Add Subject')
        add_subject.clicked.connect(self.addSubject)

        del_subject = QPushButton('- Delete')
        del_subject.clicked.connect(self.delSubject)

        clr_subject = QPushButton('x Clear')
        clr_subject.clicked.connect(self.clrAllSubject)
        clr_subject.setEnabled(False)

        load_button = QPushButton('Load Subjects')
        load_button.clicked.connect(self.loadSubjects)
        

        buttons_layout.addWidget(add_subject)
        buttons_layout.addWidget(del_subject)
        buttons_layout.addWidget(clr_subject)
        buttons_layout.addWidget(load_button)

        inner_layout.addWidget(self.subject_list, alignment= Qt.AlignLeft)
        inner_layout.addStretch()
        inner_layout.addLayout(buttons_layout)

        layout.addWidget(top_text, alignment= Qt.AlignLeft)
        layout.addLayout(inner_layout, stretch= 10)

        self.subject_widget.setLayout(layout)

    def setUp_QO_widget(self):
        self.filename = ''
        def getImageFilepath():
            file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "JPEG Files(*.jpeg);;PNG Files(*.png)")
            if file_name:
                self.filename = file_name
                pixmap = QPixmap(self.filename)
                self.image_label.setText('')
                self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
                self.image_text.setText(self.filename)
            else:
                self.filename = ''


        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 5, 10, 25)

        lower_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 5, 10, 25)

        layout = QVBoxLayout()
        top_layout.setContentsMargins(10, 15, 10, 25)
        image_layout = QVBoxLayout()

        self.select_subject = CustomQComboBox(self)
        self.select_subject.setCurrentText('No subject Selected')
        self.select_subject.setToolTip('choose subject')
        self.display_selected_subject = QLabel('No subject selected')
        view_contextual_table = QPushButton('See Subject all Contents')
        view_contextual_table.setToolTip('View database')

        input_database_label = QLabel('Input External database:')
        input_database_button = QPushButton('Enter')
        input_database_button.setToolTip('input external database')

        self.question_no = QLineEdit()
        self.question_no.setPlaceholderText('Question Number')
        self.question = QTextEdit()
        self.question.setMaximumWidth(350)
        self.question.setMinimumWidth(350)
        self.question.resize(400, 400)

        self.image_button = QPushButton('image')
        self.image_button.setToolTip('attach image to the question')
        self.image_text = QLineEdit('image link')
        self.image_text.setDisabled(True)
        self.image_label = QLabel('  No image')
        self.image_label.setObjectName('QuestionImage')
        self.image_label.resize(100, 100)
        self.image_label.setMaximumSize(150, 150)
        self.image_label.setMinimumSize(150, 150)
        self.image_button.clicked.connect(getImageFilepath)
        

        self.optionA = QLineEdit()
        self.optionA.setPlaceholderText('Option A')
        self.optionB = QLineEdit()
        self.optionB.setPlaceholderText('Option B')
        self.optionC = QLineEdit()
        self.optionC.setPlaceholderText('Option C')
        self.optionD = QLineEdit()
        self.optionD.setPlaceholderText('Option D')
        self.answer = QComboBox()
        self.answer.addItems(['A', 'B', 'C', 'D'])

        self.commit_button = QPushButton('commit')
        self.commit_button.clicked.connect(self.insertData)

        top_layout.addWidget(self.select_subject, alignment=Qt.AlignLeft)
        top_layout.addWidget(self.display_selected_subject, alignment=Qt.AlignLeft)
        top_layout.addStretch(10)
        top_layout.addWidget(view_contextual_table, alignment=Qt.AlignLeft)
        top_layout.addWidget(input_database_label, alignment=Qt.AlignRight)
        top_layout.addWidget(input_database_button, alignment=Qt.AlignRight)

        image_layout.addWidget(self.image_text)
        image_layout.addWidget(self.image_button)
        image_layout.addWidget(self.image_label)
        image_layout.addStretch(5)

        lower_layout.addWidget(self.question_no, alignment=Qt.AlignLeft)
        lower_layout.addWidget(self.question, alignment=Qt.AlignLeft)
        lower_layout.addLayout(image_layout)
        lower_layout.addWidget(self.optionA, alignment=Qt.AlignLeft)
        lower_layout.addWidget(self.optionB, alignment=Qt.AlignLeft)
        lower_layout.addWidget(self.optionC, alignment=Qt.AlignLeft)
        lower_layout.addWidget(self.optionD, alignment=Qt.AlignLeft)
        lower_layout.addWidget(self.answer, alignment=Qt.AlignLeft)

        input_section = QGroupBox()
        input_section.setLayout(lower_layout)

        layout.addLayout(top_layout)
        layout.addWidget(input_section)
        layout.addWidget(self.commit_button, alignment= Qt.AlignRight)

        self.q_o_widegt.setLayout(layout)
    
    def setUp_properties_widget(self):
        pass
        
    def addSubject(self):
        '''This method adds a subject to the subject_lists'''
        user_input, ok = QInputDialog.getText(self, 'Input', 'Enter Subject Here',flags= Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        if ok:
            list_item = QListWidgetItem()
            list_item.setText(user_input)
            self.subject_list.addItem(list_item)
            conn = sql_connection()
            AddToSubjectsTable(conn, user_input)
    
    def delSubject(self):
        '''This method removes a subject from the Subject lists'''
        row = self.subject_list.currentRow()
        row = row + 1
        if row:
            subject = self.subject_list.currentItem().text()
            answer = QMessageBox.question(self, 'Delete', f'Are You Sure you want to delete "{subject}"\t Data will be lost', QMessageBox.Yes, QMessageBox.Cancel)
            if answer == QMessageBox.Yes:
                self.subject_list.takeItem(row - 1)
                conn = sql_connection()
                RemoveSubjectsTable(conn, subject)
        else:
            QMessageBox.information(self, 'Error', 'No Subject Selected, Select subject that you want to delete')
    
    def clrAllSubject(self):
        '''clears all subject in the subject_list'''
        answer = QMessageBox.question(self, 'Clear all', f'Are You Sure you want to clear all? \t All data will be lost', QMessageBox.Yes, QMessageBox.Cancel)
        if answer == QMessageBox.Yes:
            self.subject_list.clear()

    def loadSubjects(self):
        '''This method creates table for all subjects in the subject list'''
        
        n = self.subject_list.count()
        if not (n <= 0):
            subjectTables = []
            for i in range(n):
                subject = self.subject_list.item(i).text()
                subjectTables.append(subject)
            
            for subject in subjectTables:
                conn = sql_connection()
                create_CustomTable(conn, subject)
            
            QMessageBox.information(self, 'Success', 'Subjects loaded successfully')
            self.setUp_QO_widget()
            self.select_subject.addItems(subjectTables)
        else:
            QMessageBox.information(self, 'Error', 'Subjects list is empty\nPlease, add subject(s)')

    def insertData(self):
        table_name = self.select_subject.currentText()
        question_no = int(self.question_no.text())
        question = self.question.toPlainText()
        image = convertToBinaryData(self.filename)
        optionA = self.optionA.text()
        optionB = self.optionB.text()
        optionC = self.optionC.text()
        optionD = self.optionD.text()
        answer = self.answer.currentText()

        conn = sql_connection()
        insertDataToTable(conn, table_name, 
            question_no,
            question,
            image,
            optionA,
            optionB,
            optionC,
            optionD,
            answer
        )
        QMessageBox.information(self, 'SUCCESS',f'Question added to {table_name} successfully', QMessageBox.Ok)


class CustomQListWidget(QListWidget):
    def __init__(self, parent= None):
        super().__init__(parent)
        self.parent = parent
        

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.parent.delSubject()
        elif event.key() == Qt.Key_D:
            self.parent.delSubject()


class CustomQComboBox(QComboBox):
    def __init__(self, parent= None):
        super().__init__(parent)

        self.parent = parent
        self.currentIndexChanged.connect(self._currentTextChanged)
    
    def _currentTextChanged(self):
        display = self.currentText() + ' subject selected'
        self.parent.display_selected_subject.setText(display)