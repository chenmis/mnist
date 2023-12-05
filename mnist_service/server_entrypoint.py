#!/usr/bin/env python3
import logging
from concurrent import futures

import grpc

from utils import parse_args
from grpc_service import MnistGrpcService
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
        raise


def main() -> None:
    args = parse_args()

    # Logger setup
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    run_server()


if __name__ == '__main__':
    main()
