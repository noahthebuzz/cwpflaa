import json
import logging
from pathlib import Path
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.word import Word

logger = logging.getLogger(__name__)

WORDS_FILE = Path(__file__).parent.parent / "seed_data" / "words.json"


def load_words_from_json() -> list[dict]:
    """Load words from words.json file."""
    if not WORDS_FILE.exists():
        logger.warning(f"Words file not found at {WORDS_FILE}")
        return []
    
    try:
        with open(WORDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not data:
                logger.warning("words.json is empty")
                return []
            logger.info(f"Loaded {len(data)} words from {WORDS_FILE}")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding words.json: {e}")
        return []
    except Exception as e:
        logger.error(f"Error loading words.json: {e}")
        return []


def seed_words(db: Session) -> None:
    """
    Seed the Word table from words.json.
    
    - On first run: Load all words from JSON
    - On subsequent runs: Add new words, remove deleted ones
    - Allows same word with different clues, skips only if both word AND clue are identical
    """
    words_data = load_words_from_json()
    
    if not words_data:
        logger.warning("No words to seed. Skipping seed operation.")
        return
    
    # Remove duplicates from JSON where BOTH word and clue are identical (keep first occurrence)
    seen_pairs = set()
    unique_words_data = []
    for word_data in words_data:
        word_text = word_data["word"]
        word_clue = word_data["clue"]
        pair = (word_text, word_clue)
        
        if pair not in seen_pairs:
            unique_words_data.append(word_data)
            seen_pairs.add(pair)
        else:
            logger.warning(f"Skipping duplicate (word+clue): {word_text} - {word_clue}")
    
    # Get all words currently in the database
    existing_words = {(word.text, word.clue): word for word in db.query(Word).all()}
    incoming_words_set = {(word["word"], word["clue"]) for word in unique_words_data}
    
    # Add or update words from JSON
    added_count = 0
    updated_count = 0
    
    for word_data in unique_words_data:
        word_text = word_data["word"]
        word_clue = word_data["clue"]
        pair = (word_text, word_clue)
        
        if pair in existing_words:
            # Word+clue combo exists, check if elo needs updating
            existing_word = existing_words[pair]
            if existing_word.elo != word_data.get("elo", 1000.0):
                existing_word.elo = word_data.get("elo", 1000.0)
                updated_count += 1
        else:
            # New word+clue combo, add to database
            new_word = Word(
                text=word_text,
                clue=word_clue,
                elo=word_data.get("elo", 1000.0),  # Default to 1000 if not provided
                usage_count=0
            )
            db.add(new_word)
            added_count += 1
    
    # Remove words that are no longer in the JSON file
    removed_count = 0
    for pair, word_obj in existing_words.items():
        if pair not in incoming_words_set:
            db.delete(word_obj)
            removed_count += 1
    
    try:
        db.commit()
        logger.info(f"Seed complete: {added_count} added, {updated_count} updated, {removed_count} removed")
    except Exception as e:
        db.rollback()
        logger.error(f"Error committing seed data: {e}")


def run_seed():
    """Convenience function to run seed in a standalone context."""
    db = SessionLocal()
    try:
        # Check if Word table is empty
        word_count = db.query(Word).count()
        if word_count == 0:
            logger.info("Word table is empty. Starting seed operation...")
            seed_words(db)
        else:
            logger.info(f"Word table already has {word_count} words. Checking for updates...")
            seed_words(db)
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
