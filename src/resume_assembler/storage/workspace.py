from pathlib import Path

from storage.online.blob_storage import OnlineStorage

online_storage: OnlineStorage | None = None

WORKSPACE_DIRNAME = "workspace"
ARTIFACTS_DIRNAME = "artifacts"
ARTIFACT_FILENAME = "artifact"
METADATA_FILENAME = "metadata.json"
MANIFEST_FILENAME = "manifest.json"

DOT = "."
SLASH = "/"


online_storage: OnlineStorage | None = None


def create_workspace(root_parent: Path | str | None = None) -> Path:
    workspace_dir = Path(root_parent, WORKSPACE_DIRNAME)

    return workspace_dir


def _throw_if_has_invalid_characters(input: str) -> None:
    if any(char in (DOT, SLASH) for char in input):
        raise ValueError("Invalid characters in input")


def _job_dir(workspace_dir: Path, user_id: str, job_id: str) -> Path:
    _throw_if_has_invalid_characters(user_id)
    _throw_if_has_invalid_characters(job_id)
    path = workspace_dir / user_id / ARTIFACTS_DIRNAME / job_id
    return path


def create_artifact(workspace_dir: Path, user_id: str, job_id: str) -> Path:
    path = _job_dir(workspace_dir, user_id, job_id)
    path.mkdir(parents=True, exist_ok=True)

    artifact_path = path / ARTIFACT_FILENAME

    return artifact_path


def get_artifact(workspace_dir: Path, user_id: str, job_id: str) -> Path:
    path = _job_dir(workspace_dir, user_id, job_id)

    if not path.exists():
        with open(path / ARTIFACT_FILENAME, "rb") as f:
            path.mkdir(parents=True, exist_ok=True)
            f.write(online_storage.download(user_id, job_id))

    artifact_path = path / ARTIFACT_FILENAME
    return artifact_path


def save_artifact(
    workspace_dir: Path, user_id: str, job_id: str, clear_local: bool = False
) -> None:
    path = _job_dir(workspace_dir, user_id, job_id)
    path.mkdir(parents=True, exist_ok=True)

    artifact_path = path / ARTIFACT_FILENAME
    with open(artifact_path, "wb") as f:
        online_storage.upload(user_id, job_id, f.read())

    if clear_local:
        for item in path.iterdir():
            item.unlink()
        path.rmdir()
