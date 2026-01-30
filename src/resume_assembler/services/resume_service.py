from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

from docx_editor import editor
from infra.locks.process_lock_handler import ProcessLockHandler
from utils.payload import Payload


class ResumeService:
    def __init__(self, lock: ProcessLockHandler) -> None:
        if not isinstance(lock, ProcessLockHandler):
            raise TypeError("lock must be an instance of ProcessLockHandler")
        self.lock = lock

    def _get_resume_path(self, user_id: str, process_id: str) -> Path:
        return Path("workspaces") / user_id / process_id / "resume.docx"

    def set_margins(
        self,
        user_id: str,
        process_id: str,
        margins: Sequence[float] | Mapping[str, float] | None = None,
    ) -> dict:
        with self.lock.acquire(user_id, "set_margins"):
            editor.set_margins(
                self._get_resume_path(user_id, process_id),
                margins,
            )
            return {"ok": True, "message": "Margins set successfully."}

    def add_name(
        self,
        user_id: str,
        process_id: str,
        **kwargs: float | str,
    ) -> dict:
        with self.lock.acquire(user_id, "add_name"):
            editor.add_name(
                self._get_resume_path(user_id, process_id),
                **kwargs,
            )
            return {"ok": True, "message": "Name appended successfully."}

    def add_contact_line(
        self,
        user_id: str,
        process_id: str,
        contacts: Sequence[Mapping[str, str] | str],
        font_name: str,
        font_size: float,
        center: bool = True,
    ) -> dict:
        with self.lock.acquire(user_id, "add_contact_line"):
            editor.add_contact_line(
                self._get_resume_path(user_id, process_id),
                contacts,
                font_name,
                font_size,
                center,
            )
            return {"ok": True, "message": "Contact line appended successfully."}

    def add_summary(
        self,
        user_id: str,
        process_id: str,
        text: str,
        font_name: str,
        font_size: float,
    ) -> dict:
        with self.lock.acquire(user_id, "add_summary"):
            editor.add_summary(
                self._get_resume_path(user_id, process_id),
                text,
                font_name,
                font_size,
            )
            return {"ok": True, "message": "Summary appended successfully."}

    def add_section(
        self,
        user_id: str,
        process_id: str,
        section_headering: str,
        items: Iterable[editor.SectionItemDict],
        font_name: str,
        font_size: float,
    ) -> dict:
        with self.lock.acquire(user_id, "add_section"):
            editor.add_section(
                self._get_resume_path(user_id, process_id),
                section_headering,
                items,
                font_name,
                font_size,
            )
            return {"ok": True, "message": "Section appended successfully."}

    def write_resume(
        self,
        user_id: str,
        process_id: str,
        payload: Payload,
    ) -> dict:
        with self.lock.acquire(user_id, "write_resume"):
            editor.write_resume(
                self._get_resume_path(user_id, process_id),
                payload,
            )
            return {"ok": True, "message": "Resume written successfully."}
