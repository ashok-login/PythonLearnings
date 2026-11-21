from pathlib import Path

from dotenv import load_dotenv


def load_env_file(start_directory: str | Path) -> Path:
    """Load the nearest .env in this directory or its parents and return its path.

    Existing environment variables take precedence over values in the file.
    Raises FileNotFoundError if no .env file can be found.
    Requires python-dotenv to be installed in the active Python environment.
    """
    current = Path(start_directory).resolve()
    env_file = None

    for folder in (current, *current.parents):
        candidate = folder / ".env"

        if candidate.is_file():
            env_file = candidate
            break

    if env_file is None:
        raise FileNotFoundError(
            f"Could not find .env in {current} or its parents"
        )

    load_dotenv(dotenv_path=env_file, override=False)
    return env_file
