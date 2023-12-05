import logging
import os

from dataset_services import BaseDatasetService
from dataset_services.deeplake_dataset_service import DeepLakeDatasetService
from dataset_services.tensorflow_dataset_service import TensorflowDatasetService
from enums import ServiceType


class GrpcServiceFactory:
    @staticmethod
    def get_grpc_server(logger: logging.Logger, service_type: ServiceType = ServiceType.deeplake.value) -> BaseDatasetService:
        # Choose the dataset loader based on the environment variable
        dataset_source = os.getenv("DATASET_SOURCE", service_type).lower()
        if dataset_source == "deeplake":
            return DeepLakeDatasetService(logger)
        else:
            return TensorflowDatasetService(logger)
