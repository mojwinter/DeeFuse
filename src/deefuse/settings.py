from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path


DEFAULT_DIR = Path.home() / "Documents" / "Deefuse"
SETTINGS_FILE = DEFAULT_DIR / "settings.json"


@dataclass
class Settings:
    auto_search_on_click: bool = True
    csv_dir: str = str(DEFAULT_DIR)
    target_quality: str = "flac"  # "flac" or "320"


def load_settings() -> Settings:
    DEFAULT_DIR.mkdir(parents=True, exist_ok=True)
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Settings(**{**asdict(Settings()), **data})
        except Exception:
            pass
    return Settings()


def save_settings(settings: Settings) -> None:
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(asdict(settings), f, indent=2)


# Global settings instance loaded at import time
settings = load_settings()
