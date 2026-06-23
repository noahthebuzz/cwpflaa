import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.data import func

MAX_ATTEMPTS = 10


def _generate_random_username_base() -> str:
    parts: list[str] = []
    PREFIX_WORDS, SUFFIX_WORDS, NUMBER_CHARS = func.get_username_parts()

    if PREFIX_WORDS:
        parts.append(random.choice(PREFIX_WORDS))

    suffix_count = 1 if len(SUFFIX_WORDS) < 2 else random.randint(1, 2)
    for _ in range(suffix_count):
        if SUFFIX_WORDS:
            parts.append(random.choice(SUFFIX_WORDS))

    digit_count = random.randint(3, 5)
    digits = "".join(random.choice(NUMBER_CHARS) for _ in range(digit_count))

    return "".join(parts) + digits


async def generate_unique_username(db: AsyncSession) -> str:
    for _ in range(MAX_ATTEMPTS):
        candidate = _generate_random_username_base()
        result = await db.execute(
            select(User.username).where(User.username == candidate).limit(1)
        )
        if result.scalar_one_or_none() is None:
            return candidate

    raise RuntimeError(f"Could not generate unique username after {MAX_ATTEMPTS} attempts.")
