#!/usr/bin/env python3
"""One Word, First Thought — entry program (program/v1).

Reads the single entered word from word.txt (shipped beside this file)
and writes it, unchanged, to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR).
The file the gate reads holds the word and nothing else: no newline,
no decoration — the competition enters exactly one word.
"""

import os
from pathlib import Path

WORD_FILE = Path(__file__).resolve().parent / "word.txt"
MAX_CHARS = 24  # the gate's cap for /output/entry.txt


def load_word() -> str:
    """Read the entered word and hold it to the gate before writing.

    The competition enters exactly one word: strict UTF-8, 1-24
    characters, and no white space anywhere — a stray newline in
    word.txt would hand the judge more than the word, so refuse it
    instead of quietly shipping an entry that is not one word.
    """
    raw = WORD_FILE.read_bytes()
    word = raw.decode("utf-8")  # strict: invalid bytes raise
    if not 1 <= len(word) <= MAX_CHARS:
        raise ValueError(f"word must be 1-{MAX_CHARS} characters, got {len(word)}")
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must be exactly one word, with no white space")
    return word


def main() -> None:
    word = load_word()
    data = word.encode("utf-8")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    tmp = out_dir / ".entry.txt.tmp"
    tmp.write_bytes(data)
    os.replace(tmp, target)  # atomic: the gate never sees a partial file
    if target.read_bytes() != data:
        raise IOError("entry.txt does not match the word byte for byte")


if __name__ == "__main__":
    main()
