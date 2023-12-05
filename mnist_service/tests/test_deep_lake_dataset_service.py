import logging
import unittest
from unittest.mock import patch, MagicMock
from dataset_services.deeplake_dataset_service import DeepLakeDatasetService


_logger = logging.getLogger(__name__)


class TestDeepLakeDatasetService(unittest.TestCase):

    def setUp(self):
        self.service = DeepLakeDatasetService(_logger)

    @patch('deeplake.load')
    def test_get_samples_returns_correct_data_format(self, mock_load):
        mock_image = MagicMock()
        mock_image.tobytes.return_value = b'some_image_data'
        mock_label = MagicMock()
        mock_label.data.return_value = {"text": [0]}

        mock_ds = MagicMock()
        mock_ds.__iter__.return_value = iter([{'images': mock_image, 'labels': mock_label}])
        mock_load.return_value = mock_ds

        generator = self.service.get_samples()
        image_bytes, label = next(generator)
        self.assertIsInstance(image_bytes, bytes)
        self.assertIsInstance(label, str)

    @patch('deeplake.load')
    def test_get_samples_handles_exceptions(self, mock_load):
        mock_load.side_effect = Exception("Test Error")
        with self.assertRaises(Exception):
            next(self.service.get_samples())

    @patch('deeplake.load')
    def test_continuous_data_streaming(self, mock_load):
        mock_ds = MagicMock()
        mock_ds.__iter__.return_value = iter([{'images': MagicMock(), 'labels': MagicMock()} for _ in range(3)])
        mock_load.return_value = mock_ds
        generator = self.service.get_samples()
        results = [next(generator) for _ in range(3)]
        self.assertEqual(len(results), 3)
