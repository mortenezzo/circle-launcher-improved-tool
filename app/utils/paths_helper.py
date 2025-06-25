import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def get_rainmeter_skins_path() -> Path:
    """
    Get the Rainmeter skins path from the environment variable or default to the user's directory.

    :return: Path to the Rainmeter skins directory.
    """
    skins_path = os.getenv("RAINMETER_SKINS_PATH")

    if skins_path:
        return Path(skins_path).resolve()

    user_path = Path(os.environ.get("USERPROFILE", ""))

    for folder in ["Documents", "Documentos"]:
        if (user_path / folder).exists():
            user_path = user_path / folder / "Rainmeter" / "Skins"
            break

    return Path(user_path / "Documents" / "Rainmeter" / "Skins").resolve()