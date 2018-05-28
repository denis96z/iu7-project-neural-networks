from PyQt5 import QtWidgets, uic


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        uic.loadUi('mainwindow.ui', self)
