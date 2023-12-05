#!/usr/bin/env python3
import logging


import commands
from utils import parse_args
from utils import context_manager

_logger = logging.getLogger(name=__name__)


def main() -> None:
    args = parse_args()

    # Initialize logger with the appropriate level based on the verbose flag
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    _logger.info("Starting execution.")
    command = commands.get_command(args.command)
    with context_manager.get_grpc_context_manager() as client:
        command.execute(client=client)


if __name__ == '__main__':
    main()
