#!/usr/bin/env python3
"""One Line, One Laugh: Roast Your Fridge — entry program.

Writes a single roast line to /output/entry.txt. The line is fixed text:
no input, no clock, no randomness, so both grader runs produce the same
bytes. Before writing, the program checks the line against the pinned
character count, byte count and sha256 below, and refuses to write
anything if a check fails.
"""

import hashlib
import os
import sys

# The roast: the fridge's door-open beep, reframed as the appliance
# snitching on a 3am cheese raid to the whole house. Specific detail
# (the beep), twist in the last clause, one line, reads aloud cleanly.
ROAST = (
    "My fridge beeps if the door stays open too long, which is its "
    "polite way of announcing to the whole house that I'm eating "
    "cheese at 3am again."
)

EXPECTED_CHARS = 142
EXPECTED_BYTES = 142
EXPECTED_SHA256 = "251a720e3ab335c34e3e6bd2ead33f8b99e6b6f29c7cf88ca1c0fc3011a1fbad"


def check_entry(data: bytes) -> None:
    """Fail loudly unless the entry bytes are exactly the pinned line."""
    text = data.decode("utf-8")
    if not 1 <= len(text) <= 200:
        print(f"entry is {len(text)} chars, gate needs 1-200", file=sys.stderr)
        sys.exit(1)
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        sys.exit(1)
    if text.strip() == "":
        print("entry must not be only whitespace", file=sys.stderr)
        sys.exit(1)
    if len(text) != EXPECTED_CHARS:
        print(f"entry is {len(text)} chars, expected {EXPECTED_CHARS}", file=sys.stderr)
        sys.exit(1)
    if len(data) != EXPECTED_BYTES:
        print(f"entry is {len(data)} bytes, expected {EXPECTED_BYTES}", file=sys.stderr)
        sys.exit(1)
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        print("entry sha256 does not match the pinned value", file=sys.stderr)
        sys.exit(1)


def verify(path: str, data: bytes) -> None:
    """Read the written file back and fail unless it is byte-for-byte the pinned line."""
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        print("written entry differs from the pinned bytes", file=sys.stderr)
        sys.exit(1)
    if len(written) != EXPECTED_BYTES:
        print(f"written entry is {len(written)} bytes, expected {EXPECTED_BYTES}", file=sys.stderr)
        sys.exit(1)
    if hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        print("written entry sha256 does not match the pinned value", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    data = ROAST.encode("utf-8")
    check_entry(data)
    out = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    verify(out, data)
    print(f"wrote {len(data)} bytes ({len(ROAST)} chars, "
          f"sha256 {hashlib.sha256(data).hexdigest()[:12]}...) to {out}")


if __name__ == "__main__":
    main()
