import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Bad-word list — loaded once at module import time.
# You can replace this with a file-based dictionary:
#   BAD_WORDS = set(Path("bad_words.txt").read_text().splitlines())
# ---------------------------------------------------------------------------
BAD_WORDS: set[str] = {
    "badword1", "badword2", "offensive", "slur",
    # Add your actual bad-word list here
}


def contains_bad_words(text: str) -> bool:
    """
    Returns True if the text contains any word from the bad-word dictionary.
    Matching is case-insensitive and word-boundary aware.
    """
    text_lower = text.lower()
    for word in BAD_WORDS:
        # Use word boundaries so 'ass' doesn't flag 'class'
        if re.search(rf"\b{re.escape(word)}\b", text_lower):
            return True
    return False


def load_bad_words_from_file(filepath: str) -> None:
    """
    Utility to reload the bad-word set from a text file (one word per line).
    Call this at startup if you maintain an external dictionary.
    """
    global BAD_WORDS
    path = Path(filepath)
    if path.exists():
        BAD_WORDS = set(path.read_text(encoding="utf-8").splitlines())