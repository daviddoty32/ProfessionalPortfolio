from tensorflow import keras
import tensorflow as tf

import os


def model_create():
    model = keras.Sequential([
        keras.layers.Resizing(256, 256),
        keras.layers.RandomFlip(mode='horizontal'),
        keras.layers.RandomZoom(.1),
        keras.layers.RandomContrast(.1),


        keras.layers.Convolution2D(8, 3, activation='relu'),
        keras.layers.MaxPool2D(),

        keras.layers.Convolution2D(16, 3, activation='relu'),
        keras.layers.MaxPool2D(),

        keras.layers.Convolution2D(32, 3, activation='relu'),
        keras.layers.MaxPool2D(),

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
        model = tf.keras.models.load_model(f'{os.getcwd()}/{model}')
        model.summary()
        return model
    except OSError:
        print('Model not found, check spelling and try again.')
        raise FileNotFoundError


def model_train(model_name, data):
    try:
        model = model_fetch(model_name)
    except OSError:
        model = model_create()

    model.fit(data, epochs=10, batch_size=20)

    model.save(model_name)

def model_test(model_name, data):
    model = model_fetch(model_name)

    model.evaluate(data)

def data_split(data):
    data_train = data.take(int(len(data)*.75))
    data_test = data.skip(int(len(data)*.75))
    return data_train, data_test
def main():


    rootdir = f'{os.getcwd()}/raw-img'

    data = tf.keras.utils.image_dataset_from_directory(rootdir, shuffle=True, batch_size=100)
    data_train, data_test = data_split(data)

    model_name = 'AnimalClassifier'
    #model_train(model_name, data_train)
    model_test(model_name,  data_test)

main()