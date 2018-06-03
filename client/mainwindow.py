from PyQt5 import QtWidgets, QtGui, uic

from recognition import recognize
from settings import IMG_WIDTH
from updates import update


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, config=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        uic.loadUi('mainwindow.ui', self)
        self.img_path = None
        self.config = config
        self.miExit.triggered.connect(QtWidgets.qApp.quit)
        self.miOpen.triggered.connect(self.open_file)
        self.miUpdate.triggered.connect(self.update)
        self.btnLoadImage.clicked.connect(self.open_file)
        self.btnRecognize.clicked.connect(self.recognize)

    def open_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Выбор изображения ГРЗ',
                                                     filter='Файл изображения (*.png)')
        if not file:
            return
        self.img_path = file[0]
        self.tbImagePath.setText(self.img_path)
        img = QtGui.QPixmap(self.img_path).scaledToWidth(IMG_WIDTH)
        scene = QtWidgets.QGraphicsScene()
        scene.addItem(QtWidgets.QGraphicsPixmapItem(img))
        self.gvImage.setScene(scene)

    def recognize(self):
        if self.img_path is None:
            pass
        r_char = recognize(self.config, self.img_path)
        self.tbRecognitionResult.setText(r_char)

    def update(self):
        self.config = update(self.config)