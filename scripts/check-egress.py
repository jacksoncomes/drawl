#!/usr/bin/env python3
"""
check-egress — enforce the hard filter mechanically.

The specification permits dialect in exactly one place: a chat message spoken to
the user (SKILL.md section 0). Everything else is plain English, permanently. A
specification that relies on an agent remembering a rule has one point of
failure. This is the second point.

Scans staged changes for voice artifacts and refuses the commit if any are found.

Usage:
    python scripts/check-egress.py            # scan staged diff
    python scripts/check-egress.py --all      # scan the working tree
    python scripts/check-egress.py FILE...    # scan specific files

Install as a hook:
    cp scripts/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

Exit codes:  0 clean   1 egress detected   2 usage error
"""

import argparse
import os
import re
import subprocess
import sys

# ---------------------------------------------------------------------------
# Paths exempt from scanning.
#
# A repository that documents a dialect will contain that dialect. Voice packs,
# lexicons and the specification itself are definitionally full of the thing
# this script detects. Exempting them is not a loophole; scanning them would
# make the check useless on its first run.
# ---------------------------------------------------------------------------
EXEMPT_PREFIXES = (
    "voices/",
    "reference/",
    "scripts/",
    "eval/",
)
EXEMPT_FILES = {
    "SKILL.md",
    "README.md",
    "INSTALL.md",
    "CHANGELOG.md",
}

# Binary and vendored paths nobody wants scanned.
SKIP_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf", ".ico", ".woff", ".woff2",
    ".zip", ".gz", ".tar", ".whl", ".so", ".dll", ".dylib", ".pyc", ".lock",
}
SKIP_DIR = ("node_modules/", ".git/", "venv/", ".venv/", "dist/", "build/")

# ---------------------------------------------------------------------------
# Detectors. Each is (severity, label, compiled pattern).
#
# Ordered by confidence. The dropped-g detector is the highest-yield rule and
# also the one most likely to produce a false positive, so it is scoped to
# words that are unambiguously verbs in this register.
# ---------------------------------------------------------------------------
DROPPED_G = (
    r"\b("
    r"say|runn|check|look|go|com|gett|do|try|wait|talk|noth|someth|anyth|"
    r"fix|be|ridin|work|think|mak|tak|break|push|pull|ship|test|build|"
    r"debugg|pars|load|sav|call|hand|find"
    r")in['’](?![a-z])"
)

DETECTORS = [
    (1, "address term", re.compile(r"\b(cowboy|pardner|partner o' mine|cowpokes?|cowfolk)\b", re.I)),
    (1, "exclamation", re.compile(r"\b(yeehaw|yee-haw|hot damn|hoo boy|much obliged|'preciate it)\b", re.I)),
    (1, "dropped g", re.compile(DROPPED_G, re.I)),
    (1, "dialect contraction", re.compile(r"\b(ain't|reckon|fixin['’]|y'all|outta|gonna|kinda)\b", re.I)),
    (2, "lexicon phrase", re.compile(
        r"\b(catawampus|catywampus|absquatulate|hornswoggle[dr]?|skedaddle|vamoose|"
        r"anti-goglin|snollygoster|exfluncticate|shemozzle|flapdoodle|balderdash|"
        r"poppycock|bodacious|splendiferous|tenderfoot|greenhorn|owlhoot|"
        r"four-flusher|curly wolf|coffee-boiler|bog rider|acorn calf|dogie|"
        r"all hat and no cattle|hard row to hoe|barkin['’] at a knot|"
        r"above snakes|apple-pie order|hair in the butter|acknowledge the corn)\b", re.I)),
    (2, "simile frame", re.compile(
        r"\b(slicker than|crooked as|busier than|slower than|useless as|"
        r"lonely as|restless as|dumber than)\b", re.I)),
]


def is_exempt(path: str) -> bool:
    norm = path.replace(os.sep, "/")
    if norm in EXEMPT_FILES:
        return True
    if any(norm.startswith(p) for p in EXEMPT_PREFIXES):
        return True
    if any(d in norm for d in SKIP_DIR):
        return True
    return os.path.splitext(norm)[1].lower() in SKIP_EXT


def git(*args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args], capture_output=True, text=True, check=True
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def staged_files() -> list:
    out = git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    return [f for f in out.splitlines() if f.strip()]


def tracked_files() -> list:
    out = git("ls-files")
    return [f for f in out.splitlines() if f.strip()]


def scan(path: str) -> list:
    """Return [(lineno, severity, label, text)] for one file."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except (OSError, IsADirectoryError):
        return []

    findings = []
    for n, line in enumerate(lines, 1):
        for sev, label, pat in DETECTORS:
            m = pat.search(line)
            if m:
                findings.append((n, sev, label, m.group(0), line.strip()[:90]))
                break
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True, description=__doc__)
    ap.add_argument("files", nargs="*", help="specific files to scan")
    ap.add_argument("--all", action="store_true", help="scan all tracked files")
    ap.add_argument("--quiet", action="store_true", help="suppress the clean message")
    args = ap.parse_args()

    if args.files:
        targets = args.files
    elif args.all:
        targets = tracked_files()
    else:
        targets = staged_files()

    targets = [f for f in targets if not is_exempt(f) and os.path.isfile(f)]

    if not targets:
        if not args.quiet:
            print("check-egress: nothing to scan.")
        return 0

    total = 0
    for path in sorted(targets):
        found = scan(path)
        if not found:
            continue
        total += len(found)
        print(f"\n{path}")
        for n, sev, label, hit, text in found:
            print(f"  SEV-{sev}  line {n}: {label} -> {hit!r}")
            print(f"           {text}")

    if total:
        print(
            f"\ncheck-egress: {total} voice artifact(s) in {len(targets)} file(s).\n"
            "\n"
            "The hard filter permits dialect only in a chat message spoken to the\n"
            "user. This is not one. See SKILL.md section 0. Strip these and retry.\n"
            "\n"
            "If a hit is a false positive, add the path to EXEMPT_PREFIXES or rephrase\n"
            "the line. Do not disable the hook."
        )
        return 1

    if not args.quiet:
        print(f"check-egress: clean ({len(targets)} file(s) scanned).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
