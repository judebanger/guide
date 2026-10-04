#!/usr/bin/env python3
"""Install the prompt-logging hook into your user-level Claude Code settings.

Run once from your clone of the guide repo:

    python3 hooks/install.py

It adds a UserPromptSubmit hook to ~/.claude/settings.json (keeping everything
already there), so prompts from *every* Claude Code project are logged here.
Run with --uninstall to remove it.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "log_prompt.py")
COMMAND = f'python3 "{SCRIPT}"'
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
        hooks = [h for h in group.get("hooks", []) if "log_prompt.py" not in h.get("command", "")]
        if hooks:
            out.append({**group, "hooks": hooks})
    return out


def main():
    settings = load()
    hooks = settings.setdefault("hooks", {})
    groups = strip_ours(hooks.get("UserPromptSubmit", []))
    if "--uninstall" not in sys.argv:
        groups.append({"hooks": [{"type": "command", "command": COMMAND, "timeout": 15}]})
    if groups:
        hooks["UserPromptSubmit"] = groups
    else:
        hooks.pop("UserPromptSubmit", None)
    if not hooks:
        settings.pop("hooks", None)
    save(settings)
    print(("Removed" if "--uninstall" in sys.argv else "Installed") + f" prompt hook in {SETTINGS}")


if __name__ == "__main__":
    main()
