from abc import ABC, abstractmethod


class OnlineStorage(ABC):
    @abstractmethod
    def upload_artifact(self, user_id: str, process_id: str, data: bytes) -> None: ...

    @abstractmethod
    def download_artifact(self, user_id: str, process_id: str) -> bytes: ...

    @abstractmethod
    def artifact_exists(self, user_id: str, process_id: str) -> bool: ...
