from dataset_services import enums
from dataset_services.base_dataset_service import BaseDatasetService
from dataset_services.deeplake_dataset_service import DeepLakeDatasetService
from dataset_services.tensorflow_dataset_service import TensorflowDatasetService


_service_type_to_service_class_mapping = {
    TensorflowDatasetService.get_service_type(): TensorflowDatasetService,
    DeepLakeDatasetService.get_service_type(): DeepLakeDatasetService,
}


def get_service(service_type: enums.ServiceType) -> BaseDatasetService:
    return _service_type_to_service_class_mapping[service_type]()


__all__ = (
    enums,
    BaseDatasetService,
    TensorflowDatasetService,
    DeepLakeDatasetService,
    get_service,
)
