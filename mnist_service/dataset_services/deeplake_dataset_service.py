# mnist_service/dataset_loaders/deeplake_dataset_loader.py

import deeplake
import typing
from dataset_services.base_dataset_loader import BaseDatasetService
from utils.logger import Logger

class DeepLakeDatasetService(BaseDatasetService):
    def __init__(self, logger: Logger):
        self.logger = logger
        self.dataset_url = "hub://activeloop/mnist-train"

    def get_samples(self, batch_size: int) -> typing.Generator[typing.Tuple[bytes, str], None, None]:
        try:
            ds = deeplake.load(self.dataset_url)
            for idx, entry in enumerate(ds):
                if idx >= batch_size:
                    break
                image_bytes = entry["images"].tobytes()
                label_str = str(entry["labels"].data()["text"][0])
                yield image_bytes, label_str
        except Exception as e:
            self.logger.exception(f"Error fetching data from DeepLake: {e}")
            raise
