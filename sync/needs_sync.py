#!/usr/bin/env python3
"""Decide whether the artifact sync has anything to do, before cloning or exporting.

    python3 needs_sync.py <listing.json> [<state.json>]

listing.json: the current artifacts, [{"url", "title", "updated", "type", "design": bool}, ...]
state.json:   the repo's .sync/state.json (missing or empty file = nothing synced yet)

Prints {"changed": [...listing entries...], "removed": [...ids...]} and exits
0 if there is work to do, 3 if nothing changed.
Standalone on purpose: runs before the repo is cloned.
"""
import json
import os
import sys


def artifact_id(url):
    return url.rstrip("/").rsplit("/", 1)[-1]


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        listing = json.load(f)
    state = {}
    if len(sys.argv) > 2 and os.path.exists(sys.argv[2]) and os.path.getsize(sys.argv[2]):
        with open(sys.argv[2], encoding="utf-8") as f:
            state = json.load(f).get("artifacts", {})

    current = {artifact_id(a["url"]): a for a in listing}
    changed = [a for i, a in current.items()
               if i not in state or state[i].get("updated") != a.get("updated") or state[i].get("title") != a.get("title")]
    removed = [i for i in state if i not in current]
    print(json.dumps({"changed": changed, "removed": removed}, indent=2))
    sys.exit(0 if changed or removed else 3)


if __name__ == "__main__":
    main()
