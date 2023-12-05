import logging
import os
import typing
from concurrent import futures

import grpc

import dataset_services
from dataset_services import BaseDatasetService
from protos import mnist_pb2
from protos import mnist_pb2_grpc
from utils.grpc_service_factory import GrpcServiceFactory


_logger = logging.getLogger(__name__)


class MnistGrpcService(mnist_pb2_grpc.MnistServiceServicer):
    def __init__(self, service: BaseDatasetService, server: grpc.Server):
        self._server = server
        self._service = service
        mnist_pb2_grpc.add_MnistServiceServicer_to_server(self._service, self._server)
        _logger.info("MnistGrpcServicer initialized.")

    def run_server(self):
        port = os.getenv("GRPC_PORT", "50051")
        address = f"[::]:{port}"
        self._server.add_insecure_port(address)
        self._server.start()
        _logger.info(f"Server started at {address}.")
        self._server.wait_for_termination()

    def SendMnistSamples(self, request: mnist_pb2.StreamRequest, context: grpc.ServicerContext) -> typing.Generator[mnist_pb2.Sample, None, None]:
        _logger.info(f"Serving SendMnistSamples request with batch size: {request.batch_size}")
        try:
            return (
                mnist_pb2.Sample(image=image_bytes, label=int(label_str))
                for image_bytes, label_str in self._service.get_samples(batch_size=request.batch_size)
            )
        except Exception as e:
            _logger.exception("Error in SendMnistSamples")
            context.abort(grpc.StatusCode.INTERNAL, "Internal error occurred.")
