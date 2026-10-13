#!/usr/bin/env python3
"""Build the "guide archive" static site from this repo's git history.

    python3 site/build.py [out_dir]        (default: _site)

Wayback-style: every commit is a moment in time. Chat turns show the prompt,
Claude's reply and the files changed (with diffs); design syncs show the whole
design as it looked at that moment, page by page. Standard library only.
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

MAX_DIFF_LINES = 1500
MAX_DIFF_BYTES = 400_000


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


def split_diff(sha):
    raw = git("show", "--format=", "--no-color", "--no-renames", "-U3", sha)
    diffs = {}
    for block in re.split(r"(?m)^(?=diff --git )", raw):
        m = re.match(r"diff --git a/(.+?) b/(.+?)\n", block)
        if m:
            diffs[m.group(2)] = block
    return diffs


def render_diff(block):
    if not block:
        return "<p class=muted>No textual diff.</p>"
    if "\nBinary files " in block or "GIT binary patch" in block:
        return "<p class=muted>Binary file.</p>"
    lines = block.split("\n")
    start = next((n for n, l in enumerate(lines) if l.startswith("@@")), len(lines))
    lines = lines[start:]
    cut = ""
    if len(lines) > MAX_DIFF_LINES or len(block) > MAX_DIFF_BYTES:
        cut = f"<p class=muted>Diff truncated ({len(lines)} lines) — see the full file on GitHub.</p>"
        lines = lines[:MAX_DIFF_LINES]
    rows = []
    for l in lines:
        cls = "h" if l.startswith("@@") else "a" if l.startswith("+") else "d" if l.startswith("-") else ""
        rows.append(f'<span class="{cls}">{esc(l)}</span>' if cls else esc(l))
    return "<pre class=diff>" + "\n".join(rows) + "</pre>" + cut


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

def page(title, body, depth=0, active=""):
    up = "../" * depth
    nav = "".join(
        f'<a href="{up}{href}"{" aria-current=page" if key == active else ""}>{label}</a>'
        for key, href, label in (("timeline", "index.html", "Timeline"),
                                 ("designs", "designs.html", "Designs"),
                                 ("files", "files.html", "Files")))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · guide archive</title>
<link rel="stylesheet" href="{up}assets/style.css">
<script defer src="{up}assets/app.js"></script>
</head><body>
<header class=top><a class=brand href="{up}index.html">guide<span>archive</span></a><nav>{nav}</nav>
<a class=gh href="{REPO_URL}">GitHub ↗</a></header>
<main>{body}</main>
<footer>Built from <a href="{REPO_URL}">{esc(REPO_URL.split("github.com/")[-1])}</a>. Times shown in your local time zone; hover for UTC.</footer>
</body></html>"""


def when(iso, cls="t"):
    return f'<time class="{cls}" datetime="{esc(iso)}" title="{esc(iso)}">{esc(iso.replace("T", " ")[:16])}</time>'


IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif"}
TIMELINE_THUMBS = 6


def board_card(b, up, state, small=False):
    """A live, scaled preview of one artboard."""
    src = f'{up}blob/{b["blob"]}.html'
    badge = f' <span class=badge>{state}</span>' if state else ""
    return (f'<figure class="board {state}{" small" if small else ""}" style="--w:{b["w"]};--h:{b["h"]}">'
            f'<a class=frame href="{src}" target=_blank rel=noopener aria-label="Open {esc(b["title"])} full size">'
            f'<iframe loading=lazy src="{src}" title="{esc(b["title"])}" tabindex=-1></iframe></a>'
            f'<figcaption>{esc(b["title"])}{badge}</figcaption></figure>')


def file_card(x, up, small=False):
    src = up + x["src"]
    if x["kind"] == "img":
        inner = f'<img loading=lazy src="{src}" alt="{esc(x["name"])}">'
    else:
        inner = f'<iframe loading=lazy src="{src}" title="{esc(x["name"])}" tabindex=-1></iframe>'
    w, h = (1280, 800) if x["kind"] == "html" else (794, 1123)
    return (f'<figure class="board file-{x["kind"]}{" small" if small else ""}" style="--w:{w};--h:{h}">'
            f'<a class=frame href="{src}" target=_blank rel=noopener>{inner}</a><figcaption>{esc(x["name"])}</figcaption></figure>')


