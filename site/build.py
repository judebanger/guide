#!/usr/bin/env python3
"""Build the "guide archive" static site from this repo's git history.

    python3 site/build.py [out_dir]        (default: _site)

One page per session (a chat, or a design). Each session page has a timeline
along the top; picking a point shows that prompt with the artifacts it made, or,
for a design, the pages as they looked at that backup. Standard library only.
"""
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "_site"))
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_URL = os.environ.get("GUIDE_REPO_URL", "https://github.com/judebanger/guide")

def git(*args, binary=False):
    out = subprocess.run(["git", "-C", ROOT, *args], check=True, capture_output=True).stdout
    return out if binary else out.decode("utf-8", "replace")


def esc(s):
    return html.escape(s or "", quote=True)


def is_noise(path):
    """Files that are vendor/runtime copies, not your work: listed but never diffed."""
    if "__pycache__" in path:
        return True
    m = re.match(r"designs/[^/]+/(.*)$", path)
    if m:
        rest = m.group(1)
        return rest.startswith("artifact-type/") or rest in ("index.html", "SKILL.md")
    return False


def page_id(path):
    return hashlib.sha1(path.encode()).hexdigest()[:12]


# ---------------------------------------------------------------- markdown

def md_inline(s):
    s = esc(s)
    codes = []

    def keep(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    s = re.sub(r"`([^`]+)`", keep, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r'(?<!["=>])(https?://[^\s<]+[^\s<.,;:)])', r'<a href="\1">\1</a>', s)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", s)


def markdown(text):
    lines = (text or "").replace("\r\n", "\n").split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            buf, i = [], i + 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            out.append("<pre><code>" + esc("\n".join(buf)) + "</code></pre>")
            i += 1
            continue
        m = re.match(r"(#{1,6})\s+(.*)", line)
        if m:
            n = min(len(m.group(1)) + 2, 6)
            out.append(f"<h{n}>{md_inline(m.group(2))}</h{n}>")
            i += 1
            continue
        if line.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"\s*\|?\s*:?-+", lines[i + 1]):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], rows[2:]
            t = "<div class=tablewrap><table><thead><tr>" + "".join(f"<th>{md_inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            t += "".join("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in r) + "</tr>" for r in body)
            out.append(t + "</tbody></table></div>")
            continue
        if re.match(r"\s*([-*]|\d+[.)])\s+", line):
            ordered = bool(re.match(r"\s*\d", line))
            items = []
            while i < len(lines) and (re.match(r"\s*([-*]|\d+[.)])\s+", lines[i]) or (lines[i].startswith("  ") and items)):
                if re.match(r"\s*([-*]|\d+[.)])\s+", lines[i]):
                    items.append(re.sub(r"\s*([-*]|\d+[.)])\s+", "", lines[i], count=1))
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{md_inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        if line.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i][1:].lstrip())
                i += 1
            out.append("<blockquote>" + markdown("\n".join(buf)) + "</blockquote>")
            continue
        if not line.strip():
            i += 1
            continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"(```|#{1,6}\s|\s*([-*]|\d+[.)])\s+|>|\s*\|)", lines[i]):
            buf.append(lines[i])
            i += 1
        if not buf:
            buf.append(line)
            i += 1
        out.append("<p>" + "<br>".join(md_inline(b) for b in buf) + "</p>")
    return "\n".join(out)


def parse_turn(text):
    """artifacts/text/<chat>/<…>.md → (frontmatter dict, prompt, response)."""
    meta = {}
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if m:
        for ln in m.group(1).splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    pm = re.search(r"^## Prompt\s*\n(.*?)(?=^## Response\s*$|\Z)", text, re.S | re.M)
    rm = re.search(r"^## Response\s*\n(.*)", text, re.S | re.M)
    return meta, (pm.group(1).strip() if pm else ""), (rm.group(1).strip() if rm else "")


# ---------------------------------------------------------------- history

