#!/usr/bin/env python3
import argparse
import logging
import os
from concurrent import futures

import grpc

from grpc_servicers import MnistGrpcService
from protos import mnist_pb2_grpc
from utils.grpc_service_factory import GrpcServiceFactory


def run_server(logger: logging.Logger) -> None:
    try:
        dataset_service = GrpcServiceFactory.get_grpc_server(logger)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        grpc_service = MnistGrpcService(dataset_service, server)
        grpc_service.run_server()

    except Exception:
        logger.exception(f"gRPC error - Shutting down.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Mnist dataset service",
        description="This program sending the MNIST dataset. "
                    "The Mnist dataset is streamed using gRPC protocol."
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Increase log verbosity.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Logger setup
    logger = logging.getLogger(name=__name__)
    logger.level = logging.DEBUG if args.verbose else logging.INFO
    run_server(logger)


if __name__ == '__main__':
    main()
