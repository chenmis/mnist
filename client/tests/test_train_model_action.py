import unittest
from unittest.mock import Mock, patch

from commands import MnistModelTrainer


class TestMnistModelTrainer(unittest.TestCase):
    @patch('keras.models.Sequential')
    @patch('grpc_clients.mnist_client.MnistGrpcClient')
    def test_execute_success(self, mock_client, mock_model):
        mock_client.get_mnist_samples.return_value = iter([Mock()])
        mock_model.return_value = Mock()

        MnistModelTrainer.execute(mock_client)

        mock_model.assert_called_once()
        mock_model.return_value.compile.assert_called_once_with(optimizer='adam',
                                                                loss='sparse_categorical_crossentropy',
                                                                metrics=['accuracy'])
        mock_model.return_value.fit.assert_called_once()

    @patch('grpc_clients.mnist_client.MnistGrpcClient')
    def test_create_model_called(self, mock_client):
        with patch.object(MnistModelTrainer, 'create_model', return_value=Mock()) as mocked_create_model:
            MnistModelTrainer.execute(mock_client)
            mocked_create_model.assert_called_once()


if __name__ == '__main__':
    unittest.main()


