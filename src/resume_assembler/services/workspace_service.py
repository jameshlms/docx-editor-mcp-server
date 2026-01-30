from typing import Any

from infra.locks.process_lock_handler import ProcessLockHandler
from sessions import workspace


class WorkspaceService:
    def __init__(self, lock: ProcessLockHandler) -> None:
        self.lock = lock

    def create_process(self, user_id: str, process_id: str) -> dict[str, Any]:
        with self.lock.acquire(user_id, "create_process"):
            workspace.create_process(user_id, process_id)
            return {
                "ok": True,
                "message": "Successfully created directory for new process.",
                "process_id": process_id,
            }
