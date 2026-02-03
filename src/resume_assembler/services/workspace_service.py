from pathlib import Path

from storage import workspace


class WorkspaceServiceSingletonMeta(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class WorkspaceService(metaclass=WorkspaceServiceSingletonMeta):
    def __init__(
        self,
        root_parent: str,
    ) -> None:
        self.workspace_dir = workspace.create_workspace(root_parent)

    def create_artifact(
        self,
        user_id: str,
        process_id: str,
    ) -> Path:
        return workspace.create_artifact(self.workspace_dir, user_id, process_id)

    def get_artifact(
        self,
        user_id: str,
        process_id: str,
    ) -> Path:
        return workspace.get_artifact(self.workspace_dir, user_id, process_id)

    def save_artifact(
        self,
        user_id: str,
        process_id: str,
        clear_local: bool = False,
    ) -> None:
        return workspace.save_artifact(
            self.workspace_dir, user_id, process_id, clear_local=clear_local
        )
