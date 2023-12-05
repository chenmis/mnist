import logging
import typing

import keras
import numpy as np
import tensorflow as tf

from dataset_services import enums as dataset_services_enums
from dataset_services.base_dataset_service import BaseDatasetService

_logger = logging.getLogger(__name__)


class TensorflowDatasetService(BaseDatasetService):
    def __init__(self):
        _logger.info("TensorflowDatasetService initialized.")

    @classmethod
    def get_service_type(cls) -> dataset_services_enums.ServiceType:
        return dataset_services_enums.ServiceType.tensorflow

    def get_samples(self) -> typing.Generator[typing.Tuple[bytes, str], None, None]:
        try:
            (train_images, train_labels), _ = keras.datasets.mnist.load_data()
            train_images = train_images.astype(np.float32) / 255.0

            for idx, (image, label) in enumerate(zip(train_images, train_labels)):
                if idx % 100 == 0:
                    _logger.info("send %s samples so far.", idx)
                image_bytes = self._get_image_bytes(image)
                _logger.debug(f"Sending sample image with label {label}")
                yield image_bytes, str(label)
        except Exception:
            _logger.exception("Error in get_samples.")
            raise

    @staticmethod
    def _get_image_bytes(image) -> bytes:
        try:
            image_uint8 = tf.image.convert_image_dtype(image, tf.uint8, saturate=True)
            return tf.io.encode_png(tf.expand_dims(image_uint8, -1)).numpy()
        except Exception:
            logging.exception("Error converting image to bytes.")
            raise
