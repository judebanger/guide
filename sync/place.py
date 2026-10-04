#!/usr/bin/env python3
"""Put one exported artifact into the repo, or remove one, and update .sync/state.json.

    python3 sync/place.py add --src DIR --url URL --title T --updated U --type TYPE [--design]
    python3 sync/place.py remove --id ID
    python3 sync/place.py commit                  # commit + push if anything changed

Designs:        designs/<slug>/...                (kept whole)
Other artifacts: text files  -> artifacts/text/<slug>/...
                 everything else -> artifacts/<media>/<slug>/...  (pdf, image, video, ...)
<slug> = title slug + last 8 chars of the artifact id, so renames move the folder.
"""
import argparse
import datetime
import glob
import json
import os
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "lib"))
from guide import commit, media_type, slugify  # noqa: E402

STATE = os.path.join(REPO, ".sync", "state.json")


def load_state():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as f:
            return json.load(f)
    return {"artifacts": {}}


def save_state(state):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
        f.write("\n")


def artifact_id(url):
    return url.rstrip("/").rsplit("/", 1)[-1]


def drop_folders(aid):
    suffix = "-" + aid[-8:]
    for d in glob.glob(os.path.join(REPO, "designs", "*" + suffix)) + glob.glob(os.path.join(REPO, "artifacts", "*", "*" + suffix)):
        if os.path.isdir(d):
            shutil.rmtree(d)


def add(a):
    aid = artifact_id(a.url)
    slug = f"{slugify(a.title)}-{aid[-8:]}"
    drop_folders(aid)
    placed = []
    for root, _, files in os.walk(a.src):
        for name in files:
            src = os.path.join(root, name)
            rel = os.path.relpath(src, a.src)
            if a.design:
                dest = os.path.join(REPO, "designs", slug, rel)
            else:
                dest = os.path.join(REPO, "artifacts", media_type(src), slug, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(src, dest)
            placed.append(os.path.relpath(dest, REPO))
    meta_dir = os.path.join(REPO, "designs" if a.design else os.path.join("artifacts", "text"), slug)
    os.makedirs(meta_dir, exist_ok=True)
    meta = {"title": a.title, "url": a.url, "type": a.type, "updated": a.updated,
            "synced_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "files": sorted(placed)}
    with open(os.path.join(meta_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")
    state = load_state()
    state["artifacts"][aid] = {"title": a.title, "updated": a.updated, "slug": slug, "design": a.design}
    save_state(state)
    print(f"placed {a.title}: {len(placed)} files")


def remove(a):
    drop_folders(a.id)
    state = load_state()
    gone = state["artifacts"].pop(a.id, None)
    save_state(state)
    print(f"removed {gone['title'] if gone else a.id}")


def do_commit(_):
    status = subprocess.run(["git", "-C", REPO, "status", "--porcelain", "--", "artifacts", "designs", ".sync"],
                            capture_output=True, text=True).stdout.strip()
    if not status:
        print("no changes")
        return
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    names = sorted({l[3:].split("/")[-2] if l[3:].count("/") >= 2 else l[3:] for l in status.splitlines()
                    if not l[3:].startswith(".sync")})
    msg = f"sync artifacts ({stamp})\n\n" + "\n".join(f"- {n}" for n in names) + \
          "\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n"
    if commit(REPO, msg, ["artifacts", "designs", ".sync"]):
        subprocess.run(["git", "-C", REPO, "pull", "-q", "--rebase", "origin", "main"])
        r = subprocess.run(["git", "-C", REPO, "push", "-q", "origin", "HEAD:main"], capture_output=True, text=True)
        print("pushed" if r.returncode == 0 else "push failed: " + r.stderr.strip())


p = argparse.ArgumentParser()
sub = p.add_subparsers(dest="cmd", required=True)
pa = sub.add_parser("add")
pa.add_argument("--src", required=True)
pa.add_argument("--url", required=True)
pa.add_argument("--title", required=True)
pa.add_argument("--updated", required=True)
pa.add_argument("--type", default="page")
pa.add_argument("--design", action="store_true")
pr = sub.add_parser("remove")
pr.add_argument("--id", required=True)
sub.add_parser("commit")
args = p.parse_args()
{"add": add, "remove": remove, "commit": do_commit}[args.cmd](args)
