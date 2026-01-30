from logging import getLogger
from pathlib import Path
from uuid import uuid4

from infra.locks.process_lock_handler import ProcessLockHandler
from robyn import Robyn
from services.workspace_service import WorkspaceService
from utils.types import JsonObject

logger = getLogger(__name__)

WORKSPACES_PATH = Path("workspaces")


def register(app: Robyn) -> None:
    logger.info("Registering process tools MCP...")
    try:
        mcp = app.mcp

    except Exception as e:
        logger.error(f"Failed to get MCP from app: {e}")
        return

    lock = ProcessLockHandler()
    workspace = WorkspaceService(lock)

    @mcp.tool()
    def create_process(
        user_id: str,
    ) -> JsonObject:
        process_id: str = uuid4().hex
        result = workspace.create_process(user_id, process_id)
        logger.info(f"Created process for user_id: {user_id}, process_id: {process_id}")
        return result

    logger.info(f"Registered {create_process.__name__} in MCP tools.")
