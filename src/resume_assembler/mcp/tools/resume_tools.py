from collections.abc import Mapping
from logging import getLogger
from typing import Any
from uuid import uuid4

from renderers import docx
from robyn import BaseRobyn
from services import WorkspaceService

logger = getLogger(__name__)


def register(app: BaseRobyn) -> None:
    logger.info("Registering docx tools MCP...")

    workspace_service = WorkspaceService(root_parent=".")

    try:
        mcp = app.mcp

    except Exception as e:
        logger.error(f"Failed to get MCP from app: {e}")
        return

    @mcp.tool()
    def initialize_resume(user_id: str) -> Mapping[str, Any]:
        job_id = str(uuid4().hex)
        workspace_service.create_artifact(user_id, job_id)

        logger.info(
            f"Initialized resume workspace for user_id: {user_id}, job_id: {job_id}"
        )

        return {
            "ok": True,
            "job_id": job_id,
        }

    logger.info(f"Registered {initialize_resume.__name__} in MCP tools.")

    @mcp.tool()
    def render_resume(
        user_id: str,
        job_id: str,
        payload: dict[str, Any],
    ) -> Mapping[str, Any]:
        path = workspace_service.get_artifact(user_id, job_id)
        try:
            docx.render(path, payload)

        except Exception as e:
            logger.error(
                f"Error rendering resume for user_id: {user_id}, job_id: {job_id}: {e}"
            )
            raise e

        logger.info(f"Rendered resume for user_id: {user_id}, job_id: {job_id}")

        workspace_service.save_artifact(user_id, job_id)

        return {
            "ok": True,
            "message": "Rendered resume successfully.",
            "artifact": {
                "type": "docx",
                "path": str(path),
            },
        }

    logger.info(f"Registered {render_resume.__name__} in MCP tools.")
