---
title: "The Claude setup package lives in its own private repo, so its visuals have to be in the README itself"
author: Tkrudrn-lab
date: 2026-11-15
branch: main
cost: { minutes: 30, tokens: 183296 }
id: l-d0b5284a
scope: repo
status: active
src: agent
touches:
  - CLAUDE.md
  - platform/CLAUDE.md
  - platform/Claude_Setup.md
  - platform/jobs/gemini.env.example
  - platform/jobs/gemini.py
  - platform/jobs/test_jobs.py
  - platform/ogai.sh
---

## Decided
- The setup package that goes out to other people now lives in its own private GitHub repo (tkrudrn-lab/claude-setup). The working copy sits inside hermes as a separate git repo. hermes ignores it through .git/info/exclude, not .gitignore, so the two histories never mix. Edits happen in that folder and get committed and pushed to that repo.
- The user chose private over public. A private repo gets no free GitHub Pages, so the interactive bible can't be hosted as a page. The README carries the visuals: a Mermaid flowchart, which GitHub renders, and five PNG crops of the bible.
- The bible stays as an HTML appendix inside the single setup MD, so handing someone one file still works. There is no separate bible.html in the repo.
- Every new tool follows the repo's ADDING checklist: feature card, nine places to edit, a JS syntax check, and a "recent additions" card in the README.

## Tried and ruled out
- A public repo with GitHub Pages hosting the bible. The user declined because it would make the package public.
- A CLAUDE.md inside the package repo for maintainer rules. Anyone who clones it and opens Claude Code there would load maintainer instructions on top of the setup flow. The rules went into ADDING.md instead, and the hermes router points to it.

## Watch out
- Headless Edge screenshots fail without any message when the window is taller than about 9,000px (14,000 produced no file).
- When rewriting a file in Python, read it fully before opening it for writing. `open(p,'wb').write(f(open(p,'rb').read()))` truncates the file first. That emptied the root router once in this session, and it had to be rebuilt from HEAD plus the uncommitted lines.
- The preview browser isn't signed in to GitHub, so private repo pages come back 404 there. Check the README rendering with `gh api markdown` instead.

In the code: claude-setup/README.md, claude-setup/ADDING.md, claude-setup/images/01..05-*.png, hermes .git/info/exclude, router rows in CLAUDE.md and platform/CLAUDE.md
