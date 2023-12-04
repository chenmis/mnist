import logging
import typing

import numpy as np
import tensorflow as tf

from dataset_services import base_dataset_loader
from utils.logger import Logger


class TensorflowDatasetService(base_dataset_loader.BaseDatasetService):
    def __init__(self, logger: Logger):
        self.logger = logger
        self.logger.info("TensorflowDatasetLoader initialized.")

    def get_samples(self, batch_size: int) -> typing.Generator[typing.Tuple[bytes, str], None, None]:
        try:
            (train_images, train_labels), _ = tf.keras.datasets.mnist.load_data()
            train_images = train_images.astype(np.float32) / 255.0

            for idx, (image, label) in enumerate(zip(train_images, train_labels)):
                if idx == batch_size:
                    break
                image_bytes = self._get_image_bytes(image)
                self.logger.debug(f"Generated sample image no. {idx} with label {label}")
                yield image_bytes, str(label)
        except Exception:
            self.logger.exception("Error in get_samples")
            raise

    @staticmethod
    def _get_image_bytes(image) -> bytes:
        try:
            image_uint8 = tf.image.convert_image_dtype(image, tf.uint8, saturate=True)
            return tf.io.encode_png(tf.expand_dims(image_uint8, -1)).numpy()
        except Exception as e:
            logging.exception("Error converting image to bytes: ", e)
            raise
