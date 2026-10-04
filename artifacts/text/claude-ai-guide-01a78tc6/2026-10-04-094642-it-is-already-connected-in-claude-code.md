---
source: claude-ai
project: guide
session: 01A78tc6
time: 2026-10-04T09:46:42+00:00
---

## Prompt

it is already connected in claude code

## Response

That explains it. Claude Code on your computer uses your own local `gh` login. This session runs in the cloud and reaches GitHub through the Claude GitHub App on claude.ai, which needs its own permission. That app currently can't see any of your repos, including `judebanger/guide`.

To fix it for this session: github.com → Settings → Applications → Installed GitHub Apps → Claude → Configure → add `guide` (or connect GitHub under claude.ai Settings → Connectors). Then say "done".

Or skip this for now: your local Claude Code already has GitHub access, so I can write the hook files for you to drop into your repo.

_(backfilled from the chat on 2026-10-04)_
