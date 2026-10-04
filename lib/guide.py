"""Shared helpers: where things go in the guide repo, and how to commit them."""
import mimetypes
import os
import re
import subprocess

TEXT_EXT = {
    ".txt", ".md", ".markdown", ".rst", ".html", ".htm", ".css", ".js", ".mjs", ".ts", ".tsx", ".jsx",
    ".json", ".jsonl", ".csv", ".tsv", ".xml", ".yaml", ".yml", ".toml", ".ini", ".py", ".sh", ".sql",
    ".svg-src", ".log", ".tex", ".ipynb",
}
TYPE_BY_EXT = {
    ".pdf": "pdf",
    ".svg": "image",
    ".zip": "archive", ".tar": "archive", ".gz": "archive", ".tgz": "archive", ".7z": "archive", ".rar": "archive",
    ".docx": "document", ".doc": "document", ".odt": "document", ".rtf": "document",
    ".xlsx": "spreadsheet", ".xls": "spreadsheet", ".ods": "spreadsheet",
    ".pptx": "presentation", ".ppt": "presentation", ".key": "presentation", ".odp": "presentation",
    ".woff": "font", ".woff2": "font", ".ttf": "font", ".otf": "font",
}


def media_type(path):
    """'text', 'pdf', 'image', 'video', 'audio', 'archive', 'document', ... or 'other'."""
    ext = os.path.splitext(path)[1].lower()
    if ext in TEXT_EXT:
        return "text"
    if ext in TYPE_BY_EXT:
        return TYPE_BY_EXT[ext]
    mime, _ = mimetypes.guess_type(path)
    if mime:
        major = mime.split("/")[0]
        if major in ("image", "video", "audio", "text"):
            return major
    return "other"


def slugify(s, maxlen=48):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return (s[:maxlen].rstrip("-")) or "untitled"


def subject_and_body(prompt):
    """Commit message made from the prompt: first line as subject, the rest as body.
    A first line over 72 chars is kept whole in the body so the full prompt is always there."""
    prompt = prompt.strip() or "(empty prompt)"
    first, _, rest = prompt.partition("\n")
    if len(first) <= 72:
        return first, rest.strip()
    return first[:71] + "…", prompt


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)


def commit(repo, message, paths=None):
    """Stage (paths or everything) and commit. Returns True if a commit was made."""
    git(repo, "add", "-A", *(["--", *paths] if paths else []))
    if git(repo, "diff", "--cached", "--quiet").returncode == 0:
        return False
    result = subprocess.run(["git", "-C", repo, "commit", "-q", "-F", "-"],
                            input=message, text=True, capture_output=True)
    return result.returncode == 0


def push_in_background(repo):
    subprocess.Popen(
        ["sh", "-c", f'cd "{repo}" && git pull -q --rebase origin main; git push -q origin HEAD:main'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True,
    )
