#!/usr/bin/env python3
"""Claude Code UserPromptSubmit hook: remember the prompt and when the turn started.

Nothing is committed here; hooks/turn_end.py does that once Claude has answered.
Prints nothing and always exits 0.
"""
import json
import os
import sys
import time

STATE_DIR = os.path.expanduser("~/.cache/guide-hook")


def main():
    data = json.load(sys.stdin)
    session = data.get("session_id") or "unknown"
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(os.path.join(STATE_DIR, f"{session}.json"), "w", encoding="utf-8") as f:
        json.dump({"prompt": data.get("prompt", ""), "started": time.time(), "cwd": data.get("cwd", "")}, f)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
