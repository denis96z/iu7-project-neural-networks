import numpy as np

from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array

from settings import IMG_WIDTH, IMG_HEIGHT, MODEL_FILE_PATH


def recognize(config, img_path):
    model = load_model(MODEL_FILE_PATH)

    orig_img = load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH)).convert('L')
    orig_img.show()
    cropped_width, cropped_height = config['model']['img_width'], config['model']['img_height']
    cropped_img = orig_img.crop((0, 0, cropped_width, cropped_height))
    cropped_img.show()
    img_array = np.reshape(img_to_array(cropped_img) / 255, [cropped_width, cropped_height, 1])
    img_array = np.expand_dims(img_array, axis=0)

    print(model.predict_classes(img_array))

    return 'a'