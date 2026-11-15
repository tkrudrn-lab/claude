---
title: "Gemini API key lives outside the repo, and the helper uses the Interactions API, not generateContent"
author: Tkrudrn-lab
date: 2026-11-14
branch: main
cost: { minutes: 8, tokens: 69013 }
id: l-c621656b
scope: repo
status: active
src: agent
touches:
  - platform/jobs/gemini.py
  - platform/jobs/gemini.env.example
  - platform/jobs/test_jobs.py
  - platform/CLAUDE.md
  - platform/jobs/common.py
---

## Decided
- The Gemini guide (sambutlerai PDF) says to put GEMINI_API_KEY in a project .env. This repo lives in OneDrive, so a .env here would sync to the cloud. The key goes in ~/.config/hermes/gemini.env instead, the same place as telegram.env and paths.env, and is read through common.load_env. A GEMINI_API_KEY environment variable wins if it is set.
- As of 2026-11, Google's docs (ai.google.dev now redirects to aistudio.google.com/docs) show only client.interactions.create for images, TTS, video, search and URL context. The helper follows that. The input block shapes, response_format, and output_image / output_audio / output_text come from those docs.

## Watch out
- The gemini-2.5-* models are deprecated and get rerouted to other models on 2026-12-01. Don't copy 2.5 model names from older tutorials.
- The defaults (gemini-4-hydrogen, gemini-nano-banana-2.1, gemini-3.8-flash-tts) were taken from the docs on 2026-11-14. They were not confirmed against a live key; run `python gemini.py models` first.
- `python -I` hides the user site-packages, where google-genai is installed on this laptop.

In the code: platform/jobs/gemini.py, platform/jobs/gemini.env.example, skill ~/.claude/skills/gemini-tools/SKILL.md
