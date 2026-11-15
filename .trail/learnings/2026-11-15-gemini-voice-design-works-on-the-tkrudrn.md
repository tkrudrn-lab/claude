---
title: "Gemini voice design works on the free key; designed voices are called by name but can't share a podcast request"
author: Tkrudrn-lab
date: 2026-11-15
branch: main
cost: { minutes: 9, tokens: 41814 }
id: l-d406ed3a
scope: repo
status: active
src: agent
touches:
  - platform/CLAUDE.md
  - platform/jobs/gemini.py
  - platform/jobs/test_jobs.py
---

## Decided
- Voice design (describe a voice in one or two sentences and Google stores it) works on the free AI Studio key. Tested 2026-11-15: a voice was created in about 25 s with a 13.5 s preview WAV, then used for TTS in about 15 s.
- The helper resolves `tts --voice X` in this order: one of the 30 prebuilt names, a raw voice_ID, or the display name of a designed voice (looked up with voices.list). People remember names like "자연내레이터", not IDs.

## Watch out
- A prompted voice requires store=True. Without it the API returns INVALID_ARGUMENT.
- Stored voices expire after a year of no use, and a project holds at most 200.
- Designed voices can't be mixed into a multi-speaker podcast request. Synthesize each speaker separately if that's needed. The podcast command only takes prebuilt voices.
- Put permanent traits (age, timbre, accent) in the design description. Put one-off mood in tts --style.

In the code: platform/jobs/gemini.py voice_create / voice_list / resolve_voice / voice_delete, CLI `voice create|list|delete`; tests test_resolve_voice_by_name_and_passthrough, test_voice_create_stores_prompted_voice_and_saves_sample
