import unittest
from unittest.mock import Mock, patch
from dataset_services import BaseDatasetService
from protos import mnist_pb2
import grpc
from grpc_service import MnistGrpcService


class TestMnistGrpcService(unittest.TestCase):

    def setUp(self):
        self.mock_server = Mock(spec=grpc.Server)
        self.mock_dataset_service = Mock(spec=BaseDatasetService)
        self.grpc_service = MnistGrpcService(self.mock_dataset_service, self.mock_server)

    def test_run_server(self):
        with patch.object(self.grpc_service._server, 'start') as mock_start, \
             patch.object(self.grpc_service._server, 'wait_for_termination') as mock_wait:
            self.grpc_service.run_server()
            mock_start.assert_called_once()
            mock_wait.assert_called_once()

    def test_SendMnistSamples_success(self):
        image_array_byte_mock = b'image_bytes'

        mock_context = Mock(spec=grpc.ServicerContext)
        self.mock_dataset_service.get_samples.return_value = [(image_array_byte_mock, '1')]
        generator = self.grpc_service.SendMnistSamples(mnist_pb2.StreamRequest(), mock_context)
        response = next(generator)
        self.assertIsInstance(response, mnist_pb2.Sample)
        self.assertEqual(response.image, image_array_byte_mock)
        self.assertEqual(response.label, 1)


if __name__ == '__main__':
    unittest.main()
