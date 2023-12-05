import os
import typing

import dataset_services
from utils import ServiceType

class GrpcServiceFactory:
    @staticmethod
    def get_grpc_server(service_type: typing.Optional[ServiceType] = None) -> dataset_services.BaseDatasetService:
        if service_type is None:
            # Choose the dataset loader based on the environment variable
            service_type = ServiceType[os.getenv("DATASET_SOURCE", ServiceType.tensorflow)]

        return dataset_services.get_service(service_type)

