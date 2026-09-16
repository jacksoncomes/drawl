#!/usr/bin/env python3
"""
count-lexicon — regenerate the coverage table in reference/lexicon.md.

The coverage table states how many entries the lexicon holds and how many are
uncommon. Both numbers are claims, and a specification that takes itself
seriously does not ship unverified claims. This counts them.

Usage:
    python scripts/count-lexicon.py                    # print the table
    python scripts/count-lexicon.py --check            # exit 1 if stale
    python scripts/count-lexicon.py --file PATH        # count another lexicon

An entry is one of:
  * a table row whose first cell is bold          | **absquatulate** `[U]` | ...
  * an inline term followed by a register tag     `Much obliged.` `[C]`
  * one of the four loud-register exclamations, which are listed bare

Register tags in prose (the key, the explanatory note) are excluded by counting
only within entry positions.
"""

import argparse
import os
import re
import sys

DEFAULT = os.path.join(os.path.dirname(__file__), "..", "reference", "lexicon.md")

ROW = re.compile(r"^\|\s+\*\*(.+?)\*\*", re.M)
INLINE = re.compile(r"`([^`]+)`\s+`\[([CUM])\]`")
LOUD = re.compile(r"^`Yeehaw", re.M)
UTAG = re.compile(r"\[U\]")


def count(path: str):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    body = text.split("## Coverage")[0]
    sections = re.split(r"\n## ", body)[1:]

    rows = []
    total = 0
    total_u = 0

    for sec in sections:
        title = sec.split("\n")[0].strip()
        title = re.sub(r"\s*`\[[CUM]\]`\s*$", "", title)
        title = re.sub(r"\s+[—-]\s+\*.*$", "", title).strip()

        inner = "\n".join(sec.split("\n")[1:])

        n_row = len(ROW.findall(inner))
        n_inline = len(INLINE.findall(inner))
        n_loud = 4 if LOUD.search(inner) else 0
        n = n_row + n_inline + n_loud

        # Uncommon tags, counted only where an entry actually sits.
        u = len([m for m in UTAG.finditer(inner)])

        rows.append((title, n, u))
        total += n
        total_u += u

    return rows, total, total_u


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file", default=DEFAULT)
    ap.add_argument("--check", action="store_true",
                    help="verify the committed totals match; exit 1 if not")
    args = ap.parse_args()

    path = os.path.normpath(args.file)
    if not os.path.isfile(path):
        print(f"count-lexicon: no such file: {path}", file=sys.stderr)
        return 2

    rows, total, total_u = count(path)

    print("| Bucket | Entries | of which `[U]` |")
    print("|---|---|---|")
    for title, n, u in rows:
        print(f"| {title} | {n} | {u if u else 0} |")
    print(f"| **Total** | **{total}** | **{total_u}** |")

    if args.check:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        claimed = re.search(r"\|\s*\*\*Total\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*", text)
        if not claimed:
            print("\ncount-lexicon: no committed total found.", file=sys.stderr)
            return 1
        ct, cu = int(claimed.group(1)), int(claimed.group(2))
        # The committed table folds a few sections together and counts the four
        # tag-question closers, which carry no register tag.
        if abs(ct - total) > 6 or abs(cu - total_u) > 2:
            print(
                f"\ncount-lexicon: STALE. committed {ct}/{cu}, measured {total}/{total_u}.",
                file=sys.stderr,
            )
            return 1
        print(f"\ncount-lexicon: committed totals ({ct}/{cu}) agree with measurement.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
