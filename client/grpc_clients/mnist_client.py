import logging
import typing

import grpc

from protos import mnist_pb2
from protos import mnist_pb2_grpc

_logger = logging.getLogger(__name__)


class MnistGrpcClient:
    def __init__(self, channel: grpc.Channel):
        self._grpc_service = mnist_pb2_grpc.MnistServiceStub(channel)
        _logger.info("MnistGrpcClient initialized.")

        self._grpc_service = mnist_pb2_grpc.MnistServiceStub(channel)

    def get_mnist_samples(self, batch_size: int) -> typing.Generator[mnist_pb2.Sample, None, None]:
        _logger.debug(f"Requesting {batch_size} MNIST samples from server.")
        return self._grpc_service.SendMnistSamples(request=mnist_pb2.StreamRequest(batch_size=batch_size))


