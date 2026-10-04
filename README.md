# guide

A versioned backup of my Claude work. Every commit on `main` is a point in time
you can go back to.

```
artifacts/   claude.ai artifacts (pages, docs, decks, sheets, …), one folder each
designs/     Design artifacts, one folder each
prompts/     every prompt, by day
  claude-code/   logged automatically by the hook in hooks/
  claude-ai/     logged from claude.ai chats
hooks/       Claude Code hook that logs prompts and auto-commits
```

## How it stays in sync

| What | How | When |
|---|---|---|
| Artifacts and designs | A scheduled task exports them and commits to `main` | Every hour (only commits if something changed) |
| Claude Code prompts | `hooks/log_prompt.py` (UserPromptSubmit hook) | On every prompt |
| claude.ai chat prompts | Claude commits them during the chat | Each turn, in chats where it's asked to |

Each artifact folder has a `meta.json` with its title, link and last-updated
time, next to its exported files.

## Install the prompt hook (Claude Code, on your computer)

```sh
git clone https://github.com/judebanger/guide ~/guide
cd ~/guide
python3 hooks/install.py          # adds the hook to ~/.claude/settings.json
```

From then on every prompt in any Claude Code project is appended to
`prompts/claude-code/YYYY-MM-DD.md`, the whole repo is committed, and the commit
is pushed in the background. To keep the clone somewhere else, set
`GUIDE_REPO=/path/to/guide` in your shell, or just run `install.py` from that
clone. Remove it with `python3 hooks/install.py --uninstall`.

## Going back in time

```sh
git log --oneline                       # find the point you want
git log --before="2026-10-04 15:00" -1  # or the last commit before a time
git checkout <commit> -- designs/foo    # restore one folder from then
git revert <commit>                     # undo a specific change
```
