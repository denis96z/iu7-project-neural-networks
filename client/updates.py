import json
import shutil
import requests

from settings import MODEL_FILENAME, CONFIG_FILENAME


def update(config):
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
    return config