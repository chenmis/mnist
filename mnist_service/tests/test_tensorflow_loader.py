import os


class TestTensorflowLoader:
    def test_sanity(self) -> None:
        assert os.environ["GRPC_PORT"] == "1234"
