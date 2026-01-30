from pathlib import Path


def _throw_if_has_invalid_characters(input: str) -> None:
    if "." in input or "/" in input:
        raise ValueError("Invalid characters in input")


def _get_process_dir(user_id: str, process_id: str) -> Path:
    _throw_if_has_invalid_characters(user_id)
    _throw_if_has_invalid_characters(process_id)

    workspace_dir = Path("workspaces") / user_id / process_id

    return workspace_dir


def resume_path(user_id: str, process_id: str) -> Path:
    workspace_dir = _get_process_dir(user_id, process_id)
    resume_path = workspace_dir / "resume.docx"
    return resume_path


def workspace_exists(user_id: str, process_id: str) -> bool:
    workspace_dir = _get_process_dir(user_id, process_id)
    return workspace_dir.exists()


def create_process(user_id: str, process_id: str) -> None:
    workspace_dir = _get_process_dir(user_id, process_id)
    workspace_dir.mkdir(parents=True, exist_ok=True)

    (workspace_dir / "resume.docx").touch()
    (workspace_dir / "metadata.json").touch()