def load_commits():
    raw = git("log", "--reverse", "--no-renames", "--format=\x01%H\x02%aI\x02%an\x02%s\x02%b\x03", "--name-status")
    commits = []
    for chunk in raw.split("\x01")[1:]:
        head, _, files = chunk.partition("\x03")
        sha, date, author, subject, body = head.split("\x02")
        changes = []
        for ln in files.strip().splitlines():
            parts = ln.split("\t")
            if len(parts) >= 2:
                changes.append((parts[0][0], parts[-1]))
        commits.append(dict(sha=sha, short=sha[:7], date=date, author=author,
                            subject=subject, body=body.strip(), changes=changes))
    return commits


def classify(c):
    turn_files = [p for s, p in c["changes"] if s in "AM" and re.match(r"artifacts/text/(claude-code|claude-ai)-[^/]+/[^/]+\.md$", p)]
    if c["subject"].startswith("sync artifacts"):
        return "sync", None
    if turn_files:
        return "turn", turn_files[0]
    return "change", None


# ---------------------------------------------------------------- designs

def design_slugs_touched(c):
    return sorted({m.group(1) for _, p in c["changes"] for m in [re.match(r"designs/([^/]+)/project/", p)] if m})


def preview_html(src):
    src = src.replace('<script src="./support.js"></script>', "")
    return src


def design_snapshot(sha, slug, blobs_dir):
    """Write each artboard blob once; return (title, [board dicts]) at this commit."""
    prefix = f"designs/{slug}/project/"
    tree = git("ls-tree", "-r", sha, prefix)
    files = {}
    for ln in tree.splitlines():
        meta, path = ln.split("\t", 1)
        _, kind, blob = meta.split()
        files[path[len(prefix):]] = blob
    canvas = {}
    if "canvas.json" in files:
        try:
            canvas = json.loads(git("cat-file", "-p", files["canvas.json"]))
        except Exception:
            canvas = {}
    boards_meta = canvas.get("boards", {})
    order = [n for n in canvas.get("order", []) if n in files] + \
        sorted(n for n in files if n.endswith(".dc.html") and n not in canvas.get("order", []))
    boards = []
    for name in order:
        blob = files[name]
        out = os.path.join(blobs_dir, blob + ".html")
        if not os.path.exists(out):
            with open(out, "w", encoding="utf-8") as f:
                f.write(preview_html(git("cat-file", "-p", blob)))
        bm = boards_meta.get(name, {})
        boards.append(dict(name=name, blob=blob, title=bm.get("title") or name,
                           w=int(bm.get("w") or 794), h=int(bm.get("h") or 1123)))
    title, edited = canvas.get("title") or slug, ""
    try:
        meta = json.loads(git("show", f"{sha}:designs/{slug}/meta.json"))
        title = meta.get("title") or title
        if "T" in str(meta.get("updated", "")):
            edited = meta["updated"]
    except Exception:
        pass
    return title, boards, edited


# ---------------------------------------------------------------- page shell

