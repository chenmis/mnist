import enum


class ServiceType(str, enum.Enum):
    tensorflow = "tensorflow"
    deeplake = "deeplake"
