---
source: cowork
project: guide
session: 01LdZYgu
time: 2026-10-13T03:51:19+00:00
---

## Prompt

Back up my claude.ai artifacts and designs to the GitHub repo judebanger/guide (push straight to main). Work unattended; never ask questions. Check for changes FIRST and stop early if there are none; don't clone or export anything unless something is new.

STEP 1 — cheap check, before touching the repo:
a. Artifact tool: action "list", scope "mine", limit 50 (keep paging while it says there are more). Then action "list" with type "Design" to learn which of those are designs.
b. If I have no artifacts at all, stop here and finish with "no changes".
c. Attach the repo with add_repo (owner "judebanger", repo "guide", access "push"). Do NOT clone yet.
d. Fetch the sync state without cloning: gh api repos/judebanger/guide/contents/.sync/state.json -H "Accept: application/vnd.github.raw" > /tmp/state.json (if it 404s, use an empty file). Fetch the checker the same way: gh api repos/judebanger/guide/contents/sync/needs_sync.py -H "Accept: application/vnd.github.raw" > /tmp/needs_sync.py
e. Write /tmp/listing.json: a JSON array with one object per artifact: {"url", "title", "updated" (the last-updated value exactly as listed), "type" (its type name, or "page"), "design": true/false}.
f. Run: python3 /tmp/needs_sync.py /tmp/listing.json /tmp/state.json. Exit code 3 = nothing new: stop now and finish with "no changes". Exit code 0 = it prints {"changed": [...], "removed": [...]}; continue with only those.

STEP 2 — export only what changed:
a. Clone exactly as add_repo instructed (to /home/claude/guide).
b. For each entry in "changed": create an empty folder /tmp/export/<n>/. Artifact action "read" with its url; save the full page (the saved file the result names) as index.html in that folder. Then Artifact action "list", scope "files", with that url, and fetch every published file with action "read" + "paths" (up to 256 per call) and out_dir set to that folder, so each lands at its published path. Copy files exactly; never summarise or rewrite them.
   Then run from the repo: python3 sync/place.py add --src /tmp/export/<n> --url <url> --title "<title>" --updated "<updated>" --type "<type>" [--design if it is a design]
   (place.py files designs whole under designs/<slug>/, and splits other artifacts by media: text → artifacts/text/<slug>/, pdf/images/etc → artifacts/<media>/<slug>/; it also updates .sync/state.json.)
c. For each id in "removed": python3 sync/place.py remove --id <id>
d. Commit and push: GIT_AUTHOR_NAME=judebanger GIT_AUTHOR_EMAIL=judo-alienate-oaf@duck.com GIT_COMMITTER_NAME=judebanger GIT_COMMITTER_EMAIL=judo-alienate-oaf@duck.com python3 sync/place.py commit
   It pulls with rebase before pushing (the Claude Code hooks also push to this repo). Never force-push.

Finish with one line: what was updated/removed, or "no changes". Never modify or delete anything outside artifacts/<x>/<artifact-slug>/, designs/ and .sync/ (chat folders under artifacts/ belong to the hooks).

## Response

No changes: the one artifact, "Low-FODMAP диета · гайд" (a design, last updated 2026-10-12), already matches the backed-up copy in judebanger/guide. Nothing was cloned, exported or pushed.

The permission check blocked me from running the downloaded `needs_sync.py`, so I read it and ran the same comparison inline.
