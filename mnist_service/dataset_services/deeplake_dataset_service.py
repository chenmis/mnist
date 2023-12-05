import logging
import typing

import deeplake

from dataset_services import enums as dataset_services_enums
from dataset_services.base_dataset_service import BaseDatasetService

_logger = logging.getLogger(__name__)


class DeepLakeDatasetService(BaseDatasetService):
    def __init__(self):
        self.dataset_url = "hub://activeloop/mnist-train"

    @classmethod
    def get_service_type(cls) -> dataset_services_enums.ServiceType:
        return dataset_services_enums.ServiceType.deeplake

    def get_samples(self) -> typing.Generator[typing.Tuple[bytes, str], None, None]:
        try:
            ds = deeplake.load(self.dataset_url)
            while True:  # Continuously loop over the dataset
                for entry in ds:
                    image_bytes = entry["images"].tobytes()
                    label_str = str(entry["labels"].data()["text"][0])
                    _logger.debug("Sending sample image with label %s.", label_str)
                    yield image_bytes, label_str
        except Exception:
            _logger.exception("Error fetching data from DeepLake.")
            raise
