import logging
import unittest
from unittest.mock import patch
import numpy as np
from dataset_services.tensorflow_dataset_service import TensorflowDatasetService

_logger = logging.getLogger(__name__)


class TestTensorflowDatasetService(unittest.TestCase):

    def setUp(self):
        self.service = TensorflowDatasetService(_logger)

    @patch('tensorflow.keras.datasets.mnist.load_data')
    def test_get_samples_returns_correct_data_format(self, mock_load_data):
        # Mock data shaped as 28x28 pixels
        mock_load_data.return_value = ((np.zeros((1, 28, 28)), np.array([0])), None)
        generator = self.service.get_samples()
        image_bytes, label = next(generator)
        self.assertIsInstance(image_bytes, bytes)
        self.assertIsInstance(label, str)

    @patch('tensorflow.keras.datasets.mnist.load_data')
    def test_get_samples_handles_exceptions(self, mock_load_data):
        mock_load_data.side_effect = Exception("Test Error")
        with self.assertRaises(Exception):
            next(self.service.get_samples())

    @patch('tensorflow.keras.datasets.mnist.load_data')
    def test_continuous_data_streaming(self, mock_load_data):
        # Mock data shaped as 28x28 pixels for 3 images
        mock_load_data.return_value = ((np.zeros((3, 28, 28)), np.array([0, 1, 2])), None)
        generator = self.service.get_samples()
        results = [next(generator) for _ in range(3)]
        self.assertEqual(len(results), 3)
