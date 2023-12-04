import abc
import typing


class BaseDatasetService(abc.ABC):
    @abc.abstractmethod
    def get_samples(self, batch_size: int) -> typing.Generator[typing.Tuple[bytes, str], None, None]:
        pass
