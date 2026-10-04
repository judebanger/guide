#!/usr/bin/env python3
"""Install the guide hooks into your user-level Claude Code settings.

Run once from your clone of the guide repo:

    python3 hooks/install.py

It adds a UserPromptSubmit hook (remembers the prompt) and a Stop hook (commits
the finished turn) to ~/.claude/settings.json, keeping everything already
there, so turns from *every* Claude Code project are recorded here.
Run with --uninstall to remove it.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = {
    "UserPromptSubmit": os.path.join(HERE, "turn_start.py"),
    "Stop": os.path.join(HERE, "turn_end.py"),
}
OURS = ("log_prompt.py", "turn_start.py", "turn_end.py")
SETTINGS = os.path.expanduser("~/.claude/settings.json")


def load():
    if os.path.exists(SETTINGS):
        with open(SETTINGS, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save(settings):
    os.makedirs(os.path.dirname(SETTINGS), exist_ok=True)
    with open(SETTINGS, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")


def strip_ours(groups):
    out = []
    for group in groups:
        hooks = [h for h in group.get("hooks", []) if not any(o in h.get("command", "") for o in OURS)]
        if hooks:
            out.append({**group, "hooks": hooks})
    return out


def main():
    settings = load()
    hooks = settings.setdefault("hooks", {})
    for event, script in HOOKS.items():
        groups = strip_ours(hooks.get(event, []))
        if "--uninstall" not in sys.argv:
            groups.append({"hooks": [{"type": "command", "command": f'python3 "{script}"', "timeout": 30}]})
        if groups:
            hooks[event] = groups
        else:
            hooks.pop(event, None)
    if not hooks:
        settings.pop("hooks", None)
    save(settings)
    print(("Removed" if "--uninstall" in sys.argv else "Installed") + f" guide hooks in {SETTINGS}")


if __name__ == "__main__":
    main()