KIND_LABEL = {"turn": "prompt", "sync": "design backup", "change": "repo change"}


# ---------------------------------------------------------------- build

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    for d in ("c", "d", "f", "blob", "assets"):
        os.makedirs(os.path.join(OUT, d))
    shutil.copy(os.path.join(HERE, "style.css"), os.path.join(OUT, "assets", "style.css"))
    shutil.copy(os.path.join(HERE, "app.js"), os.path.join(OUT, "assets", "app.js"))
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    commits = load_commits()
    file_hist = OrderedDict()          # path -> [(commit, status)]
    design_versions = OrderedDict()    # slug -> [dict(commit, title, boards)]
    entries = []

    for c in commits:
        kind, turn_path = classify(c)
        c["kind"] = kind
        c["prompt"], c["response"], c["chat"] = c["subject"], "", ""
        if turn_path:
            meta, prompt, response = parse_turn(git("show", f"{c['sha']}:{turn_path}"))
            c["prompt"] = prompt or c["subject"]
            c["response"] = response
            c["chat"] = turn_path.split("/")[2]
            c["source"] = meta.get("source", "")
            c["date"] = meta.get("time") or c["date"]
        for s, p in c["changes"]:
            file_hist.setdefault(p, []).append((c, s))
        for slug in design_slugs_touched(c):
            title, boards, edited = design_snapshot(c["sha"], slug, os.path.join(OUT, "blob"))
            design_versions.setdefault(slug, []).append(dict(commit=c, title=title, boards=boards, edited=edited))
            c.setdefault("designs", []).append(slug)

    # ---- what each design version changed, page by page
    for slug, versions in design_versions.items():
        for n, v in enumerate(versions):
            prev = versions[n - 1] if n else None
            pb = {b["name"]: b for b in prev["boards"]} if prev else {}
            names = {b["name"] for b in v["boards"]}
            v["delta"] = [("new" if b["name"] not in pb else "changed", b, pb.get(b["name"]))
                          for b in v["boards"] if b["name"] not in pb or pb[b["name"]]["blob"] != b["blob"]]
            v["delta"] += [("removed", None, pb[x]) for x in pb if x not in names]
            v["first"] = prev is None

    # ---- previews of other files (chat outputs, non-design artifacts)
    for c in commits:
        c["files_preview"] = []
        for s, p in c["changes"]:
            if s == "D" or is_noise(p) or p.startswith("designs/"):
                continue
            ext = os.path.splitext(p)[1].lower()
            kind = "img" if ext in IMG_EXT else "pdf" if ext == ".pdf" else "html" if ext in (".html", ".htm") else None
            if not kind:
                continue
            blob = git("rev-parse", f"{c['sha']}:{p}").strip()
            out = os.path.join(OUT, "blob", blob + ext)
            if not os.path.exists(out):
                with open(out, "wb") as f:
                    f.write(git("cat-file", "-p", blob, binary=True))
            c["files_preview"].append(dict(kind=kind, src=f"blob/{blob}{ext}", name=os.path.basename(p), path=p))

    # ---- moment pages
    for n, c in enumerate(commits):
        diffs = split_diff(c["sha"])
        prev_c = commits[n - 1] if n else None
        next_c = commits[n + 1] if n + 1 < len(commits) else None
        prev_a = f'<a href="{prev_c["sha"][:12]}.html">← earlier</a>' if prev_c else "<span></span>"
        next_a = f'<a href="{next_c["sha"][:12]}.html">later →</a>' if next_c else "<span></span>"
        body = [f'<div class=pager>{prev_a}<a href="../index.html#{c["short"]}">timeline</a>{next_a}</div>']
        body.append(f'<p class=meta><span class="kind k-{c["kind"]}">{KIND_LABEL[c["kind"]]}</span> {when(c["date"])}'
                    f'{" · " + esc(c["chat"]) if c["chat"] else ""}</p>')
        if c["kind"] == "turn":
            body.append(f'<section class=prompt><h2>Prompt</h2><div class=md>{markdown(c["prompt"])}</div></section>')
            if c["response"]:
                body.append(f'<details class=reply><summary>Claude\'s reply</summary><div class=md>{markdown(c["response"])}</div></details>')
        else:
            body.append(f'<h1 class=title>{"Design backup" if c["kind"] == "sync" else esc(c["subject"])}</h1>')
        for slug in c.get("designs", []):
            v = next(x for x in design_versions[slug] if x["commit"] is c)
            whole = f'<a href="../d/{slug}/{c["sha"][:12]}.html">whole design at this moment →</a>'
            edited = f' · edited {when(v["edited"])}' if v["edited"] else ""
            body.append(f'<h2 class=dtitle>{esc(v["title"])} <span class=muted>{len(v["boards"])} pages{edited} · {whole}</span></h2>')
            if v["first"]:
                body.append('<p class=muted>First backup of this design.</p><div class=boards>'
                            + "".join(board_card(b, "../", "") for b in v["boards"]) + "</div>")
            elif not v["delta"]:
                body.append('<p class=muted>No visible page changed (only settings or layout of the canvas).</p>')
            else:
                rows = []
                for state, b, old in v["delta"]:
                    if state == "changed":
                        rows.append(f'<div class=pair><div class=side><span class=lbl>before</span>{board_card(old, "../", "")}</div>'
                                    f'<div class=arrow aria-hidden=true>→</div><div class=side><span class=lbl>after</span>{board_card(b, "../", "changed")}</div></div>')
                    elif state == "new":
                        rows.append(f'<div class=pair><div class="side empty"><span class=lbl>before</span><div class=nothing>didn\'t exist</div></div>'
                                    f'<div class=arrow aria-hidden=true>→</div><div class=side><span class=lbl>after</span>{board_card(b, "../", "new")}</div></div>')
                    else:
                        rows.append(f'<div class=pair><div class=side><span class=lbl>before</span>{board_card(old, "../", "removed")}</div>'
                                    f'<div class=arrow aria-hidden=true>→</div><div class="side empty"><span class=lbl>after</span><div class=nothing>removed</div></div></div>')
                counts = {k: sum(1 for x in v["delta"] if x[0] == k) for k in ("changed", "new", "removed")}
                summary = ", ".join(f"{n} {k}" for k, n in counts.items() if n)
                body.append(f'<p class=muted>{summary}</p><div class=pairs>{"".join(rows)}</div>')
        if c["files_preview"]:
            body.append('<h2>Files made</h2><div class=boards>' + "".join(file_card(x, "../") for x in c["files_preview"]) + "</div>")
        ours = [(s, p) for s, p in c["changes"] if not is_noise(p)]
        body.append(f'<details class=source><summary>Source changes · {len(c["changes"])} files</summary>'
                    f'<p class=meta><a href="{REPO_URL}/commit/{c["sha"]}">{c["short"]} on GitHub ↗</a> · '
                    f'<a href="{REPO_URL}/tree/{c["sha"]}">browse repo at this moment ↗</a></p>'
                    + "".join(f'<details class=file><summary><span class="st st-{s}">{s}</span> <span class=path>{esc(p)}</span> '
                              f'<a class=hist href="../f/{page_id(p)}.html">history</a></summary>{render_diff(diffs.get(p, ""))}</details>'
                              for s, p in ours) + "</details>")
        title = (c["prompt"] or c["subject"]).splitlines()[0][:80]
        with open(os.path.join(OUT, "c", c["sha"][:12] + ".html"), "w", encoding="utf-8") as f:
            f.write(page(title, "\n".join(body), 1))

    # ---- design version pages
    design_rows = []
    for slug, versions in design_versions.items():
        os.makedirs(os.path.join(OUT, "d", slug), exist_ok=True)
        for n, v in enumerate(versions):
            c, prev = v["commit"], (versions[n - 1] if n else None)
            prev_blobs = {b["name"]: b["blob"] for b in prev["boards"]} if prev else {}
            cards = []
            for b in v["boards"]:
                state = "" if not prev else ("new" if b["name"] not in prev_blobs else "changed" if prev_blobs[b["name"]] != b["blob"] else "")
                cards.append(board_card(b, "../../", state))
            removed = [x for x in prev_blobs if x not in {b["name"] for b in v["boards"]}] if prev else []
            strip = "".join(
                f'<a href="{x["commit"]["sha"][:12]}.html"{" aria-current=page" if x is v else ""}>{when(x["commit"]["date"], "t short")}</a>'
                for x in versions)
            body = (f'<h1 class=title>{esc(v["title"])}</h1>'
                    f'<p class=meta>Version {n + 1} of {len(versions)} · '
                    + (f'last edited {when(v["edited"])}, backed up {when(c["date"])}' if v["edited"] else f'backed up {when(c["date"])}')
                    + ' · '
                    f'<a href="../../c/{c["sha"][:12]}.html">what changed</a> · <a href="index.html">all versions</a></p>'
                    f'<nav class=wayback aria-label=Versions>{strip}</nav>'
                    + (f'<p class=muted>Removed since previous version: {esc(", ".join(removed))}</p>' if removed else "")
                    + '<div class=boards>' + "".join(cards) + "</div>")
            with open(os.path.join(OUT, "d", slug, c["sha"][:12] + ".html"), "w", encoding="utf-8") as f:
                f.write(page(v["title"], body, 2, "designs"))
        latest = versions[-1]
        items = "".join(
            f'<li><a href="{x["commit"]["sha"][:12]}.html">{when(x["commit"]["date"])}</a> — {len(x["boards"])} pages</li>'
            for x in reversed(versions))
        with open(os.path.join(OUT, "d", slug, "index.html"), "w", encoding="utf-8") as f:
            f.write(page(latest["title"], f'<h1 class=title>{esc(latest["title"])}</h1><p class=meta>{len(versions)} saved versions</p><ul class=versions>{items}</ul>', 2, "designs"))
        b0 = latest["boards"][0] if latest["boards"] else None
        thumb = (f'<span class=thumb style="--w:{b0["w"]};--h:{b0["h"]}"><iframe loading=lazy src="blob/{b0["blob"]}.html" tabindex=-1 title=""></iframe></span>' if b0 else "")
        design_rows.append(f'<a class=designcard href="d/{slug}/{latest["commit"]["sha"][:12]}.html">{thumb}<span><b>{esc(latest["title"])}</b>'
                           f'<br><span class=muted>{len(latest["boards"])} pages · {len(versions)} versions · last {when(latest["commit"]["date"])}</span></span></a>')
    with open(os.path.join(OUT, "designs.html"), "w", encoding="utf-8") as f:
        f.write(page("Designs", '<h1 class=title>Designs</h1><div class=designgrid>' + ("".join(design_rows) or "<p class=muted>No designs yet.</p>") + "</div>", 0, "designs"))

    # ---- file history pages
    tree_rows = []
    for p, hist in sorted(file_hist.items()):
        if is_noise(p):
            continue
        items = "".join(
            f'<li><span class="st st-{s}">{s}</span> {when(c["date"])} <a href="../c/{c["sha"][:12]}.html">{esc((c["prompt"] or c["subject"]).splitlines()[0][:120])}</a>'
            f' · <a href="{REPO_URL}/blob/{c["sha"]}/{p}">file then ↗</a></li>' for c, s in reversed(hist))
        with open(os.path.join(OUT, "f", page_id(p) + ".html"), "w", encoding="utf-8") as f:
            f.write(page(p, f'<h1 class="title path">{esc(p)}</h1><p class=meta>{len(hist)} changes</p><ul class=versions>{items}</ul>', 1, "files"))
        tree_rows.append(f'<li data-q="{esc(p.lower())}"><a href="f/{page_id(p)}.html">{esc(p)}</a> <span class=muted>{len(hist)}× · last {when(hist[-1][0]["date"])}</span></li>')
    with open(os.path.join(OUT, "files.html"), "w", encoding="utf-8") as f:
        f.write(page("Files", '<h1 class=title>Every file, every change</h1><input class=search type=search placeholder="Filter files…" data-filter=".filelist li">'
                     '<ul class="filelist versions">' + "".join(tree_rows) + "</ul>", 0, "files"))

    # ---- timeline (index)
    days = OrderedDict()
    for c in reversed(commits):
        days.setdefault(c["date"][:10], []).append(c)
    cal = OrderedDict()
    for d, cs in days.items():
        cal.setdefault(d[:7], {})[d] = len(cs)
    groups = []
    for d, cs in days.items():
        rows = []
        for c in cs:
            text = (c["prompt"] or c["subject"]).strip()
            first = text.splitlines()[0] if text else ""
            previews = []
            for slug in c.get("designs", []):
                v = next(x for x in design_versions[slug] if x["commit"] is c)
                shown = v["boards"] if v["first"] else [b for st, b, _ in v["delta"] if b]
                states = {} if v["first"] else {b["name"]: st for st, b, _ in v["delta"] if b}
                more = len(shown) - TIMELINE_THUMBS
                cards = "".join(board_card(b, "", states.get(b["name"], ""), small=True) for b in shown[:TIMELINE_THUMBS])
                if more > 0:
                    cards += f'<a class=more href="c/{c["sha"][:12]}.html">+{more} more</a>'
                if v["first"]:
                    what = f'first backup · {len(v["boards"])} pages'
                else:
                    counts = {k: sum(1 for x in v["delta"] if x[0] == k) for k in ("changed", "new", "removed")}
                    what = ", ".join(f"{n} {k}" for k, n in counts.items() if n) or "no visible change"
                previews.append(f'<div class=dprev><a class=dname href="d/{slug}/{c["sha"][:12]}.html">{esc(v["title"])}</a> '
                                f'<span class=muted>{what}</span><div class=strip>{cards}</div></div>')
            if c["files_preview"]:
                previews.append('<div class=strip>' + "".join(file_card(x, "", small=True) for x in c["files_preview"][:TIMELINE_THUMBS]) + "</div>")
            reply = ""
            if c["kind"] == "turn" and c["response"]:
                r = re.sub(r"\s+", " ", re.sub(r"[`*#>|]", "", c["response"])).strip()
                reply = f'<p class=excerpt>{esc(r[:240])}{"…" if len(r) > 240 else ""}</p>'
            heading = (f'<a class=p href="c/{c["sha"][:12]}.html">{esc(first[:300])}</a>' if c["kind"] == "turn"
                       else f'<a class=p href="c/{c["sha"][:12]}.html">{"Design backup" if c["kind"] == "sync" else esc(first[:300])}</a>')
            rows.append(f'<li{" hidden" if c["kind"] == "change" else ""} id="{c["short"]}" class="moment k-{c["kind"]}{" has-prev" if previews else ""}" data-q="{esc(text.lower())} {esc(c["chat"].lower())}" data-kind="{c["kind"]}">'
                        f'<div class=when>{when(c["date"], "t time")}<span class="kind k-{c["kind"]}">{KIND_LABEL[c["kind"]]}</span></div>'
                        f'<div class=what>{heading}{reply}{"".join(previews)}</div></li>')
        groups.append(f'<section class=day id="day-{d}"><h2 class=dayhead>{when(d + "T00:00:00Z", "t date")}</h2><ul class=entries>{"".join(rows)}</ul></section>')
    cal_html = "".join(
        f'<div class=month><b>{m}</b><div class=dots>' + "".join(
            f'<a href="#day-{d}" title="{d}: {n}" style="--n:{min(n, 12)}">{int(d[8:])}</a>' for d, n in sorted(ds.items()))
        + "</div></div>" for m, ds in cal.items())
    kinds = "".join(f'<label><input type=checkbox{"" if k == "change" else " checked"} value="{k}"> {v}</label>' for k, v in KIND_LABEL.items())
    stats = f'{sum(1 for c in commits if c["kind"] == "turn")} prompts · {len(design_versions)} designs · {len(commits)} moments'
    body = (f'<h1 class=title>Timeline</h1><p class=meta>{stats}</p>'
            f'<div class=cal>{cal_html}</div>'
            f'<div class=controls><input class=search type=search placeholder="Search prompts…" data-filter=".entries li"><span class=kinds>{kinds}</span></div>'
            + "".join(groups))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page("Timeline", body, 0, "timeline"))
    print(f"built {len(commits)} commits, {len(design_versions)} designs, {len(file_hist)} files → {OUT}")


if __name__ == "__main__":
    main()
