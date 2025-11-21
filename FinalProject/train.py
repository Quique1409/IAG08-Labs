import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np
import os

# Definition of variables and image configuration
HEIGHT_IMG = 150 # All Redimention 150x150 px
WIDTH_IMG = 150
BATCH_SIZE = 32  #Image processing
PATH_DATASET = "dataSet"

# Load data and automatically label
trainDs = tf.keras.utils.image_dataset_from_directory(
    # Keras reads the folders and creates the dataset.
    # Use validation_split to separate 20 porcent for testing (validation).
    PATH_DATASET,
    validationSplit = 0.2,
    subSet = "training",
    seed = 123,
    imageSize = (HEIGHT_IMG, WIDTH_IMG),
    batchSize = BATCH_SIZE
)
