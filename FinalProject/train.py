import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

# Definition of variables and image configuration
HEIGHT_IMG = 150 
WIDTH_IMG = 150
BATCH_SIZE = 32
PATH_DATASET = os.path.join(base_dir, "dataSet")

# Load data and automatically label
train_ds = tf.keras.utils.image_dataset_from_directory(
    PATH_DATASET,
    validation_split=0.2,
    subset="training",       
    seed=123,
    image_size=(HEIGHT_IMG, WIDTH_IMG),
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    PATH_DATASET,
    validation_split=0.2,
    subset="validation",    
    seed=123,
    image_size=(HEIGHT_IMG, WIDTH_IMG),
    batch_size=BATCH_SIZE
)

# Names of the class
class_names = train_ds.class_names
print(f"Classes Found: {class_names}")

# Load optimization
autotune = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=autotune)
val_ds = val_ds.cache().prefetch(buffer_size=autotune)

# Create the Neural Network Convolutional (NNC)
num_classes = len(class_names) 

model = models.Sequential([
    # Input layer and rescaling
    layers.Rescaling(1./255, input_shape=(HEIGHT_IMG, WIDTH_IMG, 3)),
    
    # Create fake variations
    layers.RandomFlip("horizontal"), 
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),

    # Convolutional Blocks
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),

    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),

    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),

    # Flattening and Classification
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes, activation='softmax')
])

# Compilation
model.compile(optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
            metrics=['accuracy'])

# Training
epochs = 100
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs)

# Model Saved
model.save('models_components.h5')
print("Training completed")