import logging
import typing

import grpc

from protos import mnist_pb2
from protos import mnist_pb2_grpc
from utils.logger import Logger

logger = Logger(__name__)


class MnistGrpcClient:
    def __init__(self, channel: grpc.Channel):
        self._grpc_service = mnist_pb2_grpc.MnistServiceStub(channel)
        logger.info("MnistGrpcClient initialized.")

        self._grpc_service = mnist_pb2_grpc.MnistServiceStub(channel)

    def get_mnist_samples(self, batch_size: int) -> typing.Generator[mnist_pb2.Sample, None, None]:
        logger.debug(f"Requesting {batch_size} MNIST samples from server.")
        return self._grpc_service.SendMnistSamples(request=mnist_pb2.StreamRequest(batch_size=batch_size))


