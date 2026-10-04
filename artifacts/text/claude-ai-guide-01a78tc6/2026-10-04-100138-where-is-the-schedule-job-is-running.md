---
source: claude-ai
project: guide
session: 01A78tc6
time: 2026-10-04T10:01:38+00:00
---

## Prompt

where is the schedule job is running ?

## Response

In Anthropic's cloud, not on your computer. Each hourly run (at :50) starts a fresh cloud session in the same kind of private Linux workspace this chat uses, does the check/sync, and is then thrown away. It never touches your machine (the task isn't set to require your computer), so it runs even when your computer is off. Each run shows up as its own session in your list of scheduled tasks, where you can open it, see its output, pause it, or run it now. Task id: trig_01JxAjFKFe6JLmEfCrqFsxsC. The Claude Code hooks are the only part that runs on your computer.
