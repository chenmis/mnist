import os
import typing

import dataset_services


class GrpcServiceFactory:
    @staticmethod
    def get_grpc_server(service_type: typing.Optional[dataset_services.enums.ServiceType] = None) -> dataset_services.BaseDatasetService:
        if service_type is None:
            # Choose the dataset loader based on the environment variable
            service_type = dataset_services.enums.ServiceType[os.getenv("DATASET_SOURCE", dataset_services.enums.ServiceType.tensorflow)]

        return dataset_services.get_service(service_type)

