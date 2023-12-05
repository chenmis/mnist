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
    def __init__(self, dataset_service: BaseDatasetService, server: grpc.Server):
        self._server = server
        self._dataset_service = dataset_service

        mnist_pb2_grpc.add_MnistServiceServicer_to_server(self, server)
        _logger.info("MnistGrpcService initialized.")

    def run_server(self):
        port = os.getenv("GRPC_PORT", "50051")
        address = f"[::]:{port}"
        self._server.add_insecure_port(address)
        self._server.start()
        _logger.info(f"Server started at {address}.")
        self._server.wait_for_termination()

    def SendMnistSamples(
            self,
            request: mnist_pb2.StreamRequest,
            context: grpc.ServicerContext
    ) -> typing.Generator[mnist_pb2.Sample, None, None]:
        _logger.info("Serving SendMnistSamples request.")
        try:
            return (
                mnist_pb2.Sample(image=image_bytes, label=int(label_str))
                for image_bytes, label_str in self._dataset_service.get_samples()
            )
        except Exception:
            _logger.exception("Error in SendMnistSamples")
            context.abort(grpc.StatusCode.INTERNAL, "Internal error occurred.")
