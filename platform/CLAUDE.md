# platform — 공용 인프라

**팀이 아니다.** 6개 도메인이 공유하는 인프라·도구 레이어이고, 소유 도메인이 없다.
도메인 문서에서 여기를 참조하되 여기에 도메인 작업물을 쌓지 않는다.

## 자동화 설계

**[자동화_설계_v01.md](자동화_설계_v01.md)** (2026-10-25, **승인**) — 맥스튜디오 24시간 본진, 5개 작업을 초안까지 에이전트가 만들어 텔레그램으로. 승인선·공용 뼈대(notify·카탈로그·launchd)·도메인별 흐름·착수 순서·맥 반입 체크리스트.
구현 계획: [0a 공용 뼈대](자동화_계획_0a_공용뼈대.md) (**코드 완료 2026-10-26**, 브랜치 `automation-0a` — 텔레그램 봇 연결만 사용자 대기) → 1 블로그 → 0b 맥 반입 → 2 누리텍 → 3 릴스 → 4 온돌.
`platform/jobs/` — `common.py`(설정·로그) · `notify.py`(텔레그램) · `catalog.py`(미디어 `_catalog.csv`) · `judge.py`(분류·점수·예/아니오 판정 — Jev 모양, 맥 Ollama qwen3로 무료, 2026-10-29) · `gemini.py`(Gemini 도우미, 아래 표). 테스트 `cd platform/jobs && python -m unittest test_jobs -v` (47개). 설정은 `~/.config/hermes/paths.env`·`telegram.env` (저장소 밖). 카탈로그 생성됨 — 비바사진 241 · 서천 1,809 (2026-10-26 12시 기준, 서천은 작업 중이라 늘어난다). 영상 촬영시각은 로컬(KST).

## 맥 세팅

**[맥_세팅_v01.md](맥_세팅_v01.md)** (2026-10-27) — 맥스튜디오에 이 파일 하나 주면 0→9 순서로 세팅. 노트북 짐 싸기(PowerShell) · brew · 플러그인·스킬 41+신규(instagram-agent-skill·hypit·ECC·find-skills) · 파일 이사 · MCP 최소 · 0a 뼈대 연결·launchd · 노션 AI setup 항목 · atticus-mac · 검증표. **노션 export zip 대기**(MOTION-KIT·Model Routing·블로그 프롬프트·PDF).
**남에게 주는 도구 세팅 → 독립 비공개 레포 [claude-setup/](../claude-setup/README.md)** (github.com/tkrudrn-lab/claude-setup, 2026-11-15 이전 · hermes 커밋과 섞지 않음, `.git/info/exclude`) — `Claude_Setup.md`(Claude에게 주는 원본, 맨 끝에 바이블 HTML) · `README.md`(처음 보는 사람용 그림 안내: 3단계 시작 · 흐름도 · 바이블 화면 5장 · 최근 추가 카드) · `ADDING.md`(새 기능 넣는 체크리스트 — 기능 카드 · 고칠 곳 · 검사 · 그림 다시 만들기). **수정은 그 폴더에서 하고 그 레포에 커밋 · push.** 내용: 맥_세팅 11절 + 릴스 「Claude 저장소 40개」 범용판 · A~J 88개 · E12 Gemini(2026-11-15).
**미디어아트 먼저 이관(2026-10-30):** 서천+지시파일+Claude/에이전트 설정 zip(구글 드라이브 내 드라이브 `hermes_맥이관_20261030.zip`, 원본 `D:\_mac_upload\`) → 맥에서 [맥_미디어아트_이관_프롬프트.md](맥_미디어아트_이관_프롬프트.md) 붙여넣기. D: 전체 Drive 백업은 취소.

## 에이전트 스택

| 자산 | 어디 |
|---|---|
| 다이어그램 3쌍 (`.json` 소스 + `.html` 렌더) — 아키텍처 / CI-CD / 로그인 시퀀스 | 저장소 루트 → [STACK.md](../STACK.md) |
| 설치 스크립트 `install_hermes_full.sh` | 저장소 루트 — **안 씀**(2026-10-27 결정: Hermes Agent는 공식 설치기 + 공식 메모리, [맥_세팅_v01.md](맥_세팅_v01.md) 10절). 서드파티 TencentDB 메모리·web-ui 구성의 기록용 |
| 컴포넌트 노트 21개 (Gateway / Agent / CLI / Memory System / Web UI) | `hermes-vault/` → [VAULT.md](../VAULT.md) |

다이어그램은 HTML을 직접 고치지 않는다. JSON을 고치고 다시 렌더한다.

## 생성·자동화 도구

| 도구 | 어디 |
|---|---|
| LTX-2 비디오 생성 모델 | `LTX-2/` → [LTX2.md](../LTX2.md). **독립 서브 git repo — hermes 커밋과 섞지 않는다** |
| Higgsfield CLI, Kling 3.0 | 볼트 외부 도구 노트 |
| **생성 역할 나누기 (2026-10-30)** | **큰 작업 = Higgsfield**(claude.ai 커넥터 — 360° 이어 그리기 · Kling 영상 · 고해상도 최종본) · **작은 작업 = Open Generative AI 로컬 무료**(맥, Z-Image Turbo — 구도·색 시안 · 썸네일 · 참고 이미지 초안). **노트북에서 부르기: `platform/ogai.sh "프롬프트" [폭 높이] [저장.png]`** — SSH `apple@mac-studio`(Tailscale, 키 등록 2026-10-30)로 맥 `sd-cli` 실행 후 가져옴, 1344×576 한 장 ≈ 42초. 설치는 단독 지시서 [맥_OpenGenerativeAI_로컬설치.md](맥_OpenGenerativeAI_로컬설치.md)(구글 드라이브에도 올림) · 전체판은 [맥_세팅_v01.md](맥_세팅_v01.md) 11절 |
| **Gemini 도우미 (2026-11-14)** | `platform/jobs/gemini.py` — Claude가 못 하는 것: 그림·사진 편집(Nano Banana 2.1) · 유튜브/영상 분석 · TTS · 2인 팟캐스트 · 목소리 설계(`voice create`) · 구글 검색 사실 확인 · URL 20개 읽기. Interactions API, 키 `~/.config/hermes/gemini.env`(저장소 밖). 스킬 `~/.claude/skills/gemini-tools/`. 출처: sambutlerai 「Connect Claude to Gemini」 PDF. **2026-11-15 무료 키로 확인: 글 · 유튜브 분석 · 로컬 영상(한글 이름 · 구간) OK / 음성(TTS) · 목소리 설계 OK / 그림 · 구글 검색 근거는 무료 하루 0회 → 429(결제 필요)** · **2026-11-21 기본 모델이 바쁘면(503 · 504 · 글 60초 / 영상 5분) `gemini-3.5-flash-lite`로 한 번 넘어감** |
| Archify (다이어그램 렌더) | `hermes-vault/`, `Ai\Project Ideas\` |
| Wan GPU 렌탈 세팅 가이드 | Google Drive |
| graphify 출력 | `graphify-out/` |

## 루틴 프롬프트

`prompts/` — `day1-router.md`, `day2-skill.md`, `day4-routine.md`, `day6-command-centre.md`, `day7-cli.md`

## 주의

- 여기 있는 것들은 **도구**지 도메인 자산이 아니다. mediaart가 LTX-2를 쓴다고 해서 mediaart 소유가 되지 않는다.
- 별도 팀을 만들지 않는다. 도메인 팀들이 필요할 때 읽어 간다.
