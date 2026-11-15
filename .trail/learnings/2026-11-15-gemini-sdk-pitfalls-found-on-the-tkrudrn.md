---
title: "Gemini SDK pitfalls found on the first real calls, and what the free key can and cannot do"
author: Tkrudrn-lab
date: 2026-11-15
branch: main
cost: { minutes: 13, tokens: 33513 }
id: l-21fe1b09
scope: repo
status: active
src: agent
touches:
  - platform/jobs/gemini.py
  - platform/jobs/test_jobs.py
  - platform/CLAUDE.md
---

## Decided
- Keep a single cached Gemini client for the whole process. Calling client().models.list() or client().interactions.create() on a fresh client every time fails with "Cannot send a request, as the client has been closed". In SDK 2.33 the temporary Client gets garbage-collected right after the attribute lookup, and its connection closes with it.
- Upload local videos as an open binary file plus mime_type, not as a path. Given a path, the SDK copies the file name into the X-Goog-Upload-File-Name HTTP header, and a Korean file name (every Seocheon asset has one) crashes with UnicodeEncodeError: 'ascii'.

## Watch out
- Checked on a free AI Studio key on 2026-11-15: text, YouTube analysis, local video with start/end clipping, and URL context all work. Google Search grounding returns 429 "exceeded your current quota" on gemini-4-hydrogen, 3.8-flash and 3.5-flash-lite alike, so it needs billing turned on. Image and TTS were not tried.
- On a 429 the SDK retries quietly for minutes before it raises. A call that hangs this long is usually a billing or quota problem, not the network.
- The URL tool can't fetch some sites (example.com failed, Wikipedia worked). The model then answers from memory and still exits cleanly. Check that url_context_result shows status success.

In the code: platform/jobs/gemini.py (client is @functools.cache; video_block opens the file before upload), test test_local_video_uploads_file_object_not_path in platform/jobs/test_jobs.py
