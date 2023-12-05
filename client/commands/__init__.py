from commands.base_command import BaseCommand
from commands.enums import CommandType
from commands.train_mnist_model import MnistModelTrainer

_command_type_to_command_class_mapping = {
    MnistModelTrainer.get_command_type(): MnistModelTrainer,
}


def get_command(command_type: CommandType) -> BaseCommand:
    return _command_type_to_command_class_mapping[command_type]()


__all__ = (
    BaseCommand,
    CommandType,
    MnistModelTrainer,
    get_command,
)
