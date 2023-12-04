import unittest
from unittest.mock import Mock, patch
from grpc_clients.mnist_client import MnistGrpcClient
from protos import mnist_pb2
import grpc


class TestMnistGrpcClient(unittest.TestCase):

    @patch('grpc_clients.mnist_client.mnist_pb2_grpc.MnistServiceStub')
    def test_get_mnist_samples_successful_response(self, mock_stub):
        # Arrange
        mock_channel = Mock()
        mock_response = [mnist_pb2.Sample(image=b'some_image_data', label=1)]
        mock_stub.return_value.SendMnistSamples.return_value = mock_response
        client = MnistGrpcClient(mock_channel)

        # Act
        response = list(client.get_mnist_samples(batch_size=1))

        # Assert
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0].image, b'some_image_data')
        self.assertEqual(response[0].label, 1)

    @patch('grpc_clients.mnist_client.mnist_pb2_grpc.MnistServiceStub')
    def test_get_mnist_samples_handles_grpc_errors(self, mock_stub):
        # Arrange
        mock_channel = Mock()
        mock_stub.return_value.SendMnistSamples.side_effect = grpc.RpcError("Test Error")
        client = MnistGrpcClient(mock_channel)

        # Act & Assert
        with self.assertRaises(grpc.RpcError):
            list(client.get_mnist_samples(batch_size=1))

    @patch('grpc_clients.mnist_client.mnist_pb2_grpc.MnistServiceStub')
    def test_get_mnist_samples_parses_data_correctly(self, mock_stub):
        # Arrange
        mock_channel = Mock()
        mock_response = [mnist_pb2.Sample(image=b'image_data_1', label=1),
                         mnist_pb2.Sample(image=b'image_data_2', label=2)]
        mock_stub.return_value.SendMnistSamples.return_value = mock_response
        client = MnistGrpcClient(mock_channel)

        # Act
        response = list(client.get_mnist_samples(batch_size=2))

        # Assert
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].image, b'image_data_1')
        self.assertEqual(response[1].image, b'image_data_2')



if __name__ == '__main__':
    unittest.main()
