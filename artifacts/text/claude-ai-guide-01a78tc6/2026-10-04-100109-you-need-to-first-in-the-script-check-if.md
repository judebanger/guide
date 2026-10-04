---
source: claude-ai
project: guide
session: 01A78tc6
time: 2026-10-04T10:01:09+00:00
---

## Prompt

you need to first in the script check if there was a something new and only then sync

what you are doing is 

* commit message contains the promt
* any resulted text goes into artifacts/text
* any pdf/image/etc except text goes to artifcats/%type of media%

## Response

Restructured the repo around those rules:

- **Commit message = the prompt.** Every turn is its own commit (first line as subject, the rest as body), so `git log` reads as your prompt history and `git log --grep` finds any turn.
- **Reply text → `artifacts/text/<chat>/<date>-<time>-<prompt>.md`** (prompt + Claude's reply).
- **PDFs, images, video, etc. → `artifacts/<media type>/<chat>/…`**, sorted automatically by file type.
- **One folder per chat**: `claude-code-<project>-<session>` or `claude-ai-<project>-<session>`.
- **Hourly artifact sync checks first**: it compares the artifact list with `.sync/state.json` (fetched without cloning) and stops immediately if nothing is new; only changed artifacts are exported. Designs stay whole in `designs/`; other artifacts are split into `artifacts/text/<artifact>/` and `artifacts/<media>/<artifact>/`.
- **Claude Code hooks**: `turn_start.py` (UserPromptSubmit) remembers the prompt, `turn_end.py` (Stop) commits the finished turn with the reply and any media files the turn created. Install: `python3 hooks/install.py`.
- Old `prompts/` folder removed; this chat's earlier turns were backfilled in the new format.
