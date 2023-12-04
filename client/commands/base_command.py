import abc

from grpc_clients import mnist_client
from commands import enums as commands_enums


class BaseCommand(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_command_type(cls) -> commands_enums.CommandType:
        pass

    @classmethod
    @abc.abstractmethod
    def execute(cls, client: mnist_client.MnistGrpcClient) -> None:
        pass
