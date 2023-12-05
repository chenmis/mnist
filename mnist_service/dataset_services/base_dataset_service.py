import abc
import typing

from dataset_services import enums as dataset_services_enums


class BaseDatasetService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_service_type(cls) -> dataset_services_enums.ServiceType:
        pass

    @abc.abstractmethod
    def get_samples(self) -> typing.Generator[typing.Tuple[bytes, str], None, None]:
        pass


