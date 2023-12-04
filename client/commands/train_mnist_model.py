# client/commands/train_mnist_model.py
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from grpc_clients import mnist_client
from commands import base_command
from commands import enums as commands_enums
from utils.logger import Logger

logger = Logger(__name__)


class MnistModelTrainer(base_command.BaseCommand):
    model = None  # Class attribute for the model

    @classmethod
    def get_command_type(cls) -> commands_enums.CommandType:
        return commands_enums.CommandType.train

    @classmethod
    def execute(cls, client: mnist_client.MnistGrpcClient) -> None:
        logger.info("Starting MNIST model training.")

        if cls.model is None:
            cls.model = cls.create_model()
            cls.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
            logger.info("Created and compiled a new model.")

        try:
            response = client.get_mnist_samples(batch_size=10000)
            images, labels = cls.prepare_data(response)
            cls.model.fit(images, labels, epochs=5)
            logger.info("Model training completed successfully.")
        except Exception as e:
            logger.exception(f"Error during model training: {e}")

    @staticmethod
    def prepare_data(response):
        images = []
        labels = []
        for sample in response:
            images.append(sample.image)  # Directly append the raw bytes
            labels.append(int(sample.label))
        return np.array(images), np.array(labels)

    @staticmethod
    def create_model():
        logger.debug("Creating the model.")
        model = models.Sequential([
            layers.Lambda(lambda x: tf.map_fn(lambda y: tf.image.decode_png(y, channels=1), x, dtype=tf.uint8)),
            layers.Rescaling(1./255),
            layers.Flatten(input_shape=(28, 28)),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(10, activation='softmax')
        ])
        return model
