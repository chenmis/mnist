# client/commands/train_mnist_model.py
import logging
import typing

import numpy as np
import tensorflow as tf
import keras

from commands import base_command
from commands import enums as commands_enums
from grpc_clients import mnist_client

_logger = logging.getLogger(__name__)


class MnistModelTrainer(base_command.BaseCommand):
    @classmethod
    def get_command_type(cls) -> commands_enums.CommandType:
        return commands_enums.CommandType.train

    @classmethod
    def execute(cls, client: mnist_client.MnistGrpcClient) -> None:
        _logger.info("Starting MNIST model training.")

        model = cls.create_model()
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        _logger.info("Created and compiled a new model.")

        try:
            model.fit_generator(
                generator=tf.data.Dataset.from_generator(
                    lambda: cls._get_data_generator(client=client),
                    output_types=(tf.uint8, tf.int64),
                ),
                verbose=2,
            )
            _logger.info("Model training completed successfully.")
        except Exception:
            _logger.exception("Error during model training.")
            raise

    @classmethod
    def _get_data_generator(
            cls,
            client: mnist_client.MnistGrpcClient,
    ) -> typing.Generator[typing.Tuple[bytes, int], None, None]:
        samples = client.get_mnist_samples(batch_size=10000)
        for sample in samples:
            yield sample.image, sample.label

    # @staticmethod
    # def prepare_data(response):
    #     images = []
    #     labels = []
    #     for sample in response:
    #         images.append(sample.image)  # Directly append the raw bytes
    #         labels.append(int(sample.label))
    #     return np.array(images), np.array(labels)

    @staticmethod
    def create_model() -> keras.Model:
        _logger.debug("Creating a ... model")
        model = keras.models.Sequential([
            keras.layers.Lambda(lambda x: tf.map_fn(lambda y: tf.image.decode_png(y, channels=1), x, dtype=tf.uint8)),
            keras.layers.Rescaling(1./255),
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(10, activation="softmax")
        ])
        return model
