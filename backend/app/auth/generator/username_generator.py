# Standalone Username Generator Module
# Place username_prefix.txt and username_suffix.txt in the same folder as this file

import random
import time
import string
from pathlib import Path
from typing import Optional, Callable
from sqlalchemy.orm import Session


# ===== CONFIGURATION =====
PREFIX_FILE = "username_prefix.txt"
SUFFIX_FILE = "username_suffix.txt"


# ===== WORD LIST LOADING =====
def _load_wordlist(filename: str) -> list[str]:
    """
    Load words from a text file in the same directory as this module.
    Each word on a separate line. Capitalizes first letter of each word.
    """
    filepath = Path(__file__).parent / filename
    if not filepath.exists():
        return []
    
    words: list[str] = []
    with filepath.open("r", encoding="utf-8") as f:
        for line in f:
            w = line.strip()
            if w:
                words.append(w[0].upper() + w[1:])
    return words


# Load word lists and digits
PREFIX_WORDS = _load_wordlist(PREFIX_FILE)
SUFFIX_WORDS = _load_wordlist(SUFFIX_FILE)
NUMBER_CHARS = list(string.digits)


def get_username_parts() -> tuple[list[str], list[str], list[str]]:
    """Return the loaded username parts (prefixes, suffixes, digits)."""
    return PREFIX_WORDS, SUFFIX_WORDS, NUMBER_CHARS


# ===== USERNAME GENERATION =====
def _generate_random_username_base() -> str:
    """
    Generates a base username like 'TopDogReptile8907' (without DB uniqueness check).
    
    Format:
    - 1 Prefix word
    - 1–2 Suffix words
    - 3–5 digits
    
    Returns:
        A randomly generated username string.
    """
    parts: list[str] = []

    # Add 1 prefix word
    if PREFIX_WORDS:
        parts.append(random.choice(PREFIX_WORDS))

    # Add 1–2 suffix words
    suffix_count = 1 if len(SUFFIX_WORDS) < 2 else random.randint(1, 2)
    for _ in range(suffix_count):
        if SUFFIX_WORDS:
            parts.append(random.choice(SUFFIX_WORDS))

    # Add 3–5 digits
    digit_count = random.randint(3, 5)
    digits = "".join(random.choice(NUMBER_CHARS) for _ in range(digit_count))

    return "".join(parts) + digits


def _generate_random_username_base() -> str:
    """
    Generates a base username like 'TopDogReptile8907' (without DB uniqueness check).
    
    Format:
    - 1 Prefix word
    - 1–2 Suffix words
    - 3–5 digits
    
    Returns:
        A randomly generated username string.
    """
    parts: list[str] = []

    # Add 1 prefix word
    if PREFIX_WORDS:
        parts.append(random.choice(PREFIX_WORDS))

    # Add 1–2 suffix words
    suffix_count = 1 if len(SUFFIX_WORDS) < 2 else random.randint(1, 2)
    for _ in range(suffix_count):
        if SUFFIX_WORDS:
            parts.append(random.choice(SUFFIX_WORDS))

    # Add 3–5 digits
    digit_count = random.randint(3, 5)
    digits = "".join(random.choice(NUMBER_CHARS) for _ in range(digit_count))

    return "".join(parts) + digits


def generate_unique_username(
    db: Session,
    max_attempts: int = 100
) -> Optional[str]:
    """
    Generate a unique username with database uniqueness check using SQLAlchemy.
    
    Args:
        db: SQLAlchemy session for database queries
        max_attempts: Maximum number of attempts to find a unique username (default: 100)
    
    Returns:
        A unique username string, or None if unable to find one within max_attempts.
    """
    from app.models.user import User
    
    for _ in range(max_attempts):
        candidate = _generate_random_username_base()
        
        # Check if username exists in database using SQLAlchemy
        exists = db.query(User).filter(User.username == candidate).first() is not None
        if not exists:
            return candidate
    
    return None


# ===== SYNCHRONOUS VERSION (if needed) =====
def generate_random_username() -> str:
    """
    Synchronous version: Generate a random username without database check.
    
    Returns:
        A randomly generated username string.
    """
    return _generate_random_username_base()


# ===== EXAMPLE USAGE =====
if __name__ == "__main__":
    # Example 1: Generate random username (no DB check)
    print("Generated username:", generate_random_username())
    print("Generated username:", generate_random_username())
    
    # Example 2: Generate multiple usernames
    print("\nGenerated 5 usernames:")
    for _ in range(5):
        print(f"  - {generate_random_username()}")
