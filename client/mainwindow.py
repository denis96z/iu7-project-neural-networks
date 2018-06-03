from PIL import Image
from PyQt5 import QtWidgets, QtGui, uic

from settings import IMAGE_WIDTH, IMAGE_HEIGHT


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, config=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        uic.loadUi('mainwindow.ui', self)
        self.image = None
        self.config = config
        self.miExit.triggered.connect(QtWidgets.qApp.quit)
        self.miOpen.triggered.connect(self.open_file)
        self.btnLoadImage.clicked.connect(self.open_file)

    def open_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Выбор изображения ГРЗ',
                                                     filter='Файл изображения (*.png)')
        if not file:
            return
        filename = file[0]
        self.image = Image.open(filename).resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        self.tbImagePath.setText(filename)
        img = QtGui.QPixmap(filename).scaledToWidth(self.gvImage.width())
        scene = QtWidgets.QGraphicsScene()
        scene.addItem(QtWidgets.QGraphicsPixmapItem(img))
        self.gvImage.setScene(scene)
