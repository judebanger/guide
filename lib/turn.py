"""Record one prompt/response turn in the guide repo and commit it.

One folder per chat, named <source>-<project>-<session>:

    artifacts/text/<chat>/<date>-<time>-<slug>.md          the prompt and Claude's reply
    artifacts/<media>/<chat>/<date>-<time>-<slug>/<file>   PDFs, images, … produced that turn

Commit message = the prompt.
"""
import datetime
import os
import shutil

from guide import commit, media_type, slugify, subject_and_body

MAX_FILE_BYTES = 50 * 1024 * 1024


def record_turn(repo, prompt, response, files=(), source="claude-code", project="", session="", when=None, base=None):
    """files: paths of things produced this turn. Text files are skipped (the reply is the text);
    everything else is copied to artifacts/<media>/<chat>/, keeping its path relative to `base`.
    Returns True if a commit was made."""
    when = when or datetime.datetime.now().astimezone()
    stamp = when.strftime("%Y-%m-%d-%H%M%S")
    slug = slugify(prompt.splitlines()[0] if prompt.strip() else "turn", 40)
    name = f"{stamp}-{slug}"
    chat = "-".join(slugify(x, 32) for x in (source, project, session) if x)

    saved = []
    for src in files:
        if not os.path.isfile(src) or os.path.getsize(src) > MAX_FILE_BYTES:
            continue
        kind = media_type(src)
        if kind == "text":
            continue
        rel = os.path.relpath(src, base) if base and os.path.abspath(src).startswith(os.path.abspath(base) + os.sep) else os.path.basename(src)
        dest = os.path.join(repo, "artifacts", kind, chat, name, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src, dest)
        saved.append(os.path.relpath(dest, repo))

    text_dir = os.path.join(repo, "artifacts", "text", chat)
    os.makedirs(text_dir, exist_ok=True)
    text_path = os.path.join(text_dir, name + ".md")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(f"---\nsource: {source}\nproject: {project}\nsession: {session}\ntime: {when.isoformat(timespec='seconds')}\n")
        if saved:
            f.write("files:\n" + "".join(f"  - {p}\n" for p in saved))
        f.write("---\n\n## Prompt\n\n" + prompt.strip() + "\n\n## Response\n\n" + (response.strip() or "_(no text)_") + "\n")

    subject, body = subject_and_body(prompt)
    trailer = f"Source: {source}" + (f"\nProject: {project}" if project else "") + (f"\nSession: {session}" if session else "")
    message = subject + "\n\n" + (body + "\n\n" if body else "") + trailer + "\n"
    return commit(repo, message, [os.path.relpath(text_path, repo), *saved])
