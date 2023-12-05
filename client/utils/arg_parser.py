import argparse
from utils import CommandType


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Mnist trainer",
        description="This program trains an ML model from the MNIST dataset. "
                    "The training data is streamed from a remote gRPC server."
    )
    parser.add_argument(
        "-c",
        "--command",
        choices=[command.value for command in CommandType],
        required=True,
        help="The command to run."
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase log verbosity.")
    return parser.parse_args()
