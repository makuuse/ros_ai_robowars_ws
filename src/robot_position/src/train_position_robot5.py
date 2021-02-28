#!/usr/bin/python3

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras  #Abstraktiokerros?
from tensorflow.keras import layers

def sanitize(data):
    valid = '1234567890.'
    return float(''.join(filter(lambda char: char in valid, data)))


train_dataset_path = 'robot5_positions1.csv'
test_dataset_path = 'robot5_positions2.csv'
validation_dataset_path = 'robot5_positions3.csv'

# CSV-tiedoston sarakkeiden otsikot...
column_names = ['yaw_radians', 'lidar1_ranges', 'ground_truth_x', 'ground_truth_y']

raw_train_dataset = pd.read_csv(train_dataset_path, names = column_names) # Datasetin lataus...
#print(raw_train_dataset.shape)
#print(raw_train_dataset.head)
#raw_train_dataset['lidar1_ranges'] = raw_train_dataset['lidar1_ranges'].str.replace('\'', '', regex = True)
#raw_train_dataset['lidar1_ranges'] = raw_train_dataset['lidar1_ranges'].str.replace('(', '', regex = True)
#raw_train_dataset['lidar1_ranges'] = raw_train_dataset['lidar1_ranges'].str.replace(')', '', regex = True)
#raw_train_dataset['lidar1_ranges'] = tf.convert_to_tensor(raw_train_dataset['lidar1_ranges'])
print(raw_train_dataset)
train_dataset = raw_train_dataset.copy() # Jätetään "raaka datasetti" erilleen.... Jos sitä pitää muokata tms?
train_label_x = train_dataset.pop('ground_truth_x')
train_label_y = train_dataset.pop('ground_truth_y')

train_labels = pd.concat([train_label_x, train_label_y], axis = 1) # Uusi datasetti, missä x ja y samassa...

raw_validation_dataset = pd.read_csv(validation_dataset_path, names = column_names)
#raw_validation_dataset['lidar1_ranges'] = raw_validation_dataset['lidar1_ranges'].str.replace('\'', '', regex = True)
raw_validation_dataset['lidar1_ranges'] = raw_validation_dataset['lidar1_ranges'].str.replace('(', '', regex = True)
raw_validation_dataset['lidar1_ranges'] = raw_validation_dataset['lidar1_ranges'].str.replace(')', '', regex = True)
raw_validation_dataset['lidar1_ranges'] = tf.convert_to_tensor(raw_validation_dataset['lidar1_ranges'])
print(raw_validation_dataset)
validation_dataset = raw_validation_dataset.copy()
validation_label_x = validation_dataset.pop('ground_truth_x')
validation_label_y = validation_dataset.pop('ground_truth_y')

validation_labels = pd.concat([validation_label_x, validation_label_y], axis = 1) # Uusi datasetti, missä x ja y samassa...
#print(validation_labels.head)

raw_test_dataset = pd.read_csv(test_dataset_path, names = column_names)
#raw_test_dataset['lidar1_ranges'] = raw_test_dataset['lidar1_ranges'].str.replace('\'', '', regex = True)
raw_test_dataset['lidar1_ranges'] = raw_test_dataset['lidar1_ranges'].str.replace('(', '', regex = True)
raw_test_dataset['lidar1_ranges'] = raw_test_dataset['lidar1_ranges'].str.replace(')', '', regex = True)
raw_test_dataset['lidar1_ranges'] = tf.convert_to_tensor(raw_test_dataset['lidar1_ranges'])
print(raw_test_dataset)
test_dataset = raw_test_dataset.copy()
test_label_x = test_dataset.pop('ground_truth_x')
test_label_y = test_dataset.pop('ground_truth_y')

test_labels = pd.concat([test_label_x, test_label_y], axis = 1) # Uusi datasetti, missä x ja y samassa...
#print(test_labels.head)

def build_model():
    model = keras.Sequential([
        layers.Dense(64, activation = "relu", input_shape = [len(train_dataset.keys())], name = "layer1"),    # Neuronien määrä ja neuroverkon muoto suoraan datasetin määrästä?
        layers.Dense(64, activation = "relu", name = "layer2"),
        layers.Dense(2, activation = "relu", name = "layer3")
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001) # Learning rate 0.001?

    model.compile(loss = 'mse', 
                  optimizer = optimizer,
                  metrics = ['mae', 'mse'])
    return model

model = build_model()

print(model.summary())

EPOCHS = 10
mae = 0 # Mean absolute error...

for x in range(50):
    history = model.fit(
        train_dataset, train_labels,
        epochs = EPOCHS, validation_data = (validation_dataset, validation_labels), verbose = 1)
    last_mae = mae
    loss, mae, mse = model.evaluate(test_dataset, test_labels, verbose = 2)
    print("Testing set Mean Abs error: {:5.2f} position".format(mae))
    if mae < last_mae:
        print("saving model...")
        model_save_path = "saved_model/robot5_model" + str(x*10) + "epochs"
        model.save(model_save_path) # Tallennetaan malli
