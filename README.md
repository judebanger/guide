# guide

A versioned backup of my Claude work. Every commit on `main` is a point in time
you can go back to, and every chat turn is its own commit **whose message is the prompt**.

```
artifacts/
  text/
    <chat>/<date>-<time>-<prompt>.md   one file per turn: the prompt + Claude's reply
    <artifact>-<id>/                   text files of a claude.ai artifact (html, md, json, …) + meta.json
  pdf/   image/   video/   audio/   document/   spreadsheet/   presentation/   archive/   other/
    <chat>/<date>-<time>-<prompt>/…    files produced in that chat turn
    <artifact>-<id>/…                  non-text files of a claude.ai artifact
designs/
  <design>-<id>/                       Design artifacts, kept whole, + meta.json
hooks/   Claude Code hooks that record each turn
site/    builder for the archive website (GitHub Pages)
sync/    scripts used by the hourly artifact sync
lib/     shared helpers        bin/   manual tools        .sync/   sync state
```

`<chat>` is one folder per conversation:
`claude-code-<project>-<session id>` for Claude Code, `claude-ai-<project>-<session id>` for claude.ai.

## How it stays in sync

| What | How | When |
|---|---|---|
| Claude Code turns | `hooks/turn_start.py` + `hooks/turn_end.py` | Every turn, as soon as Claude finishes answering |
| claude.ai chat turns | Claude runs `bin/record_turn.py` | Each turn, in chats where it's asked to |
| claude.ai artifacts and designs | Scheduled task using `sync/` | Hourly. It first compares the artifact list with `.sync/state.json` and stops right there if nothing is new |

Artifacts made in claude.ai can't be filed under a chat folder, because the
artifact list doesn't say which chat made them, so each gets its own folder.

## Install the hooks (Claude Code, on your computer)

```sh
git clone https://github.com/judebanger/guide ~/guide
cd ~/guide
python3 hooks/install.py          # adds both hooks to ~/.claude/settings.json
```

From then on, every turn in any Claude Code project is committed and pushed in
the background: the commit message is your prompt, Claude's reply goes in
`artifacts/text/<chat>/`, and any PDFs, images etc. created or changed in the
project during that turn are copied into `artifacts/<type>/<chat>/`.
To keep the clone elsewhere, set `GUIDE_REPO=/path/to/guide`, or run
`install.py` from that clone. Remove with `python3 hooks/install.py --uninstall`.
Requires `python3` and `git` with push access to this repo.

## Archive website

**https://judebanger.github.io/guide/** — a wayback-style view of this repo,
rebuilt by `.github/workflows/pages.yml` after every push:

- **Timeline**: every prompt and every design backup with its timestamp (in
  your local time), showing live previews of the pages that changed. Open a
  moment for before → after previews of each changed page; the source diffs
  are tucked away at the bottom.
- **Designs**: each design as it looked after every sync, page by page, with
  changed and new pages outlined; step through versions along the top.
- **Files**: every file's change history, linking to the file as it was then.

Build it locally with `python3 site/build.py` (output in `_site/`).

## Going back in time

```sh
git log --oneline                        # every prompt, newest first
git log --grep="sales chart"             # find the turn where you asked something
git log --before="2026-10-04 15:00" -1   # last commit before a time
git checkout <commit> -- designs/foo     # restore one folder from then
git revert <commit>                      # undo a specific change
```
