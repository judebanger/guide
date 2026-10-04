#!/usr/bin/env python3
"""Record a turn by hand (used from claude.ai chats, where there are no hooks).

    python3 bin/record_turn.py --prompt-file p.txt --response-file r.md [--file out.pdf ...] [--when ISO] [--push]
"""
import argparse
import datetime
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "lib"))

from guide import push_in_background  # noqa: E402
from turn import record_turn  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--prompt-file", required=True)
ap.add_argument("--response-file", required=True)
ap.add_argument("--file", action="append", default=[])
ap.add_argument("--source", default="claude-ai")
ap.add_argument("--project", default="")
ap.add_argument("--session", default="")
ap.add_argument("--when")
ap.add_argument("--push", action="store_true")
a = ap.parse_args()

read = lambda p: open(p, encoding="utf-8").read()  # noqa: E731
when = datetime.datetime.fromisoformat(a.when) if a.when else None
made = record_turn(REPO, read(a.prompt_file), read(a.response_file), a.file, source=a.source,
                   project=a.project, session=a.session, when=when)
print("committed" if made else "nothing to commit")
if made and a.push:
    push_in_background(REPO)
