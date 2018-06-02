import json
import shutil
import sys
import requests

from PyQt5 import QtWidgets
from mainwindow import MainWindow

from settings import MODEL_FILENAME, CONFIG_FILENAME


def main():
    try:
        config = json.loads(open(CONFIG_FILENAME).read())
        if config['model'] is None:
            try:
                r = requests.get('http://{0}{1}'.format(config['server'], config['server-model-path']))
                if r.status_code != 200:
                    raise ConnectionError
                config['model'] = r.json()
                r = requests.get('http://{0}{1}'.format(config['server'], config['model']['file']))
                if r.status_code != 200:
                    raise ConnectionError
                with open(MODEL_FILENAME, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                with open(CONFIG_FILENAME, 'w') as f:
                    json.dump(config, f)
            except:
                print('Не удалось загрузить данные с сервера')
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow(config=config)
        window.show()
        sys.exit(app.exec_())
    except:
        print('Невозможно загрузить конфигурационный файл')


if __name__ == '__main__':
    main()
