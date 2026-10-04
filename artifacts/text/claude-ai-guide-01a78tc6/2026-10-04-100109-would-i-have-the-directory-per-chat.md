---
source: claude-ai
project: guide
session: 01A78tc6
time: 2026-10-04T10:01:09+00:00
---

## Prompt

would I have the directory per chat ?

## Response

Switched to one folder per chat: `artifacts/text/<chat>/<date>-<time>-<prompt>.md` for turns and `artifacts/<media>/<chat>/…` for files made in that chat. `<chat>` looks like `claude-code-myproject-3f9a1c2e` or `claude-ai-guide-01A78tc6`. Artifacts from the hourly sync can't go into chat folders (the listing doesn't say which chat made them), so each gets its own folder.
