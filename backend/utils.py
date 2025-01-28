from pathlib import Path

def correct_dir(dir: str):
    return dir.strip() != "" and Path(dir).expanduser().is_dir()
