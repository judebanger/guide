#!/usr/bin/env python3
"""Claude Code UserPromptSubmit hook.

Appends every prompt to prompts/YYYY-MM-DD.md in the guide repo, commits
everything that changed (so each prompt is a point in time you can revert to)
and pushes to origin/main in the background so the prompt is never delayed.

Repo location: $GUIDE_REPO if set, otherwise the repo this script lives in.
Prints nothing and always exits 0, so it can never block a prompt.
"""
import datetime
import json
import os
import subprocess
import sys

REPO = os.environ.get("GUIDE_REPO") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def git(*args, check=False):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True, check=check)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    prompt = (data.get("prompt") or "").rstrip()
    if not prompt:
        return

    now = datetime.datetime.now().astimezone()
    session = data.get("session_id", "unknown")
    cwd = data.get("cwd", "")
    project = os.path.basename(cwd.rstrip("/")) if cwd else "?"

    log_dir = os.path.join(REPO, "prompts", "claude-code")
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, now.strftime("%Y-%m-%d") + ".md")
    new_file = not os.path.exists(path)
    with open(path, "a", encoding="utf-8") as f:
        if new_file:
            f.write(f"# Claude Code prompts, {now:%Y-%m-%d}\n")
        f.write(f"\n## {now:%H:%M:%S %z} · {project} · session `{session[:8]}`\n\n")
        f.write(f"`cwd: {cwd}`\n\n")
        f.write(prompt + "\n")

    first_line = prompt.splitlines()[0][:60]
    git("add", "-A")
    git("commit", "-q", "-m", f"prompt ({project}): {first_line}")

    # Push without waiting; rebase first in case the scheduled sync pushed meanwhile.
    subprocess.Popen(
        ["sh", "-c", f'cd "{REPO}" && git pull -q --rebase origin main; git push -q origin HEAD:main'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
