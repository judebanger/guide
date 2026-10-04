#!/usr/bin/env python3
"""Claude Code Stop hook: commit the finished turn to the guide repo.

- commit message: the prompt
- Claude's reply text: artifacts/text/<chat>/...
- PDFs, images, etc. created or changed in the project during the turn: artifacts/<media>/<chat>/...
  (<chat> = claude-code-<project>-<session id>)

Then pushes to origin/main in the background. Prints nothing and always exits 0.
Repo location: $GUIDE_REPO, or the repo this script lives in.
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("GUIDE_REPO") or os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "lib"))

from guide import media_type, push_in_background  # noqa: E402
from turn import record_turn  # noqa: E402

STATE_DIR = os.path.expanduser("~/.cache/guide-hook")
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".next", "dist", "build", ".cache", "target"}
MAX_SCAN = 20000


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text")
    return ""


def last_turn(transcript_path):
    """(prompt, reply) for the most recent real user prompt in the transcript."""
    prompt, replies = "", []
    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                msg = entry.get("message") or {}
                if entry.get("type") == "user" and not entry.get("isMeta"):
                    content = msg.get("content")
                    is_tool_result = isinstance(content, list) and any(
                        isinstance(c, dict) and c.get("type") == "tool_result" for c in content)
                    if not is_tool_result and text_of(content).strip():
                        prompt, replies = text_of(content), []
                elif entry.get("type") == "assistant":
                    t = text_of(msg.get("content"))
                    if t.strip():
                        replies.append(t)
    except OSError:
        pass
    return prompt, "\n\n".join(replies)


def changed_media(cwd, since):
    """Non-text files under cwd modified since the turn started."""
    found, seen = [], 0
    repo = os.path.abspath(REPO)
    for root, dirs, files in os.walk(cwd):
        if os.path.abspath(root).startswith(repo):
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in files:
            seen += 1
            if seen > MAX_SCAN:
                return found
            path = os.path.join(root, name)
            try:
                if os.path.getmtime(path) >= since and media_type(path) != "text":
                    found.append(path)
            except OSError:
                pass
    return found


def main():
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        return
    session = data.get("session_id") or "unknown"
    state_file = os.path.join(STATE_DIR, f"{session}.json")
    state = {}
    if os.path.exists(state_file):
        with open(state_file, encoding="utf-8") as f:
            state = json.load(f)

    t_prompt, reply = last_turn(data.get("transcript_path", ""))
    prompt = state.get("prompt") or t_prompt
    if not prompt.strip():
        return
    cwd = state.get("cwd") or data.get("cwd") or os.getcwd()
    started = state.get("started")
    files = changed_media(cwd, started) if started and os.path.abspath(cwd) != os.path.expanduser("~") else []

    when = datetime.datetime.fromtimestamp(started).astimezone() if started else None
    if record_turn(REPO, prompt, reply, files, source="claude-code",
                   project=os.path.basename(cwd.rstrip("/")), session=session[:8], when=when, base=cwd):
        push_in_background(REPO)
    if os.path.exists(state_file):
        os.remove(state_file)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
