from __future__ import annotations

import os
from .settings import settings, Settings

# ── FILE & PATHS ────────────────────────────────────────────────────────
SKIPPED_CSV = ""
MATCHED_CSV = ""
DOWNLOAD_PATH = None  # None ⇒ uses the default deemix download folder

# ── DEEMIX & API SETTINGS ───────────────────────────────────────────────
DEEMIX_CLI = "deemix"
BITRATES_PREFER = []
DEEZER_API_URL = "https://api.deezer.com/search"

# ── SCANNING & MATCHING ─────────────────────────────────────────────────
SUPPORTED_EXTENSIONS = [".flac", ".mp3", ".m4a"]
DURATION_TOLERANCE_SEC = 10

# ── CSV HEADERS ─────────────────────────────────────────────────────────
SKIP_HDR = ["Track", "Artist", "Album", "Duration"]
MATCH_HDR = [
    "Local Track", "Local Artist", "Local Album", "Local Duration",
    "Deezer Track", "Deezer Artist", "Deezer Album", "Deezer Duration",
    "Deezer URL",
]


def reload_settings(s: Settings = settings) -> None:
    """Update module globals based on stored settings."""
    global SKIPPED_CSV, MATCHED_CSV, BITRATES_PREFER
    csv_dir = os.path.expanduser(s.csv_dir)
    os.makedirs(csv_dir, exist_ok=True)
    SKIPPED_CSV = os.path.join(csv_dir, "skipped_tracks.csv")
    MATCHED_CSV = os.path.join(csv_dir, "matched_tracks.csv")
    if s.target_quality == "flac":
        BITRATES_PREFER[:] = ["flac", "320"]
    else:
        BITRATES_PREFER[:] = ["320"]


reload_settings()
