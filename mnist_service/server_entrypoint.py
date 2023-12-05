#!/usr/bin/env python3
import argparse
import logging
from concurrent import futures

import grpc

from grpc_servicers import MnistGrpcService
from utils.grpc_service_factory import GrpcServiceFactory

_logger = logging.getLogger(__name__)


def run_server() -> None:
    try:
        dataset_service = GrpcServiceFactory.get_grpc_server()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        grpc_service = MnistGrpcService(dataset_service, server)
        grpc_service.run_server()
    except Exception:
        _logger.exception(f"gRPC error - Shutting down.")


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
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    run_server()


if __name__ == '__main__':
    main()
