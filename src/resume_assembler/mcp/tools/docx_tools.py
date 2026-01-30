from collections.abc import Mapping, Sequence
from logging import getLogger
from pathlib import Path
from typing import Any, Union

from infra.locks.process_lock_handler import ProcessLockHandler
from robyn import BaseRobyn
from services.resume_service import ResumeService
from utils.payload import Payload

logger = getLogger(__name__)


def register(app: BaseRobyn) -> None:
    logger.info("Registering docx tools MCP...")

    try:
        mcp = app.mcp

    except Exception as e:
        logger.error(f"Failed to get MCP from app: {e}")
        return

    lock = ProcessLockHandler()
    logger.info("Initialized ProcessLockHandler for docx tools.")
    editor = ResumeService(lock)

    @mcp.tool()
    def add_name(
        user_id: str,
        process_id: str,
        text: str,
        font_name: str,
        font_size: float,
    ) -> Mapping[str, Any]:
        result = editor.add_name(
            Path("workspaces") / user_id / process_id / "resume.docx",
            text=text,
            font_name=font_name,
            font_size=font_size,
        )
        logger.info(
            f"Added name to resume for user_id: {user_id}, process_id: {process_id}"
        )
        return result

    logger.info(f"Registered {add_name.__name__} in MCP tools.")

    @mcp.tool()
    def add_contact_line(
        user_id: str,
        process_id: str,
        contacts: Sequence[Union[Mapping[str, str], str]],
        font_name: str,
        font_size: float,
        bold: bool = False,
        italic: bool = False,
    ) -> Mapping[str, Any]:
        editor.add_contact_line(
            user_id=user_id,
            process_id=process_id,
            contacts=contacts,
            font_name=font_name,
            font_size=font_size,
        )
        logger.info(
            f"Added contact line to resume for user_id: {user_id}, process_id: {process_id}"
        )
        return {"ok": True, "message": "Contact line appended successfully."}

    logger.info(f"Registered {add_contact_line.__name__} in MCP tools.")

    @mcp.tool()
    def set_margins(
        user_id: str,
        process_id: str,
        margins: Sequence[float],
    ) -> Mapping[str, Any]:
        editor.set_margins(
            Path("workspaces") / user_id / process_id / "resume.docx",
            margins,
        )
        logger.info(
            f"Set margins for resume for user_id: {user_id}, process_id: {process_id}"
        )
        return {"ok": True, "message": "Margins set successfully."}

    logger.info(f"Registered {set_margins.__name__} in MCP tools.")

    @mcp.tool()
    def add_section(
        user_id: str,
        process_id: str,
        break_type: str,
    ) -> Mapping[str, Any]: ...

    logger.info(f"Registered {add_section.__name__} in MCP tools.")

    @mcp.tool(
        description="Write a complete resume based on the provided payload.",
        input_schema={
            "properties": {
                "payload": {"type": "object"},
                "process_id": {"type": "string"},
                "user_id": {"type": "string"},
            },
            "required": ["user_id", "process_id", "payload"],
            "type": "object",
        },
    )
    def write_resume(
        user_id: str,
        process_id: str,
        payload: Payload,
    ) -> Mapping[str, Any]:
        editor.write_resume(
            user_id=user_id,
            process_id=process_id,
            payload=payload,
        )
        logger.info(f"Wrote resume for user_id: {user_id}, process_id: {process_id}")
        return {"ok": True, "message": "Resume written successfully."}

    logger.info(f"Registered {write_resume.__name__} in MCP tools.")

    logger.info("Docx tools MCP registration complete.")
