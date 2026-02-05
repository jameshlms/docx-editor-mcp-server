from pathlib import Path

from storage.online.blob_storage import OnlineStorage

online_storage: OnlineStorage | None = None

WORKSPACE_DIRNAME = "workspace"
ARTIFACTS_DIRNAME = "artifacts"
ARTIFACT_FILENAME = "resume.docx"
METADATA_FILENAME = "metadata.json"
MANIFEST_FILENAME = "manifest.json"

DOT = "."
SLASH = "/"


online_storage: OnlineStorage | None = None


def create_workspace(root_parent: Path | str | None = None) -> Path:
    workspace_dir = Path(root_parent, WORKSPACE_DIRNAME)
    workspace_dir.mkdir(parents=True, exist_ok=True)

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

    return path


def get_artifact(workspace_dir: Path, user_id: str, job_id: str) -> Path:
    path = _job_dir(workspace_dir, user_id, job_id)

    if not online_storage.artifact_exists(user_id, job_id) and not path.exists():
        raise FileNotFoundError(
            "Artifact does not exist locally or online. The artifact likely was never created or has been deleted."
        )

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        with open(path / ARTIFACT_FILENAME, "wb") as f:
            f.write(online_storage.download_artifact(user_id, job_id))

    return path


def save_artifact(
    workspace_dir: Path, user_id: str, job_id: str, clear_local: bool = False
) -> None:
    path = _job_dir(workspace_dir, user_id, job_id)
    path.mkdir(parents=True, exist_ok=True)

    artifact = path / ARTIFACT_FILENAME
    with open(artifact, "rb") as f:
        online_storage.upload_artifact(user_id, job_id, f.read())

    if clear_local:
        for item in path.iterdir():
            item.unlink()
        path.rmdir()
