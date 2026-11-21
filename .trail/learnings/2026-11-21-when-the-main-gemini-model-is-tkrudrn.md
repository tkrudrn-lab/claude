---
title: "When the main Gemini model is busy, wait a fixed time then retry once on the lite model"
author: Tkrudrn-lab
date: 2026-11-21
branch: main
cost: { minutes: 1, tokens: 2499 }
id: l-3398d7b0
scope: repo
status: active
src: agent
touches:
  - platform/jobs/gemini.py
  - platform/jobs/test_jobs.py
---

## Decided
- Text and video questions get a per-request time limit (60 s for text, 300 s for video) and, if the main model is busy, one retry on gemini-3.5-flash-lite. On 2026-11-21 gemini-4-hydrogen returned 503 "high demand" and gemini-3.8-flash returned 504 or hung. Without a limit, `gemini.py text` sat for about 3 minutes and printed nothing. flash-lite answered in 1–4 s the whole time.
- The limit goes on each generation call (`timeout=` on interactions.create), not on the client's http_options. A client-wide limit would also cut off `files.upload` of a big local video.
- Only 5xx and client timeouts count as busy. 429 (free-tier "0 per day") and 400 are re-raised unchanged, because switching models doesn't fix them and they need the user to see the real reason.
- The switch prints one line to stderr (`[gemini] <model> 바쁨(...) → gemini-3.5-flash-lite로 다시`), so the reader knows the answer came from the lighter model.

## Watch out
- Images and TTS do not fall back. Those models have no lite substitute that gives the same kind of output.
- The SDK's error classes live in a private module (google.genai._gaos.lib.compat_errors). The check uses duck typing instead: the class name APITimeoutError, or `status_code >= 500`.
- The video fallback path is covered by a unit test only. It was not run against the live API.

In the code: platform/jobs/gemini.py — FALLBACK_MODEL, WAIT_S, VIDEO_WAIT_S, busy(), answer(); tests test_text_falls_back_to_lite_when_main_model_busy, test_video_timeout_falls_back_with_longer_wait, test_quota_error_does_not_fall_back
