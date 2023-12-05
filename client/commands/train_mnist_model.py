import logging
import typing

import numpy.typing
import numpy as np
import tensorflow as tf
import keras

from grpc_clients import mnist_client
from commands import base_command
from utils import CommandType

logger = logging.getLogger(__name__)


class PrintStatusCallback(keras.callbacks.Callback):
    def __init__(self):
        super().__init__()
        self.counter = 0

    def on_batch_end(self, batch, logs=None):
        self.counter += batch
        if self.counter % 100 == 0:
            logger.info(f"Processed {self.counter} images - Loss: {logs['loss']}, Accuracy: {logs['accuracy']}")


class MnistModelTrainer(base_command.BaseCommand):
    @classmethod
    def get_command_type(cls) -> CommandType:
        return CommandType.train

    @classmethod
    def execute(cls, client: mnist_client.MnistGrpcClient) -> None:
        logger.info("Starting MNIST model training.")

        model = cls.create_model()
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        logger.info("Created and compiled a new model.")

        try:
            model.fit(
                x=cls.data_generator(client),
                verbose=2,
                callbacks=[PrintStatusCallback()]
            )
            logger.info("Model training completed successfully.")
        except Exception:
            logger.exception("Error during model training.")
            raise

    @staticmethod
    def data_generator(
            client: mnist_client.MnistGrpcClient,
    ) -> typing.Generator[typing.Tuple[numpy.typing.NDArray, numpy.typing.NDArray], None, None]:
        samples_generator = client.get_mnist_samples()

        for sample in samples_generator:
            logger.debug(f"Received sample with label {sample.label}")
            image = tf.io.decode_png(sample.image, channels=1)
            image = tf.image.convert_image_dtype(image, tf.float32)
            yield np.array([image]), np.array([sample.label])

    @staticmethod
    def create_model() -> keras.Model:
        logger.debug("Creating the model.")
        model = keras.models.Sequential([
            keras.layers.Flatten(input_shape=(28, 28, 1)),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(10, activation='softmax')
        ])
        return model
