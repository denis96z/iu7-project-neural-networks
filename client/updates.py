import json
import requests

from tqdm import tqdm
from settings import MODEL_FILE_PATH, CONFIG_FILE_PATH


def update(config):
    try:
        r = requests.get('http://{0}{1}'.format(config['server'], config['server-model-path']))
        if r.status_code != 200:
            raise ConnectionError
        config['model'] = r.json()
        r = requests.get('http://{0}{1}'.format(config['server'], config['model']['file']), stream=True)
        if r.status_code != 200:
            raise ConnectionError
        with open(MODEL_FILE_PATH, "wb") as handle:
            for data in tqdm(r.iter_content()):
                handle.write(data)
        with open(CONFIG_FILE_PATH, 'w') as f:
            json.dump(config, f)
    except:
        print('Не удалось загрузить данные с сервера')
    return config