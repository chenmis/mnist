#!/usr/bin/env python3
import logging
import os
from concurrent import futures

import grpc

from grpc_servicers import MnistGrpcService
from protos import mnist_pb2_grpc
from utils.grpc_service_factory import GrpcServiceFactory
from utils.logger import Logger


def run_server(logger: Logger) -> None:
    try:
        dataset_service = GrpcServiceFactory.get_grpc_server(logger)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        grpc_service = MnistGrpcService(dataset_service, server)
        grpc_service.run_server()

    except Exception:
        logger.exception(f"gRPC error - Shutting down.")


def main() -> None:
    # Logger setup
    logger = Logger(name=__name__)
    run_server(logger)


if __name__ == '__main__':
    main()
