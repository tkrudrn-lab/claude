---
title: "Gemini SDK pitfalls, and what a free AI Studio key can and cannot do"
author: Tkrudrn-lab
date: 2026-11-15
branch: main
cost: { minutes: 14, tokens: 37233 }
id: l-6bd1fa8b
scope: repo
status: active
replaces: l-21fe1b09
src: agent
touches:
  - platform/jobs/gemini.py
  - platform/jobs/test_jobs.py
---

## Decided
- Keep one cached Gemini client per process. A temporary Client gets garbage-collected right after the attribute lookup, which closes its connection ("Cannot send a request, as the client has been closed").
- Upload local videos as an open binary file plus mime_type, never as a path. Given a path, the SDK puts the file name into an HTTP header, and Korean names crash it.
- Turn off the SDK's silent retries for the interactions API (`client.interactions.sdk_configuration.retry_config = None`). Otherwise a 429 sits there retrying for minutes and looks like a hang. A free-tier "0 per day" limit never clears by waiting.
- Always ask image models for image/jpeg and save as .jpg. Asking for image/png returns 400 "Supported values: 'image/jpeg'".

## Watch out
- Free key, tested 2026-11-15. These work: text, YouTube and local video analysis with clipping, URL context, and TTS (Kore Korean voiceover in about 14 s, a 24 kHz mono 16-bit WAV). Image models (nano-banana-2.1, 3.1-flash-image) and Google Search grounding return 429 "limit: 0 requests per day on Free Tier", so they need billing turned on.
- HttpRetryOptions(attempts=1) in http_options does not stop the interactions-layer retries. Only the retry_config override does.
- The URL tool can't fetch some sites (example.com). The model then answers from memory and exits cleanly. Check that url_context_result shows status success.

In the code: platform/jobs/gemini.py (client: functools.cache + retry_config None; image: forced .jpg/jpeg; video_block: opened file upload), tests test_image_always_asks_jpeg_and_saves_jpg, test_client_turns_off_silent_retries, test_local_video_uploads_file_object_not_path
