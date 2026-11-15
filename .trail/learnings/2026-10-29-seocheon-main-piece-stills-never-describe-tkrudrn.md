---
title: "Seocheon main-piece stills: never describe the multi-wall room in image prompts; get still approval before any video"
author: Tkrudrn-lab
date: 2026-10-29
branch: main
cost: { minutes: 1, tokens: 1818 }
id: l-4f0d7822
scope: repo
status: active
src: agent
---

## Decided
- For the 12-minute Seocheon main piece, the demo originals are not stretched. Each scene first gets a 21:9 still for the user to approve, and video is made from the approved stills afterward (user decision, 2026-10-29).
- Each still uses its demo source frame as the reference image, so the demo's color and feel carry over.

## Tried and ruled out
- Writing "a 4-wall immersive media-art room" (even followed by "not a photo of a room") into the image prompt. Nano Banana 2 then draws side panels, vertical seams, or a room box. This hit about 1 in 7 scenes and survived two retries.
- Adding a "no seams / no panels" sentence while keeping the room wording does not fix it.
- What works: describe only "one single continuous scene filling the whole frame edge to edge, no panels, no walls, no room". For the reference, use a clean still that was already generated for the same theme.

## Watch out
- References taken from demo hall/wall clips also carry their seams into the output.
- Reference images also carry their palette into the output. The demo's migrating-bird clip turned every tidal-flat scene into a red salt-marsh flat.

In the code:
- This is the Seocheon work indexed from `domains/mediaart/seocheon.md` and `domains/mediaart/CLAUDE.md`.
- The assets live outside the repo: stills are in `D:\서천군 영상 소스\서천군 릴스\v04_소스\_키프레임_v10\` (contact sheets under `_시트\`, replaced versions under `_교체전\`).
- The plan doc is `v04_소스\서천_12분_본편_씬구성_v10.md`, section 7.
- Model and settings: nano_banana_2, 21:9, 2k, 2cr per image.
