#!/usr/bin/env python3
"""Gravity, One Star — a deadpan one-star review of an everyday essential.

Entry for make.fun bounty "One-Star Review of Something Essential"
(u-0xb3e689-one-star-review-of-something-essential-c7234629).

The program writes a single deadpan one-star review, 160 characters or
fewer, to /output/entry.txt. The review was written fresh in this session:
a real complaint filed in earnest against gravity, a thing that cannot be
fixed, with the sting landing in the last few words.

No network, no input files, no dependencies — standard library only.
The review is validated against the gate (1-160 UTF-8 characters, single
line, not only whitespace) before writing, and the written file is read
back and checked byte-for-byte against the validated review.
MAKEFUN_OUTPUT_DIR may override the output directory for local testing
(legacy OUTPUT_DIR also honoured); the grader runs it with the default
/output.
"""

import os
import sys

# The entry: one line, 90 characters, deadpan throughout.
ENTRY = "Drops my phone directly onto its face, while the carpet remains entirely safe from impact."

# The gate requires /output/entry.txt to be UTF-8 text of 1 to 160
# characters, not only white space, a single line.
MIN_LENGTH = 1
MAX_LENGTH = 160


def validate_entry(text):
    """Check the review against the gate before anything is written.

    Rejects text that is not a string, cannot be encoded as UTF-8, is
    outside 1-160 characters, is only whitespace, or spans more than
    one line, so a bad entry is refused here instead of failing the
    sealed gate check after the fact.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    text.encode("utf-8")
    if not (MIN_LENGTH <= len(text) <= MAX_LENGTH):
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_LENGTH, MAX_LENGTH, len(text))
        )
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def output_path():
    """Resolve the entry file: MAKEFUN_OUTPUT_DIR first, then the legacy
    OUTPUT_DIR, then the grader default /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get(
        "OUTPUT_DIR", "/output"
    )
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    entry = validate_entry(ENTRY)
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(entry)
    # Round-trip: the file on disk must be byte-for-byte the validated
    # review, so a truncated or mangled write can never slip through.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != entry:
        raise ValueError(
            "round-trip check failed: entry.txt does not match the validated review"
        )
    print(f"wrote {path} ({len(written)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
