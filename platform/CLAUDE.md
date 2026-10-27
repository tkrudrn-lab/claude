# platform — 공용 인프라

**팀이 아니다.** 6개 도메인이 공유하는 인프라·도구 레이어이고, 소유 도메인이 없다.
도메인 문서에서 여기를 참조하되 여기에 도메인 작업물을 쌓지 않는다.

## 자동화 설계

**[자동화_설계_v01.md](자동화_설계_v01.md)** (2026-10-25, **승인**) — 맥스튜디오 24시간 본진, 5개 작업을 초안까지 에이전트가 만들어 텔레그램으로. 승인선·공용 뼈대(notify·카탈로그·launchd)·도메인별 흐름·착수 순서·맥 반입 체크리스트.
구현 계획: [0a 공용 뼈대](자동화_계획_0a_공용뼈대.md) (**코드 완료 2026-10-26**, 브랜치 `automation-0a` — 텔레그램 봇 연결만 사용자 대기) → 1 블로그 → 0b 맥 반입 → 2 누리텍 → 3 릴스 → 4 온돌.
`platform/jobs/` — `common.py`(설정·로그) · `notify.py`(텔레그램) · `catalog.py`(미디어 `_catalog.csv`). 테스트 `cd platform/jobs && python -m unittest test_jobs -v` (15개). 설정은 `~/.config/hermes/paths.env`·`telegram.env` (저장소 밖). 카탈로그 생성됨 — 비바사진 241 · 서천 1,809 (2026-10-26 12시 기준, 서천은 작업 중이라 늘어난다). 영상 촬영시각은 로컬(KST).

## 맥 세팅

**[맥_세팅_v01.md](맥_세팅_v01.md)** (2026-10-27) — 맥스튜디오에 이 파일 하나 주면 0→9 순서로 세팅. 노트북 짐 싸기(PowerShell) · brew · 플러그인·스킬 41+신규(instagram-agent-skill·hypit·ECC·find-skills) · 파일 이사 · MCP 최소 · 0a 뼈대 연결·launchd · 노션 AI setup 항목 · atticus-mac · 검증표. **노션 export zip 대기**(MOTION-KIT·Model Routing·블로그 프롬프트·PDF).

## 에이전트 스택

| 자산 | 어디 |
|---|---|
| 다이어그램 3쌍 (`.json` 소스 + `.html` 렌더) — 아키텍처 / CI-CD / 로그인 시퀀스 | 저장소 루트 → [STACK.md](../STACK.md) |
| 설치 스크립트 `install_hermes_full.sh` | 저장소 루트 |
| 컴포넌트 노트 21개 (Gateway / Agent / CLI / Memory System / Web UI) | `hermes-vault/` → [VAULT.md](../VAULT.md) |

다이어그램은 HTML을 직접 고치지 않는다. JSON을 고치고 다시 렌더한다.

## 생성·자동화 도구

| 도구 | 어디 |
|---|---|
| LTX-2 비디오 생성 모델 | `LTX-2/` → [LTX2.md](../LTX2.md). **독립 서브 git repo — hermes 커밋과 섞지 않는다** |
| Higgsfield CLI, Kling 3.0 | 볼트 외부 도구 노트 |
| Archify (다이어그램 렌더) | `hermes-vault/`, `Ai\Project Ideas\` |
| Wan GPU 렌탈 세팅 가이드 | Google Drive |
| graphify 출력 | `graphify-out/` |

## 루틴 프롬프트

`prompts/` — `day1-router.md`, `day2-skill.md`, `day4-routine.md`, `day6-command-centre.md`, `day7-cli.md`

## 주의

- 여기 있는 것들은 **도구**지 도메인 자산이 아니다. mediaart가 LTX-2를 쓴다고 해서 mediaart 소유가 되지 않는다.
- 별도 팀을 만들지 않는다. 도메인 팀들이 필요할 때 읽어 간다.
