---
title: Ongoing Seocheon-gun (서천군) nature media-art video project and its conventions
author: Tkrudrn-lab
date: 2026-10-28
id: l-7f03838f
scope: repo
status: active
touches:
  - CLAUDE.md
  - SEOCHEON.md
  - LTX2.md
  - STACK.md
  - VAULT.md
  - panorama_test/C05_outpaint_21x9.png
  - panorama_raw/C05_pano.png
  - domains/mediaart/seocheon.md
---

## Decided
User is producing a Seocheon-gun (서천군) nature media-art piece: a 0–60s sequenced storyboard (spring camellia → summer vivarium → autumn reeds → winter/sunset beach → media-art whale/galaxy finale) defined in an Excel sheet `영상 프롬프트.xlsx` (cols: 초 / 시각연출 / 청각연출&효과 / 장면 / 영문 이미지 프롬프트). Each row = one clip; filename comes from the 시각연출 column.

Generation is done via the Higgsfield CLI (`hf`, installed at `~/.higgsfield/bin/hf.exe`; account [email]). Base 61 clips were made at 3s/4K with Kling 3.0 (Seedance 2.0 can't do <4s). Then converted into 30 vertical 9:16 "immersive media art reels" (ARTE Museum / teamLab style: content wrapped across 4 surfaces — walls + ceiling + mirror floor — with visitor silhouettes), via pipeline: extract frame → nano_banana_2 4-screen composite still → kling3_0 image-to-video.

Outputs: base clips in `바탕 화면\Higgefield\Assets`; reels in `바탕 화면\Higgefield\Reels`.

**2026-07-15 — project pivoted to a 30-min 4-wall installation piece** 『서천, 생명의 맥박 (The Pulse of Seocheon)』, based on the client's planning PDF (4 parts: 서막 동백/갯벌 여명 → 갯벌 오케스트라/춘장대 파도/주꾸미 → 칠면초 붉은 카펫/도요새 군무/한산모시 → 심해 잘피/전어떼/순환 엔딩). Room 16×16×3.5 m, 4-wall projection, 1-month deadline.
…

## Watch out
Reuse this folder/naming/model pipeline. See hermes-media-art-preferences for style/scope rules.

_From Claude Code's memory of this repo, last updated Oct 28._
