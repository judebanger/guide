---
source: cowork
project: guide
session: 01LdZYgu
time: 2026-10-13T05:04:46+00:00
---

## Prompt

something not fun - i need the artifact preview + timeline, not md changes

## Response

I rebuilt the site around previews: the timeline now shows the pages themselves, and the markdown/code changes are tucked away. It's live at https://judebanger.github.io/guide/ and the deploy succeeded.

- **Timeline:** each entry is a prompt or a design backup with its time. Backups show small live previews of the pages that changed: blue outline for new pages, green for changed ones, and "+N more" when there are more than six. The first backup shows the whole design.
- **Opening an entry:** you get each changed page as **before → after**, side by side, with "didn't exist" or "removed" where that applies. Claude's reply is folded away, and the code changes sit closed at the very bottom.
- **Hidden by default:** the site's own setup commits, like the ones I just made. Tick **repo change** to show them.
- **Design tab:** unchanged. It still has every saved version with a time bar to step through.

The 04:52 backup shows up as 23 changed and 16 new pages, which is your 04:39 edit.

The previews are drawn straight from each page's saved file, not by claude.ai's editor. Your pages are plain enough that they match the real thing in my checks. A page that later uses images or editor features might look slightly off there.