def page(title, body, depth=0):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · guide archive</title>
<link rel="stylesheet" href="{up}assets/style.css">
<script defer src="{up}assets/app.js"></script>
</head><body>
<header class=top><a class=brand href="{up}index.html">guide<span>archive</span></a>
<a class=gh href="{REPO_URL}">GitHub ↗</a></header>
<main>{body}</main>
<footer>Built from <a href="{REPO_URL}">{esc(REPO_URL.split("github.com/")[-1])}</a>. Times are in your local time zone; hover for UTC.</footer>
</body></html>"""


def when(iso, cls="t"):
    return f'<time class="{cls}" datetime="{esc(iso)}" title="{esc(iso)}">{esc(iso.replace("T", " ")[:16])}</time>'


IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif"}
TEXT_EXT = {".md", ".txt", ".csv", ".json", ".py", ".js", ".ts", ".css", ".yml", ".yaml", ".sh"}


def board_card(b, up, state="", small=False):
    """A live, scaled preview of one design page."""
    src = f'{up}blob/{b["blob"]}.html'
    badge = f' <span class=badge>{state}</span>' if state else ""
    return (f'<figure class="board {state}{" small" if small else ""}" style="--w:{b["w"]};--h:{b["h"]}">'
            f'<a class=frame href="{src}" target=_blank rel=noopener aria-label="Open {esc(b["title"])} full size">'
            f'<iframe loading=lazy src="{src}" title="{esc(b["title"])}" tabindex=-1></iframe></a>'
            f'<figcaption>{esc(b["title"])}{badge}</figcaption></figure>')


def write_blob(sha, path):
    blob = git("rev-parse", f"{sha}:{path}").strip()
    ext = os.path.splitext(path)[1].lower()
    out = os.path.join(OUT, "blob", blob + ext)
    if not os.path.exists(out):
        with open(out, "wb") as f:
            f.write(git("cat-file", "-p", blob, binary=True))
    return f"blob/{blob}{ext}", out


def artifact_card(sha, path, up):
    """Preview of one file a prompt produced."""
    name = os.path.basename(path)
    ext = os.path.splitext(path)[1].lower()
    src, local = write_blob(sha, path)
    src = up + src
    cap = f'<figcaption>{esc(name)} · <a href="{src}" download="{esc(name)}">download</a></figcaption>'
    if ext in IMG_EXT:
        return f'<figure class="art img"><a href="{src}" target=_blank rel=noopener><img loading=lazy src="{src}" alt="{esc(name)}"></a>{cap}</figure>'
    if ext == ".pdf":
        return f'<figure class="art doc"><iframe loading=lazy src="{src}" title="{esc(name)}"></iframe>{cap}</figure>'
    if ext in (".html", ".htm"):
        return (f'<figure class="board art" style="--w:1280;--h:800"><a class=frame href="{src}" target=_blank rel=noopener>'
                f'<iframe loading=lazy src="{src}" title="{esc(name)}" tabindex=-1></iframe></a>{cap}</figure>')
    if ext in TEXT_EXT and os.path.getsize(local) < 300_000:
        text = open(local, encoding="utf-8", errors="replace").read()
        inner = f'<div class=md>{markdown(text)}</div>' if ext == ".md" else f'<pre>{esc(text[:20000])}</pre>'
        return f'<figure class="art text">{inner}{cap}</figure>'
    return f'<figure class="art other"><a class=filebox href="{src}" download="{esc(name)}">{esc(ext.lstrip(".").upper() or "FILE")}</a>{cap}</figure>'


def session_title(prompts):
    first = next((p for p in prompts if p.strip()), "Untitled session")
    first = re.sub(r"\s+", " ", first).strip()
    return first[:90] + ("…" if len(first) > 90 else "")


# ---------------------------------------------------------------- build

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    for d in ("s", "blob", "assets"):
        os.makedirs(os.path.join(OUT, d))
    shutil.copy(os.path.join(HERE, "style.css"), os.path.join(OUT, "assets", "style.css"))
    shutil.copy(os.path.join(HERE, "app.js"), os.path.join(OUT, "assets", "app.js"))
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    sessions = OrderedDict()   # id -> dict(kind, steps, ...)
    for c in load_commits():
        kind, turn_path = classify(c)
        if turn_path:
            chat = turn_path.split("/")[2]
            meta, prompt, response = parse_turn(git("show", f"{c['sha']}:{turn_path}"))
            arts = [p for s, p in c["changes"] if s != "D" and p != turn_path and not is_noise(p)
                    and re.match(rf"artifacts/[^/]+/{re.escape(chat)}/", p)]
            s = sessions.setdefault(chat, dict(kind="chat", id=chat, steps=[],
                                               source="Claude Code" if chat.startswith("claude-code") else "claude.ai"))
            s["steps"].append(dict(sha=c["sha"], date=meta.get("time") or c["date"],
                                   prompt=prompt or c["subject"], response=response, arts=arts))
        for slug in design_slugs_touched(c):
            title, boards, edited = design_snapshot(c["sha"], slug, os.path.join(OUT, "blob"))
            s = sessions.setdefault("design-" + slug, dict(kind="design", id="design-" + slug, steps=[], source="Design"))
            s["title"] = title
            prev = s["steps"][-1] if s["steps"] else None
            pb = {b["name"]: b for b in prev["boards"]} if prev else {}
            names = {b["name"] for b in boards}
            delta = [("new" if b["name"] not in pb else "changed", b, pb.get(b["name"]))
                     for b in boards if b["name"] not in pb or pb[b["name"]]["blob"] != b["blob"]]
            delta += [("removed", None, pb[x]) for x in pb if x not in names]
            s["steps"].append(dict(sha=c["sha"], date=c["date"], edited=edited, boards=boards,
                                   delta=delta, first=prev is None))

    cards = []
    for sid, s in sessions.items():
        steps = s["steps"]
        if s["kind"] == "chat":
            s["title"] = session_title([x["prompt"] for x in steps])
        ticks, panels = [], []
        last_day = None
        for n, st in enumerate(steps):
            day = st["date"][:10]
            if day != last_day:
                ticks.append(f'<li class=daymark>{when(day + "T12:00:00Z", "t day")}</li>')
                last_day = day
            if s["kind"] == "chat":
                label = re.sub(r"\s+", " ", st["prompt"]).strip()
                label = esc(label[:60] + ("…" if len(label) > 60 else ""))
                extra = f'<span class=n>{len(st["arts"])} artifact{"" if len(st["arts"]) == 1 else "s"}</span>' if st["arts"] else ""
            else:
                cnt = {k: sum(1 for x in st["delta"] if x[0] == k) for k in ("changed", "new", "removed")}
                label = "first backup" if st["first"] else (", ".join(f"{v} {k}" for k, v in cnt.items() if v) or "no visible change")
                extra = f'<span class=n>{len(st["boards"])} pages</span>'
            ticks.append(f'<li><button type=button class=tick data-step="{n}" aria-controls="step-{n}">'
                         f'{when(st["date"], "t time")}<span class=lbl>{label}</span>{extra}</button></li>')
            panels.append(render_step(s, n, st))
        latest = steps[-1]
        rng = f'{when(steps[0]["date"])} – {when(latest["date"])}' if len(steps) > 1 else when(latest["date"])
        unit = "prompt" if s["kind"] == "chat" else "version"
        meta = f'{s["source"]} · {len(steps)} {unit}{"" if len(steps) == 1 else "s"} · {rng}'
        body = (f'<p class=crumb><a href="../index.html">← All sessions</a></p>'
                f'<h1 class=title>{esc(s["title"])}</h1><p class=meta>{meta}</p>'
                f'<div class=trackwrap><button type=button class=nav data-dir=-1 aria-label="Earlier">‹</button>'
                f'<ol class=track>{"".join(ticks)}</ol>'
                f'<button type=button class=nav data-dir=1 aria-label="Later">›</button></div>'
                f'<div class=panels data-default="{len(steps) - 1}">{"".join(panels)}</div>')
        with open(os.path.join(OUT, "s", sid + ".html"), "w", encoding="utf-8") as f:
            f.write(page(s["title"], body, 1))

        if s["kind"] == "design" and latest["boards"]:
            b0 = latest["boards"][0]
            thumb = (f'<span class="thumb board" style="--w:{b0["w"]};--h:{b0["h"]}"><span class=frame>'
                     f'<iframe loading=lazy src="blob/{b0["blob"]}.html" tabindex=-1 title=""></iframe></span></span>')
        else:
            first_art = next((p for st in steps for p in st["arts"] if os.path.splitext(p)[1].lower() in IMG_EXT), None)
            thumb = (f'<span class="thumb pic"><img loading=lazy src="{write_blob(next(st["sha"] for st in steps if first_art in st["arts"]), first_art)[0]}" alt=""></span>'
                     if first_art else f'<span class="thumb chat" aria-hidden=true>{len(steps)}</span>')
        cards.append((latest["date"], f'<a class=session href="s/{sid}.html">{thumb}<span class=info>'
                                      f'<span class="src src-{s["kind"]}">{s["source"]}</span>'
                                      f'<b>{esc(s["title"])}</b><span class=muted>{len(steps)} {unit}{"" if len(steps) == 1 else "s"} · last {when(latest["date"])}</span>'
                                      f'</span></a>'))

    cards.sort(key=lambda x: x[0], reverse=True)
    body = ('<h1 class=title>Sessions</h1><p class=meta>Chats and designs, newest first. Open one to step through it.</p>'
            '<input class=search type=search placeholder="Filter sessions…" data-filter=".sessions .session">'
            '<div class=sessions>' + ("".join(c for _, c in cards) or "<p class=muted>Nothing recorded yet.</p>") + "</div>")
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page("Sessions", body, 0))
    print(f"built {len(sessions)} sessions → {OUT}")


def render_step(s, n, st):
    up = "../"
    src = f'<a class=srclink href="{REPO_URL}/commit/{st["sha"]}">source ↗</a>'
    if s["kind"] == "chat":
        out = [f'<p class=meta>{when(st["date"])} · prompt {n + 1} of {len(s["steps"])} · {src}</p>',
               f'<section class=prompt><div class=md>{markdown(st["prompt"])}</div></section>']
        if st["arts"]:
            out.append(f'<h2>Artifacts from this prompt</h2><div class=arts>'
                       + "".join(artifact_card(st["sha"], p, up) for p in st["arts"]) + "</div>")
        else:
            out.append('<p class=muted>No artifacts were made in this prompt.</p>')
        if st["response"]:
            out.append(f'<details class=reply><summary>Claude\'s reply</summary><div class=md>{markdown(st["response"])}</div></details>')
    else:
        edited = f'edited {when(st["edited"])} · backed up {when(st["date"])}' if st["edited"] else f'backed up {when(st["date"])}'
        out = [f'<p class=meta>Version {n + 1} of {len(s["steps"])} · {edited} · {src}</p>']
        if st["first"]:
            out.append(f'<h2>All {len(st["boards"])} pages</h2><div class=boards>'
                       + "".join(board_card(b, up) for b in st["boards"]) + "</div>")
        else:
            if st["delta"]:
                cnt = {k: sum(1 for x in st["delta"] if x[0] == k) for k in ("changed", "new", "removed")}
                out.append(f'<h2>What changed <span class=muted>{", ".join(f"{v} {k}" for k, v in cnt.items() if v)}</span></h2><div class=pairs>')
                for state, b, old in st["delta"]:
                    before = board_card(old, up, "removed" if state == "removed" else "") if old else '<div class=nothing>didn\'t exist</div>'
                    after = board_card(b, up, state) if b else '<div class=nothing>removed</div>'
                    out.append(f'<div class=pair><div class=side><span class=lbl>before</span>{before}</div>'
                               f'<div class=arrow aria-hidden=true>→</div><div class=side><span class=lbl>after</span>{after}</div></div>')
                out.append("</div>")
            else:
                out.append('<p class=muted>No page changed in this backup (only canvas settings).</p>')
            out.append(f'<details class=allpages><summary>All {len(st["boards"])} pages at this point</summary><div class=boards>'
                       + "".join(board_card(b, up) for b in st["boards"]) + "</div></details>")
    return f'<section class=step id="step-{n}" data-step="{n}" hidden>{"".join(out)}</section>'


if __name__ == "__main__":
    main()
