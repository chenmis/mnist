import contextlib
import logging
import json
import os
import typing

import grpc

import grpc_clients


_logger = logging.getLogger(__name__)

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
def get_grpc_context_manager() -> typing.ContextManager[grpc_clients.MnistGrpcClient]:
    try:
        address = os.getenv("GRPC_ADDRESS", "localhost")
        port = os.getenv("GRPC_PORT", "50051")
        target = f"{address}:{port}"

        _logger.info(f"Attempting to connect to gRPC server at {target}.")
        with grpc.insecure_channel(target=target, options=(("grpc.service_config", grpc_client_config),), ) as channel:
            yield grpc_clients.MnistGrpcClient(channel=channel)
    except grpc.RpcError:
        _logger.error(f"gRPC error occurred while connecting to server.")
        raise
