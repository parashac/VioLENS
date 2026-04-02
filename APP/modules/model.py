import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

IMG_SIZE = 224
FRAMES = 30
NUM_CLASSES = 2
LEARNING_RATE = 1e-4

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "epoch_16.weights.h5")

def build_model():
    base_cnn = tf.keras.applications.MobileNetV2(input_shape=(IMG_SIZE, IMG_SIZE, 3),
                                                  include_top=False, weights='imagenet',
                                                  pooling='avg')
    base_cnn.trainable = False
    inputs = keras.Input(shape=(FRAMES, IMG_SIZE, IMG_SIZE, 3))
    x = layers.TimeDistributed(base_cnn)(inputs)
    x = layers.LSTM(128)(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(NUM_CLASSES, activation='softmax')(x)
    model = keras.Model(inputs, outputs)
    model.compile(optimizer=keras.optimizers.Adam(LEARNING_RATE),
                  loss='categorical_crossentropy', metrics=['accuracy'])
    return model


print("[INFO] Building model architecture...")
model = build_model()
print("[INFO] Loading weights from", MODEL_PATH)
model.load_weights(MODEL_PATH)
print("[INFO] Model ready.")