"""Domain-specific text normalization for German crossword answers."""

from __future__ import annotations

import re

_ALLOWED_PATTERN = re.compile(r"^[A-Z]+$")


def normalize_answer(raw: str) -> str:
    """Normalize raw answer input according to strict puzzle content rules."""
    if raw is None:
        raise ValueError("Answer is required")

    normalized = (
        raw.strip()
        .replace("Ä", "AE")
        .replace("Ö", "OE")
        .replace("Ü", "UE")
        .replace("ä", "AE")
        .replace("ö", "OE")
        .replace("ü", "UE")
        .replace("ß", "SS")
        .upper()
    )

    if not normalized:
        raise ValueError("Answer cannot be empty")

    if not _ALLOWED_PATTERN.fullmatch(normalized):
        raise ValueError("Answer must only contain uppercase Latin letters")

    return normalized
