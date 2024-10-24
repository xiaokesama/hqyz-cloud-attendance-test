from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QLabel
from PyQt6 import uic
import sys

from common import manager


def get_inputs():
    name = ui.lineEdit.text()
    xpath = ui.lineEdit_2.text()
    note = ui.lineEdit_3.text()
    parent = ui.lineEdit_4.text()
    return name, xpath, note, parent


def showResults(results):
    ui.textEdit.setPlainText(results)


def check_ele_exist():
    results = manager.validate_xpath(get_inputs()[0])
    showResults(results)


def save_ele():
    results = manager.save_xpath(*get_inputs())
    showResults(results)


def update_ele():
    results = manager.update_xpath(*get_inputs())
    showResults(results)


def delete_ele():
    pass


def show_all_names():
    results = manager.get_all_names(get_inputs()[0])
    showResults(results)


def main():
    ui.setWindowTitle('Element Location Manager')
    ui.pushButton.clicked.connect(check_ele_exist)
    ui.pushButton_2.clicked.connect(save_ele)
    ui.pushButton_3.clicked.connect(update_ele)
    ui.pushButton_4.clicked.connect(show_all_names)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = uic.loadUi('manager.ui')
    main()
    ui.show()
    sys.exit(app.exec())
