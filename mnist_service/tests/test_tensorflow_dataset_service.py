import unittest
from unittest.mock import patch
import numpy as np
import tensorflow as tf

from utils import ServiceType
from dataset_services import TensorflowDatasetService


class TestTensorflowDatasetService(unittest.TestCase):

    def setUp(self):
        self.service = TensorflowDatasetService()

    def test_init(self):
        with patch('logging.Logger.info') as mock_log_info:
            service = TensorflowDatasetService()
            mock_log_info.assert_called_with("TensorflowDatasetService initialized.")

    def test_get_service_type(self):
        self.assertEqual(self.service.get_service_type(), ServiceType.tensorflow)

    @patch('tensorflow.keras.datasets.mnist.load_data')
    def test_get_samples(self, mock_load_data):
        mock_load_data.return_value = ((np.random.rand(100, 28, 28), np.random.randint(0, 10, 100)), None)
        with patch.object(self.service, '_get_image_bytes') as mock_get_image_bytes:
            mock_get_image_bytes.return_value = b'image_bytes'
            samples = list(self.service.get_samples())
            self.assertEqual(len(samples), 100)
            for image_bytes, label in samples:
                self.assertEqual(image_bytes, b'image_bytes')
                self.assertIsInstance(label, str)

    @patch('tensorflow.image.convert_image_dtype')
    @patch('tensorflow.io.encode_png')
    def test_get_image_bytes(self, mock_encode_png, mock_convert_image_dtype):
        mock_convert_image_dtype.return_value = tf.constant([[0]], dtype=tf.uint8)
        mock_encode_png.return_value = tf.constant(b'image_bytes', dtype=tf.string)
        image = np.random.rand(28, 28).astype(np.float32)
        image_bytes = self.service._get_image_bytes(image)
        self.assertEqual(image_bytes, b'image_bytes')


if __name__ == '__main__':
    unittest.main()
