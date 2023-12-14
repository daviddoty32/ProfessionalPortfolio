import PIL
from tensorflow import keras
import tensorflow as tf

from PIL import Image
import os


def model_create():
    model = keras.Sequential([
        keras.layers.MaxPool2D(),
        keras.layers.Convolution2D(10, 3, activation='relu'),
        keras.layers.Flatten(),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(9, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


def model_fetch(model):
    try:
        model = tf.keras.models.load_model(f'ProfessionalPortfolio/Animal_Classifier_AI/{model}')
        model.summary()
    except FileNotFoundError:
        print('Model not found, check spelling and try again.')
        raise FileNotFoundError


def model_train_animal_classifier(data):
    try:
        model = model_fetch('AnimalClassifier')
    except FileNotFoundError:
        model = model_create()

    model.fit(data, epochs=10, batch_size=20)

    model.save('AnimalClassifier')


def main():
    rootdir = f'C:\\Users\\david\\PycharmProjects\\pythonProject\\ProfessionalPortfolio\\Animal_Classifier_AI\\raw-img'
    for subdir, dirs, files in os.walk(rootdir):
        for directory in dirs:
            print(directory)
            rootdir = f'C:\\Users\\david\\PycharmProjects\\pythonProject\\ProfessionalPortfolio\\Animal_Classifier_AI\\raw-img\\{directory}'
            for subdir, dirs, files in os.walk(rootdir):
                for file in files:
                    try:
                        rootdir = f'C:\\Users\\david\\PycharmProjects\\pythonProject\\ProfessionalPortfolio\\Animal_Classifier_AI\\raw-img\\{directory}'
                        image = Image.open(f'{rootdir}\\{file}')
                        image = image.resize((64, 64))
                        image.save(f'{rootdir}\\{file}')
                    except PIL.UnidentifiedImageError:
                        os.remove(f'{rootdir}\\{file}')

    rootdir = f'C:\\Users\\david\\PycharmProjects\\pythonProject\\ProfessionalPortfolio\\Animal_Classifier_AI\\raw-img'

    data = tf.keras.utils.image_dataset_from_directory(rootdir, shuffle=True)
    model_train_animal_classifier(data)
