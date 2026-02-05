from collections.abc import Mapping
from json import dumps
from logging import getLogger
from typing import Any
from uuid import uuid4

from renderers import docx
from robyn import BaseRobyn
from services import WorkspaceService
from utils.payload import Payload

logger = getLogger(__name__)


def register(app: BaseRobyn) -> None:
    logger.info("Registering docx tools MCP...")

    try:
        mcp = app.mcp

    except Exception as e:
        logger.error(f"Failed to get MCP from app: {e}")
        return

    logger.info("Successfully obtained MCP from app.")

    logger.info("Setting up WorkspaceService...")
    workspace_service = WorkspaceService(root_parent=".")
    logger.info("WorkspaceService setup complete.")

    @mcp.tool(name="initialize_resume", description="Initialize a resume workspace.")
    def initialize_resume(user_id: str) -> str:
        render_id = uuid4().hex
        workspace_service.create_artifact(user_id, render_id)
        docx.create_document(
            workspace_service.get_artifact(user_id, render_id) / "resume.docx"
        )

        logger.info(
            f"Initialized resume workspace for user_id: {user_id}, render_id: {render_id}"
        )

        return dumps(
            {
                "ok": True,
                "render_id": render_id,
            }
        )

    logger.info(f"Registered {initialize_resume.__name__} in MCP tools.")

    @mcp.tool(
        name="render_resume",
        description="Render a resume document in DOCX format.",
        input_schema={
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The user ID."},
                "render_id": {
                    "type": "string",
                    "description": "The render ID provided upon initialization.",
                },
                "payload": {
                    "type": "object",
                    "description": "The payload containing resume data.",
                },
            },
            "required": ["user_id", "render_id", "payload"],
        },
    )
    def render_resume(
        user_id: str,
        render_id: str,
        payload: Payload,
    ) -> Mapping[str, Any]:
        path = workspace_service.get_artifact(user_id, render_id) / "resume.docx"
        try:
            docx.render(path, payload)

        except Exception as e:
            logger.error(
                f"Error rendering resume for user_id: {user_id}, render_id: {render_id}: {e}"
            )
            raise e

        logger.info(f"Rendered resume for user_id: {user_id}, render_id: {render_id}")

        workspace_service.save_artifact(user_id, render_id)

        return {
            "ok": True,
            "message": "Rendered resume successfully.",
            "artifact": {
                "type": "docx",
                "path": str(path),
            },
        }

    logger.info(f"Registered {render_resume.__name__} in MCP tools.")
