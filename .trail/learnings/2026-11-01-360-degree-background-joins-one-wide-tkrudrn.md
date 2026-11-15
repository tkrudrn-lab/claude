---
title: "360-degree background joins: one wide-gap inpaint leaves hard edges, fix with a narrow seam band"
author: Tkrudrn-lab
date: 2026-11-01
branch: main
cost: { minutes: 1, tokens: 1980 }
id: l-9a335b99
scope: repo
status: active
src: agent
---

## Decided
- To join an 8:1 background plate end to start as a 360-degree panorama, the first step is one Nano Banana 2.1 inpaint (21:9 2k) that fills the gap between the last 700 px and the first 700 px. Then each seam with a hard edge gets a second inpaint: a 1000 px band centered on the seam, with a 200 px crossfade inside the band.
- Every join is checked in a seam zoom (±700 px around each seam) before it is accepted.

## Tried and ruled out
- Matching the left and right context (blur-diff ≤ 12) is not enough. In about 1 in 3 underwater, fog and night scenes, the model ignores the context tone and paints the 1885 px gap as a separate picture, which leaves a vertical cut at both mask edges. The edge-score number also misses some of these, so the final check has to be visual.
- A single tone offset per side does not hide the cut.

## Watch out
- About 1 in 3 results ignore aspect_ratio 21:9 and come back 2048x2048 or 16:9. Reject on shape and resubmit.
- The model often shifts the right context about 30 px sideways. Phase-correlate each context and remap linearly before checking, or good results get rejected.
- If a media_upload result is short enough to come back inline, it fills the context. Requesting 13 or more slots (padding with dummies) makes it save to a file.

In the code: the media-art domain (`domains/mediaart/CLAUDE.md`). The tools are in the session scratchpad: `bg/bgplate.py` (join: shape/shift/tone ramp), `bg/seamfix.py` (prep/apply), `bg/edge.py`. Outputs go to `_배경_v10` (C:\Users\kk9oo\Videos\서천_배경_v10_임시 while D: is disconnected).
