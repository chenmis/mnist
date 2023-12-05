import unittest
from unittest import mock

import grpc

import grpc_clients
from protos import mnist_pb2


class TestMnistGrpcClient(unittest.TestCase):

    @mock.patch('grpc_clients.mnist_client.mnist_pb2_grpc.MnistServiceStub')
    def test_get_mnist_samples_successful_response(self, mock_stub: mock.MagicMock) -> None:
        # Arrange
        mock_channel = mock.Mock()
        mock_response = (mnist_pb2.Sample(image=b'some_image_data', label=1))
        mock_stub.return_value.SendMnistSamples.return_value = mock_response
        client = grpc_clients.MnistGrpcClient(mock_channel)

        # Act
        response = list(client.get_mnist_samples())

        # Assert
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0].image, b"some_image_data")
        self.assertEqual(response[0].label, 1)

    @mock.patch('grpc_clients.mnist_client.mnist_pb2_grpc.MnistServiceStub')
    def test_get_mnist_samples_handles_grpc_errors(self, mock_stub: mock.MagicMock) -> None:
        # Arrange
        mock_channel = mock.Mock()
        mock_stub.return_value.SendMnistSamples.side_effect = grpc.RpcError("Test Error")
        client = grpc_clients.MnistGrpcClient(mock_channel)

        # Act & Assert
        with self.assertRaises(grpc.RpcError):
            list(client.get_mnist_samples())

    @mock.patch('grpc_clients.mnist_client.mnist_pb2_grpc.MnistServiceStub')
    def test_get_mnist_samples_parses_data_correctly(self, mock_stub: mock.MagicMock) -> None:
        # Arrange
        mock_channel = mock.Mock()
        mock_response = [
            mnist_pb2.Sample(image=b'image_data_1', label=1),
            mnist_pb2.Sample(image=b'image_data_2', label=2),
        ]
        mock_stub.return_value.SendMnistSamples.return_value = mock_response
        client = grpc_clients.MnistGrpcClient(mock_channel)

        # Act
        response = list(client.get_mnist_samples())

        # Assert
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].image, b'image_data_1')
        self.assertEqual(response[1].image, b'image_data_2')



