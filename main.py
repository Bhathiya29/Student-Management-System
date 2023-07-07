# STUDENT MANAGEMENT SYSTEM APPLICATION
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, \
    QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QPushButton
import sys
from PyQt6.QtGui import QAction
import sqlite3
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')

        # Adding the Menu Bar
        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        search_menu_item = self.menuBar().addMenu('&Search')

        add_student_action = QAction('Add Student', self)  # Adding actions to the menu bar
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction('About', self)
        file_menu_item.addAction(about_action)

        search = QAction('Search', self)
        search.triggered.connect(self.search)
        search_menu_item.addAction(search)

        # Adding the Table Structure
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect('database.db')  # Connecting to the database
        result = connection.execute('SELECT * FROM students')
        self.table.setRowCount(0)  # Loads the data as fresh so no duplications
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

        # self.table

    def insert(self):
        dialog = InsertDialog()  # The pop up window
        dialog.exec()

    def search(self):
        search_dialog = SearchDialog()
        search_dialog.exec()


class InsertDialog(QDialog):  # The Insert Dialog window
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Adding Widgets (Student Name)
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name:')
        layout.addWidget(self.student_name)

        # Adding Widgets (Combo box of courses)
        self.course_name = QComboBox()
        courses = ['Biology', 'Maths', 'Physics', 'Astronomy']
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Adding Widgets (Mobile Number)
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText('Mobile')
        layout.addWidget(self.mobile)

        # Adding the Submit button
        button = QPushButton('Register')
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())  # Retrieving the selected combo value
        mobile = self.mobile.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?,?,?)",
                       (name, course, mobile))
        connection.commit()  # applying the SQL query to the db
        cursor.close()
        connection.close()

        system.load_data()  # The changes will be shown immediately as we load the data inside the same method


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Student')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Adding Widgets (Student Name)
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText('Name:')
        layout.addWidget(self.search_name)

        # Adding the search button
        search_button = QPushButton('Search')
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)

        self.setLayout(layout)

    # Name Search Method
    def search(self):
        name = self.search_name.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        result = cursor.execute('SELECT * FROM students WHERE name =?', (name,))
        rows = list(result)
        items = system.table.findItems(name, Qt.MatchFlag.MatchFixedString)  # Tables have a method called findItems
        for item in items:
            print(item)
            system.table.item(item.row(), 1).setSelected(True)  # item is a method of table

        cursor.close()
        connection.close()


app = QApplication(sys.argv)
system = MainWindow()
system.show()
system.load_data()
sys.exit(app.exec())
