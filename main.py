#!/usr/bin/env python3
"""Warning Label for Humans: One Line, Big Laugh.

Writes the funniest single-line safety warning label that should come
printed on every human being to /output/entry.txt.

The judge weighs, in order: (1) it is a warning label for humans and
funny, (2) the laugh lands in one read with the turn in the last few
words, (3) it feels true about people in general, (4) it sounds like a
real printed label, (5) it stays inside 160 characters with no filler.

So the program scores a handful of original candidate labels against
those criteria and writes the winner. Deterministic: same winner, same
bytes, every run.
"""

import os

CANDIDATES = [
    "WARNING: This human runs on caffeine, spite, and unread notifications. Do not shake, do not ask how they slept, and never, ever say 'quick question.'",
    "WARNING: Contents may suddenly explain a dream in full detail, reply 'k' to your paragraph, and ask 'are we there yet' as a grown adult.",
    "WARNING: This human will say 'I'm five minutes away' from bed. Do not operate heavy machinery, group chats, or expectations near this unit.",
    "WARNING: Handle with care. This human reads the message, types for nine minutes, then sends 'lol'. Side effects include being left on read.",
]

# Words that make a line read as a real printed safety label.
LABEL_WORDS = ("warning", "do not", "contents", "handle", "side effects")

# Human truths the judge recognises in one read.
RECOGNITION = (
    "caffeine", "unread", "quick question", "left on read",
    "five minutes away", "are we there yet", "reply",
)


def score(line: str) -> float:
    """Score one candidate against the judge's published criteria."""
    low = line.lower()
    points = 0.0
    # 1. It is a warning label for humans, in label wording.
    if low.startswith("warning:"):
        points += 3.0
    if "human" in low or "this unit" in low:
        points += 2.0
    if any(w in low for w in LABEL_WORDS):
        points += 1.0
    # 2. The turn lands in the last few words: the punch sits at the end.
    tail = low.rsplit(".", 1)[-1].strip()
    if any(w in tail for w in ("quick question", "left on read", "grown adult", "expectations")):
        points += 3.0
    # 3. Recognition: true about how humans actually behave.
    points += sum(1.0 for w in RECOGNITION if w in low)
    # 4. Real label rhythm: short imperative clauses.
    points += 0.5 * low.count("do not")
    # 5. Uses the line well: long enough to earn its length, inside 160.
    if 100 <= len(line) <= 160:
        points += 1.0
    if "\n" in line or len(line) > 160:
        points -= 10.0
    return points


def validate(line: str) -> None:
    """Enforce the sealed gate before writing: UTF-8 text, 1 to 160
    characters, not only white space, and a single line."""
    if not isinstance(line, str) or not line.strip():
        raise ValueError("entry must not be empty or only white space")
    line.encode("utf-8")  # raises on non-UTF-8 content
    if len(line) > 160:
        raise ValueError(f"entry is {len(line)} characters, over the 160 cap")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")


def main() -> None:
    winner = max(CANDIDATES, key=score)
    validate(winner)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(winner)


if __name__ == "__main__":
    main()
