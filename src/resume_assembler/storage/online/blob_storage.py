from abc import ABC, abstractmethod


class OnlineStorage(ABC):
    @abstractmethod
    def upload(self, user_id: str, process_id: str, data: bytes) -> None: ...

    @abstractmethod
    def download(self, user_id: str, process_id: str) -> bytes: ...
