---
source: claude-ai
project: guide
session: 01A78tc6
time: 2026-10-04T09:46:40+00:00
---

## Prompt

all the artefacts, any design session, push straifht to main, artifacts to the separate dir, theh design into the own, and every prompt as well, so i can revert back to any point in time

maybe instead of schedule we can run a hook

## Response

Hooks don't exist in this chat; they're a Claude Code feature, so nothing here can fire automatically on every prompt. Here's what's possible:

**Artifacts and designs: a scheduled task.** It can run as often as hourly. Each run exports every artifact and design and pushes straight to `main` (`artifacts/<name>/`, `designs/<name>/`). Each run is one commit, so you can roll back to any hour.

**Prompts: the tricky part.** A scheduled run starts fresh and can't read your chat history, so it can't capture prompts. Two ways around it:

- **In this conversation:** I can commit a `prompts/` log entry plus a snapshot of whatever changed at the end of each turn. That gives you a true point-in-time history, but only for chats where I'm doing it.
- **Claude Code on your computer:** that's where real hooks live. A `UserPromptSubmit` hook can log every prompt and auto-commit, which matches what you described. I can write that hook config and script for you.

A sensible setup would be the hourly scheduled task for artifacts and designs, the hook if you use Claude Code, and per-turn commits here.

What's the repo (`owner/repo`)? Once I have it, I'll attach it, set up the folder structure and create the scheduled task.

_(backfilled from the chat on 2026-10-04)_
