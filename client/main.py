import json
import sys

from PyQt5 import QtWidgets

from mainwindow import MainWindow
from settings import CONFIG_FILE_PATH
from updates import update


def main():
    try:
        config = json.loads(open(CONFIG_FILE_PATH).read())
        if config['model'] is None:
            config = update(config)
    except:
        print('Невозможно загрузить конфигурационный файл')
        return
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow(config=config)
        window.show()
        sys.exit(app.exec_())
    except:
        pass


if __name__ == '__main__':
    main()
