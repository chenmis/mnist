import abc

from grpc_clients import mnist_client
from utils import CommandType


class BaseCommand(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_command_type(cls) -> CommandType:
        pass

    @classmethod
    @abc.abstractmethod
    def execute(cls, client: mnist_client.MnistGrpcClient) -> None:
        pass
