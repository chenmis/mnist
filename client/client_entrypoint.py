#!/usr/bin/env python3
import argparse
import contextlib
import logging
import os
import typing

import grpc

import commands
import grpc_clients


@contextlib.contextmanager
def _grpc_client(logger: logging.Logger) -> typing.ContextManager[grpc_clients.MnistGrpcClient]:
    try:
        address = os.getenv("GRPC_ADDRESS", "localhost")
        port = os.getenv("GRPC_PORT", "50051")
        target = f"{address}:{port}"
        logger.debug(f"Attempting to connect to gRPC server at {target}.")
        with grpc.insecure_channel(target=target) as channel:
            yield grpc_clients.MnistGrpcClient(channel=channel)
    except grpc.RpcError as e:
        logger.error(f"gRPC error occurred while connecting to server: {e}")
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Mnist trainer",
        description="This program trains an ML model from the MNIST dataset. "
                    "The training data is streamed from a remote gRPC server."
    )
    parser.add_argument(
        "-c",
        "--command",
        choices=[command.value for command in commands.CommandType],
        required=True,
        help="The command to run."
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase log verbosity.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Initialize logger with the appropriate level based on the verbose flag
    logger = logging.getLogger(name=__name__)
    logger.level = logging.DEBUG if args.verbose else logging.INFO

    logger.info("Starting execution.")
    command = commands.get_command(args.command)
    with _grpc_client(logger) as client:
        command.execute(client=client)


if __name__ == '__main__':
    main()
