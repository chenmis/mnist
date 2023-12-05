#!/usr/bin/env python3
import contextlib
import json
import logging
import os
import typing

import grpc

import commands
import grpc_clients
from utils import parse_args

_logger = logging.getLogger(name=__name__)

# move to config.py
grpc_client_config = json.dumps({
        "methodConfig": [{
            "name": [{}],
            "retryPolicy": {
                "maxAttempts": 5,
                "initialBackoff": "0.1s",
                "maxBackoff": "10s",
                "backoffMultiplier": 2,
                "retryableStatusCodes": ["UNAVAILABLE"],
            },
        }]
    })


@contextlib.contextmanager
def _get_grpc_context_manager() -> typing.ContextManager[grpc_clients.MnistGrpcClient]:
    try:
        address = os.getenv("GRPC_ADDRESS", "localhost")
        port = os.getenv("GRPC_PORT", "50051")
        target = f"{address}:{port}"

        _logger.info(f"Attempting to connect to gRPC server at {target}.")
        with grpc.insecure_channel(target=target, options=(("grpc.service_config", grpc_client_config),), ) as channel:
            yield grpc_clients.MnistGrpcClient(channel=channel)
    except grpc.RpcError as e:
        _logger.error(f"gRPC error occurred while connecting to server: {e}")
        raise


def main() -> None:
    args = parse_args()

    # Initialize logger with the appropriate level based on the verbose flag
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    _logger.info("Starting execution.")
    command = commands.get_command(args.command)
    with _get_grpc_context_manager() as client:
        command.execute(client=client)


if __name__ == '__main__':
    main()
