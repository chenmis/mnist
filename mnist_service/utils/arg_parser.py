import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Mnist dataset service",
        description="This program sending the MNIST dataset. "
                    "The Mnist dataset is streamed using gRPC protocol."
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Increase log verbosity.")
    return parser.parse_args()
