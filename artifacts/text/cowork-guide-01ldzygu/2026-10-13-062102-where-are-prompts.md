---
source: cowork
project: guide
session: 01LdZYgu
time: 2026-10-13T06:21:02+00:00
---

## Prompt

where are prompts?

## Response

The site only shows prompts that have been saved into the repo, and so far that's 10: the ones from your first setup chat on Oct 4. They're in the session titled "can I sync all my work here with gh ?". Click a point on its timeline to see each one.

Two sets of prompts are missing:

- **The chat where you edited the FODMAP design.** Backing up an artifact only copies its files. claude.ai doesn't record which chat made an artifact or what was asked, so the design shows up as its own session with versions and no prompts.
- **This conversation and other claude.ai chats.** Only Claude Code saves prompts automatically, through the hooks. In claude.ai chats, a prompt is saved only when Claude is asked to run `bin/record_turn.py` for each turn, and nobody has asked that since the first chat.

What I can do:

1. **Backfill this conversation now.** I have all your prompts here with their replies, so I can add them as a session with the right timestamps.
2. **Record every claude.ai chat in this Project from now on.** You'd add one line to the Project's custom instructions, something like: "After each reply, record the turn to judebanger/guide with bin/record_turn.py." I can't edit those instructions myself, but I can write the exact line for you.
3. **Add the FODMAP design chat's prompts.** I can't open other chats from here. If you paste them in or open that chat and ask it to record itself, they'll appear on the site. I can put them on the same timeline as the design versions so you can see which prompt led to which change.

Keep in mind the repo is public now, so anything recorded is visible to everyone. Should I start with backfilling this conversation?
