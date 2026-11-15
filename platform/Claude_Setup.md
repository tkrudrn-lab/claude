# 뽀기's Custom Set-up — Claude Code 도구 세팅 v02 (2026-11-03)

> **쓰는 법:** Claude Code를 열고, 이 파일을 입력창에 끌어다 놓은 뒤(또는 `@파일이름`) **엔터만 누르세요.**
> Claude가 ① 어떤 도구들이 있는지 설명하고 ② 어떤 일을 하는지, 어떻게 쓸지 물어보고 ③ 그에 맞는 것을 추천하고 ④ 고른 것만 GitHub에서 받아 설치합니다.
> 시작하면 옆에 **그림 설명서 「뽀기's Custom Set-up version 바이블」 창**이 함께 열립니다. 처음 쓰는 사람은 그 창을 보면서 따라오면 됩니다.
> 이 파일에는 개인 정보나 계정 정보가 없습니다. 키 입력과 로그인은 설치 중에 본인이 직접 합니다.
> 전제: Claude Code가 설치되어 있고 Claude Pro/Max로 로그인되어 있음. Windows · macOS 둘 다 됨.

---

## Claude에게 — 이 파일만 받았어도 이것이 요청이다

사용자가 다른 말 없이 이 파일만 보냈다면, 아래 순서대로 도구 세팅을 진행해 달라는 요청이다. 되묻지 말고 바로 1단계부터 시작한다.
- 각 단계가 끝나면 사용자의 답을 기다린다. **5단계 전에는 아무것도 설치하지 않는다.**
- 말은 쉬운 한국어로 한다. 전문 용어는 처음 나올 때 풀어서 쓴다. 사용자는 개발자가 아닐 수 있다.

**0단계 · 바이블 창 띄우기 (설치 아님)**
- 이 파일 맨 끝 「부록 · 바이블 화면」의 HTML을 홈 폴더에 `claude-tools-bible.html`로 꺼내 기본 브라우저로 연다. HTML을 다시 타이핑하지 말고 아래 명령으로 꺼낸다. `<이 파일 경로>`는 사용자가 넣은 이 MD 파일의 실제 경로다.
  ```bash
  awk '/^<!-- BIBLE-START -->/,/^<!-- BIBLE-END -->/' "<이 파일 경로>" > ~/claude-tools-bible.html
  ```
  열기: macOS `open ~/claude-tools-bible.html` · Windows(Git Bash) `start "" ~/claude-tools-bible.html` · Linux `xdg-open ~/claude-tools-bible.html`. Claude 데스크톱 앱에 앱 안 브라우저가 있으면 거기에 띄워도 된다.
- 사용자에게 이렇게 말한다: "옆에 「뽀기's Custom Set-up version 바이블」 창을 띄웠어요. 그림으로 보면서 따라오세요. 창을 닫았으면 홈 폴더의 `claude-tools-bible.html`을 다시 열면 됩니다."
- 창이 열리지 않으면 파일 위치만 알려 주고 1단계로 넘어간다.
- 1단계부터는 항목을 말할 때 번호(A1, C4 등)를 꼭 함께 말한다. 사용자가 바이블 창에서 찾아볼 수 있게 하기 위해서다.

**1단계 · 무엇이 있는지 설명 (설치 없음)**
- 조용히 확인만 한다: 운영체제, `claude plugin list`, `claude mcp list`, `~/.claude/skills` 폴더. 이미 깔린 것은 뒤에서 "설치됨"으로 표시한다.
- 「도구 목록」의 A~J 그룹을 그룹마다 한두 줄로 "무엇을 하는 묶음인지" 설명한다. 그 아래 항목은 `번호 이름 — 짧은 기능` 형태로 짧게 나열한다(긴 표 금지). H(참고 링크)와 「일부러 뺀 것」은 한 줄씩만 소개한다.
- 끝에 이렇게 말한다: "자세히 보고 싶은 그룹이 있으면 말씀하세요. 이제 어떤 일에 쓰실지 몇 가지 여쭤볼게요." 그리고 바로 2단계 첫 질문을 한다.

**2단계 · 하는 일과 쓰는 방식 묻기**
한 번에 다 묻지 말고 두세 번에 나눠 묻는다. 선택지가 4개 이하인 질문은 선택지 질문 도구(AskUserQuestion)가 있으면 그걸 쓰고, 아니면 번호 목록으로 묻는다.
1. 어떤 사업이나 일을 하나요? (업종, 혼자인지 팀인지, 손님이 온라인인지 오프라인인지)
2. Claude에게 주로 맡기고 싶은 일은? 여러 개 골라도 된다: 문서·제안서·PPT / 엑셀·숫자·회계 / 마케팅·SNS·블로그 / 영업·고객 응대 / 계약·법무 / 채용·인사 / 리서치·웹 자료 수집 / 홈페이지·디자인 / 영상·이미지 콘텐츠 / 상품 사진·포스터 / 앱끼리 자동화 / 고객에게 문자·카카오 알림톡 / 일정·할 일 관리 / 코딩 / 기타(직접 입력)
3. 폰 메신저(텔레그램 등)로 Claude에게 일을 시키고 싶나요?
4. 쓰고 있는 구독이나 계정: Claude Pro 또는 Max / ChatGPT 구독 / GitHub / Gmail·구글 캘린더 / Slack / 프리미어 프로 / 카카오 비즈니스 채널 / Zapier / Metricool·vidIQ 같은 SNS 도구 / 기타
5. 돈이 드는 외부 서비스(키 발급, 쓰는 만큼 결제)도 괜찮나요, 아니면 무료로만 갈까요?
6. 노트북 용량이나 성능이 넉넉한가요? (넉넉하지 않으면 무거운 것은 뺀다)
답이 애매하면 하나만 더 묻고 넘어간다.

**3단계 · 맞춤 추천**
- 「추천 지도」로 사용자 답에 맞는 항목을 고른다. 「모두에게 기본」은 항상 넣는다.
- 표로 보여 준다: `번호 | 이름 | 추천 이유(사용자 답과 연결해서) | 필요한 것·비용`. 보통 15~25개 정도로 맞춘다.
- 비슷한 것은 하나만 추천한다(목록의 "비슷한 것" 줄 참고).
- 무료만 원하면 키나 결제가 필요한 것은 「나중에 고려」 칸으로 따로 보여 준다.
- I 그룹(개인 비서)은 3번 답이 "예"일 때만 추천한다. Claude Pro만 있으면 I1이나 I2를, ChatGPT 구독이 있으면 I5도 후보로 넣는다. I5를 추천할 때는 모델 요금 표를 같이 보여 준다.

**4단계 · 고르기 확정**
- 이렇게 묻는다: "추천에서 뺄 것이나 목록에서 더할 것이 있으면 번호로 알려 주세요. 예: `C9 빼고 E3 추가`, 그대로면 `추천대로`."
- 최종 설치 목록(이미 설치된 것 표시 포함)과 준비물(키, 로그인, 앱)을 표로 다시 보여 주고 "이대로 설치할까요?"라고 묻는다. 사용자가 "예"라고 하면 5단계로 간다.

**5단계 · 설치** — 「0. 기본 도구」 중 필요한 것을 먼저 깔고, 최종 목록을 번호 순서대로 설치한다. 항목마다 아래 a~f를 지킨다.
- a. **README 먼저 읽기:** `curl -fsSL https://raw.githubusercontent.com/<소유자>/<저장소>/HEAD/README.md` 로 받아 설치 부분을 확인한다. 아래 명령은 2026-11-03에 README와 대조한 것이다. README가 그 뒤에 바뀌었으면 **README를 따른다.**
- b. `curl … | bash` 나 `irm … | iex` 같은 설치 스크립트는 바로 실행하지 않는다. 파일로 받고, 무엇을 하는지 사용자에게 요약해 준 다음 실행한다.
- c. 키나 로그인이 필요하면 멈추고 사용자에게 직접 하게 한다. 키 값은 파일과 채팅 어디에도 적지 않는다(환경변수나 각 도구의 로그인 명령으로만).
- d. `claude plugin install 이름@마켓` 의 `@마켓` 부분은 `claude plugin marketplace list` 로 확인한다. 아래에 적은 이름과 다를 수 있다.
- e. 설치 과정에서 CLAUDE.md나 settings.json에 규칙이나 훅을 넣으려 하면, 무엇을 넣는지 보여 주고 동의를 받는다.
- f. 실패하면 한 번 더 시도한다. 그래도 안 되면 건너뛰고 기록한 뒤 다음 항목으로 넘어간다. 전체를 멈추지 않는다.

**6단계 · 확인과 첫 사용 안내**
- 맨 아래 「확인」 절을 실행하고, 항목별로 설치됨 / 건너뜀 / 실패(이유)를 표로 보고한다.
- 사용자가 직접 해야 할 일(키 발급, 로그인, 커넥터 연결)을 체크리스트로 정리한다.
- 2단계 답에 맞춰 "처음 해 볼 만한 것" 세 가지를 알려 준다. 고른 도구의 README나 도움말에서 시작 명령을 찾아 예시 문장과 함께 보여 준다.
- 마지막으로 Claude Code를 재시작하라고 안내한다.

> **Windows + Claude 데스크톱 앱이면:** 앱 안에서 설치한 프로그램은 일부 파일이 앱 전용 숨은 폴더로 들어가, 앱 밖 터미널에서 안 보일 수 있다. 앱 밖에서도 쓸 CLI(uv, gh, rtk 등)는 **일반 PowerShell이나 Windows 터미널에서 설치**하라고 안내한다.

---

## 도구 목록 (1단계에서 짧게 설명하고, 3단계 추천에 쓴다)

무게: 가벼움 = 설치만 하면 끝 · 보통 = 설정이 조금 필요 · 무거움 = 용량이나 토큰을 많이 쓰거나 훅이 붙음

### A. 일하는 방식 — Claude Code의 작업 습관 전체를 바꾸는 것
| 번호 | 이름 | 하는 일 | 필요한 것 · 무게 |
|---|---|---|---|
| A1 | ★ superpowers | 브레인스토밍 → 계획 → TDD → 디버깅 순서를 스킬로 지키게 함 | 가벼움 |
| A2 | ★ andrej-karpathy-skills | 카파시의 코딩 규칙을 CLAUDE.md 하나로 | 가벼움 |
| A3 | ★ agent-skills (Addy Osmani) | spec → plan → build → test → review → ship 흐름 | 가벼움 |
| A4 | ★ mattpocock-skills | TDD, 코드 리뷰, PR, 버그 진단 | 가벼움 |
| A5 | ponytail | 코드를 최소로 쓰게 하는 규칙 | 가벼움 |
| A6 | gstack (Garry Tan) | 브라우저 QA · 리뷰 · 배포 등 도구 23개 | 보통 (bun 필요) |
| A7 | ECC (Everything Claude Code) | 스킬 311 · 에이전트 71 · 명령 97 | 무거움 (훅 없는 minimal로 설치) |
| A8 | GSD | 프로젝트를 단계별로 계획하고 실행 | 무거움 (훅 8종 + 상태 표시줄) |
| A9 | oh-my-claudecode | Claude Code 멀티 에이전트 팀 | 보통 |
| A10 | bmad | PRD · 설계 · 스프린트를 역할 에이전트로 진행 | 보통 |
| A11 | agency-agents | 마케팅 · 법무 · 영업 등 역할 에이전트 283개 | 무거움 (개수 많음) |
| A12 | Archon | AI 코딩 하네스를 직접 만드는 도구 | 무거움 (별도 앱, 개발자용) |

비슷한 것: A7 · A8 · A9 · A10 · A11 · A12는 모두 "큰 묶음"이라 하나나 둘만 골라도 됩니다.

### B. 사업 플러그인 — Anthropic 공식 (knowledge-work-plugins) · 사업하는 사람에게 가장 쓸모 있는 그룹
| 번호 | 이름 | 하는 일 |
|---|---|---|
| B1 | ★ small-business | 소상공인 업무 묶음: 매출 · 현금흐름 · 청구 · 마케팅 · 고객 응대 |
| B2 | ★ productivity | 할 일과 하루 계획, 업무 맥락 기억 |
| B3 | sales | 미팅 준비 · 고객 조사 · 파이프라인 · 아웃리치 |
| B4 | marketing | 콘텐츠 · 캠페인 · 성과 분석 |
| B5 | finance | 회계 · 정산 · 재무 보고 |
| B6 | customer-support | 문의 분류 · 답변 초안 · 지식베이스 |
| B7 | operations | 거래처 관리 · 업무 절차 문서 · 리스크 |
| B8 | data | 엑셀/SQL 데이터 분석 · 시각화 |
| B9 | legal | 계약서 검토 · NDA |
| B10 | human-resources | 채용 · 온보딩 · 평가 |
| B11 | brand-voice | 기존 글에서 브랜드 말투를 뽑아 규칙으로 |
| B12 | product-management | 기획서 · 로드맵 |

이 그룹은 Gmail · 캘린더 · Slack 같은 커넥터를 연결하면 더 잘 됩니다. 커넥터 연결은 claude.ai 설정에서 본인이 합니다.

### C. 글 · 디자인 · 마케팅 · 문서 스킬
| 번호 | 이름 | 하는 일 | 필요한 것 · 무게 |
|---|---|---|---|
| C1 | ★ anthropics/skills (공식) | Word · PowerPoint · Excel · PDF 만들기 + 사내 공지 · 문서 공동 작성 · 테마 · 웹앱 테스트 등 | 가벼움 |
| C2 | ★ find-skills | 필요한 스킬을 찾아 줌 | 가벼움 |
| C3 | ★ humanizer | AI 티 나는 문장 다듬기 | 가벼움 |
| C4 | ★ marketing-skills | 카피 · SEO · 광고 · 이메일 · 가격 등 마케팅 스킬 50여 개 | 가벼움 |
| C5 | instagram-agent-skill | 릴스 · 캡션 · 캐러셀 · DM 답장 글쓰기 13종 (게시는 안 함) | 가벼움 (Python) |
| C6 | ppt-master | PPT 생성 | 보통 (Python 패키지) |
| C7 | ui-ux-pro-max | UI/UX 디자인 시스템 · 배너 · 슬라이드 | 가벼움 |
| C8 | impeccable | 웹 디자인 품질 검사 | 가벼움 (훅 없이 설치) |
| C9 | taste-skill | 디자인 취향 다듬기 | **무거움** — 설치 후 꺼 두고 쓸 때만 켬 |
| C10 | diagram-design | 다이어그램 (Mermaid · draw.io · Excalidraw 가져오기) | 가벼움 |
| C11 | archify | 아키텍처 다이어그램 렌더 | 가벼움 |
| C12 | last30days | 최근 30일 화제 리서치 | 틱톡 · 인스타는 ScrapeCreators 키 |
| C13 | open-seo | SEO 감사 · 키워드 | DataForSEO 계정 |
| C14 | hyperframes | HTML로 영상 만들기 · 모션 스킬 | 보통 (ffmpeg) |
| C15 | hypit | 바이럴 영상 클론 | 무거움 · **자체 라이선스**라 상업용 전에 LICENSE 확인 |
| C16 | planning-with-files | 계획을 파일로 남겨 세션이 끊겨도 이어감 | 가벼움 |
| C17 | i-have-adhd | 답을 앞에 두고 짧게 말하게 함 | 가벼움 |
| C18 | caveman | 답을 짧게 해서 토큰 절약 | 가벼움 (스킬만) |
| C19 | career-ops | 구직 지원 관리 | 가벼움 · 구직할 때만 |
| C20 | wshobson/agents | 개발 분야별 플러그인 마켓 (필요한 것만 골라 설치) | 보통 · 개발자용 |
| C21 | ai-engineering-from-scratch (rohitg00) | AI 엔지니어링을 기초부터 배우는 과정. 스킬로 깔면 Claude가 튜터가 됨 (`/start-learning`) | 가벼움 · 학습용 |

비슷한 것: C3 · C17 · C18은 모두 답과 글을 다듬는 것 / C7 · C8 · C9는 모두 디자인 / C10 · C11은 모두 다이어그램

### D. 기억 · 코드 이해 — 개발자용 (코딩을 안 하면 그룹째 빼도 됨)
| 번호 | 이름 | 하는 일 | 필요한 것 · 무게 |
|---|---|---|---|
| D1 | claude-mem | 세션 사이에 기억을 유지 | 기록할 때마다 요금제 토큰을 씀 |
| D2 | agentmemory | 코딩 에이전트의 장기 기억 | 보통 (Node 20+) |
| D3 | beads | 코딩 에이전트용 작업 기억 | 가벼움 |
| D4 | graphify | 코드나 문서를 지식 그래프로 | 보통 (uv) |
| D5 | codegraph | 코드 지식 그래프를 자동으로 최신 유지 | 가벼움 |
| D6 | codebase-memory-mcp | 코드 구조 그래프 MCP | 가벼움 |
| D7 | Understand-Anything | 코드베이스를 그래프로 만들어 설명 | 보통 |
| D8 | trail | 코드 그래프 검색 + 세션별 배운 점 공유 | 보통 (저장소마다 init) |
| D9 | repomix | 저장소를 AI가 읽기 좋은 파일 하나로 묶음 | 가벼움 |
| D10 | serena | 의미 기반 코드 검색 · 편집 | 보통 (uv) |

비슷한 것: D1 · D2 · D3은 모두 기억 / D4 · D5 · D6 · D7 · D8 · D10은 모두 코드 그래프라 하나만 골라도 됩니다.

### E. 도구 · MCP
| 번호 | 이름 | 하는 일 | 필요한 것 · 무게 |
|---|---|---|---|
| E1 | ★ context7 | 라이브러리 최신 문서를 에이전트에 넣어 줌 | 가벼움 |
| E2 | ★ playwright-mcp | Claude가 브라우저를 직접 조작 | 가벼움 |
| E3 | firecrawl | 웹 페이지 수집 · 정리 | Firecrawl 키 · AGPL-3.0 |
| E4 | Agent-Reach | 여러 플랫폼 읽기 채널 | 보통 (uv) · 일부 채널은 로그인 |
| E5 | github-mcp-server | GitHub 공식 MCP | GitHub 토큰 · 개발자용 |
| E6 | vibe-kanban | 코딩 에이전트용 칸반 보드 | 가벼움 · 개발자용 |
| E7 | multica | 사람과 AI 에이전트를 한 팀으로 묶는 작업판 | 무거움 (서버 포함) |
| E8 | Codex (CLI + Claude Code 플러그인) | Claude Code 안에서 OpenAI Codex 부르기 | ChatGPT 계정 |
| E9 | rea-agents | 리버스 엔지니어링 MCP | 무거움 · 보안/개발자용 |
| E10 | Higgsfield | AI 이미지 · 짧은 영상 생성 (공식 CLI + 스킬, 또는 claude.ai 커넥터) | 유료 플랜 |
| E11 | premiere-pro-mcp | Claude에서 프리미어 프로 조작 | 프리미어 프로 |
| E12 | Gemini 도구 (gemini-tools) | Claude가 못 하는 것을 Gemini API로 — 그림 · 사진 편집, 유튜브 · 영상 분석, 보이스오버 · 2인 팟캐스트, 웹 페이지 20개 한 번에 읽기 | Google AI Studio 키 · 글 · 영상 분석은 무료, 검색 근거는 결제 필요 · 그림 · 음성도 결제가 필요할 수 있음 |

### F. 토큰 절약 · 상태 표시
| 번호 | 이름 | 하는 일 | 필요한 것 · 무게 |
|---|---|---|---|
| F1 | ★ rtk | 개발 명령 출력의 토큰을 60~90% 줄임 | 가벼움 |
| F2 | ★ claude-hud | 컨텍스트 사용량 · 도구 · 에이전트를 화면에 표시 | 가벼움 |
| F3 | headroom | LLM에 넣기 전에 출력을 압축 | 보통 · **MCP 방식만** (프록시 방식 금지, 아래 참고) |

### G. 앱
| 번호 | 이름 | 하는 일 | 필요한 것 · 무게 |
|---|---|---|---|
| G1 | AppFlowy | 오픈소스 노션 대체 (메모 · 할 일 · DB) | 가벼움 |
| G2 | OpenMontage | 영상 제작 자동화 파이프라인 | 무거움 · 개발 도구 필요 |
| G3 | atticus-mac | 단축키 음성 비서 (Claude 사용) | **macOS 26 이상만** |

### I. 개인 비서 에이전트 — 헤르메스와 그 대안 (하나만 고르면 됨)
폰 메신저로 일을 시키고, 예약 작업을 돌리고, 기억을 이어 가는 "개인 비서" 방식입니다. I1~I4는 Claude 구독 안에서 돌아갑니다. I5 헤르메스 원본은 **모델 요금을 따로 내야 합니다**(아래 표).
| 번호 | 이름 | 하는 일 | 필요한 것 · 무게 |
|---|---|---|---|
| I1 | ★ telegram 채널 플러그인 (Anthropic 공식) | 폰 텔레그램으로 노트북의 Claude Code에 일을 시킴 | 가벼움 · bun · 텔레그램 봇 토큰 · **Claude Code가 켜져 있을 때만** 동작 |
| I2 | ★ ClaudeClaw (moazbuilds) | 헤르메스와 가장 비슷함. 백그라운드 상주 · 예약 작업 · 텔레그램/디스코드/슬랙 · 웹 대시보드 | 보통 · 봇 토큰 · **허용 사용자 ID를 꼭 지정** |
| I3 | AionUi | 화면으로 쓰는 24시간 작업 앱. 깔린 Claude Code를 찾아 쓰고, 텔레그램 원격 · 예약 작업 지원 | 보통 · 데스크톱 앱 |
| I4 | NanoClaw | 컨테이너 안에서 도는 개인 비서, 메신저 10여 종 · 예약 작업 | 무거움 · Docker · Claude 연결 방식을 설치 때 확인 |
| I5 | ★ **Hermes Agent** (Nous Research 공식, MIT) | 스스로 배우는 개인 비서. 써 가면서 스킬을 직접 만들고 고친다. 텔레그램 · 디스코드 · 슬랙 · 왓츠앱 · CLI · 데스크톱 앱 · 예약 작업 · 서브에이전트 | 보통 · **모델 요금 별도** (아래) |
| I6 | oh-my-hermes | I5 위에 얹는 작업 분할 · 병렬 실행 층 (`omh-*` 스킬 100여 개) | I5를 고른 경우만 |

**I5 헤르메스의 모델 고르기 (`hermes model`)** — 로컬 모델은 쓰지 않는 전제
| 방법 | 되나 | 돈은 어디서 나가나 |
|---|---|---|
| ChatGPT 구독 (Codex 로그인) | 됨 | ChatGPT 요금제. 구독 한도 계산 방식은 문서에 아직 없음 |
| Claude **Max** 로그인 | 됨 | Max 기본 사용량이 아니라, **따로 사 둔 추가 사용량 크레딧에서 전부 빠짐** |
| Claude **Pro** 로그인 | **안 됨** | — |
| Anthropic API 키 | 됨 | 쓰는 만큼 종량제 (Claude 구독과 별개) |
| OpenRouter · Nous Portal | 됨 | 각 서비스 결제 |

비용을 정하기 어려우면 I1이나 I2로 시작하고, 헤르메스는 나중에 더해도 됩니다.

### J. 외부 서비스 연결 — 마케팅 · 콘텐츠 · 자동화 (각 서비스 계정 필요)
Claude에 "연결"해서 쓰는 외부 서비스입니다. 모두 업체가 공식으로 제공하는 연결 방법이고, 각 서비스의 계정과 요금은 따로입니다. Higgsfield(이미지 · 짧은 영상)는 E10에 있습니다.
| 번호 | 이름 | 하는 일 | 필요한 것 · 비용 |
|---|---|---|---|
| J1 | vidIQ | 유튜브 · 인스타에서 뜨는 콘텐츠와 급성장 채널 찾기 | 무료 플랜 가능 (크레딧 차감) |
| J2 | ★ Metricool | SNS 성과 분석 · 예약 발행 | 무료 플랜 가능 |
| J3 | Phantombuster | 인스타 · 링크드인 데이터 수집 자동화 | 유료 · **플랫폼 약관 위반으로 계정 제한 위험** |
| J4 | Photoroom | 배경 제거 · 제품 사진 연출 | 유료 API 크레딧 (앱 구독과 별개) |
| J5 | Ideogram | 글자가 안 깨지는 포스터 · 로고 | Ideogram 구독 |
| J6 | HeyGen | 내 사진과 목소리로 말하는 짧은 영상 | 플랜 크레딧 (일부 기능은 유료만) |
| J7 | ★ Zapier | 앱끼리 이어서 자동화 (예: 새 주문 → 시트 기록 → 메일) | Zapier 계정 · 호출마다 task 2개 |
| J8 | 솔라피 (SOLAPI) | 고객에게 문자 · 카카오 알림톡 발송 | 메시지당 요금 · 알림톡은 사업자 카카오 채널 + 템플릿 승인 |
| J9 | PlayMCP (카카오) | 카카오가 모아 둔 MCP 도구를 골라 도구함에 담아 쓰기 (예: 카톡 나에게 보내기) | 카카오 계정 · 무료 · 도구함 최대 10개 |

### H. 참고 자료 — 설치 없음, 링크만 알려 준다
- [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) — Claude Code 같은 하네스를 처음부터 만들며 배우는 교재
- [claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) — Claude Code 사용 모범 사례
- [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) — 스킬 추천 목록
- [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) — MCP 서버 모음
- [system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) — 여러 AI 도구의 시스템 프롬프트 모음. GPL-3.0이고 공식 출처가 아닌 것도 섞여 있어 읽기만 할 것

### 일부러 뺀 것 (설치하지 않는다)
- **claude-code-router · cc-switch** — Claude Code를 다른 모델이나 다른 API 주소로 보내는 도구. 이번 목적과 맞지 않고, 꺼지면 Claude도 같이 멈춘다.
- **headroom 프록시 모드 · 플러그인판** — `ANTHROPIC_BASE_URL`을 바꿔서 프록시가 죽으면 Claude가 멈춘다. F3은 MCP 방식만 쓴다.
- **wide-trace/open-higgsfield** — 계정과 저장소가 같은 날 만들어졌고 별점 조작이 의심되며, API 키를 받아 간다.
- **hermes-claude-auth** — 스스로 "Claude Code OAuth 우회"라고 소개하는 도구. 약관 위반으로 계정이 정지될 수 있다.
- 로컬 LLM(Ollama 등), 원격 접속 도구, 로컬 이미지/음성 모델 — 이번 세팅 범위 밖.

---

## 추천 지도 (3단계에서 쓴다)

2단계 답에서 해당하는 줄을 모두 모아 합친다. (키) = 키 발급 필요 · (유료) = 결제 필요 · (무거움) = 용량이나 토큰을 많이 씀

| 사용자가 말한 것 | 추천 |
|---|---|
| **모두에게 기본** | A1 superpowers · C1 공식 스킬(Word·PPT·Excel·PDF) · C2 find-skills · C3 humanizer · F2 claude-hud |
| 사업 운영 전반 | B1 small-business · B2 productivity · B7 operations |
| 엑셀 · 숫자 · 회계 | B5 finance · B8 data |
| 문서 · 제안서 · PPT | C6 ppt-master · C10 diagram-design · B11 brand-voice |
| 마케팅 · SNS · 블로그 | B4 marketing · C4 marketing-skills · C5 instagram-agent-skill · B11 brand-voice · J2 Metricool · J1 vidIQ · C12 last30days(키) · C13 open-seo(키) |
| 영업 · 고객 응대 | B3 sales · B6 customer-support · J8 솔라피(유료) |
| 계약 · 법무 | B9 legal |
| 채용 · 인사 | B10 human-resources |
| 리서치 · 웹 자료 수집 | E2 playwright-mcp · E4 Agent-Reach · E3 firecrawl(키) · C12 last30days(키) · E12 Gemini(유튜브 분석 · 페이지 20개 읽기, 키) |
| 홈페이지 · 디자인 | C7 ui-ux-pro-max · C8 impeccable · E2 playwright-mcp |
| 영상 · 이미지 콘텐츠 | C14 hyperframes · E10 Higgsfield(유료) · E12 Gemini(영상 분석 무료 · 그림 · 보이스오버) · J6 HeyGen(유료) · J5 Ideogram · E11 premiere-pro-mcp(프리미어를 쓰면) · C15 hypit(무거움) · G2 OpenMontage(무거움) |
| 상품 사진 · 포스터 · 로고 | J4 Photoroom(유료) · J5 Ideogram |
| 앱끼리 자동화 | J7 Zapier |
| 고객에게 문자 · 카카오 알림톡 · 카카오 서비스 | J8 솔라피(유료) · J9 PlayMCP |
| 일정 · 할 일 · 메모 | B2 productivity · C16 planning-with-files · G1 AppFlowy |
| 폰 메신저로 일 시키기 | Claude Pro만 있으면 I1(가벼움) 또는 I2(계속 켜 두는 형) · ChatGPT 구독이 있으면 I5 · 화면으로 쓰고 싶으면 I3 |
| 코딩도 한다 | A3 agent-skills · A4 mattpocock-skills · A5 ponytail · E1 context7 · D9 repomix · D5 codegraph(코드 그래프는 하나만) · F1 rtk · E8 Codex(ChatGPT 구독이 있으면) |
| GitHub를 쓴다 | E5 github-mcp-server(키) |
| 답을 짧고 핵심만 | C17 i-have-adhd 또는 C18 caveman (둘 중 하나) |
| AI를 공부하고 싶다 | C21 ai-engineering-from-scratch · H 참고 링크 |
| "다 갖춘 큰 묶음"을 원한다 | A7 ECC(minimal) 하나만. A8~A12는 사용자가 직접 원할 때만 |
| Gmail · 캘린더 · Slack 등을 쓴다 | B 그룹에 더해, claude.ai 설정에서 해당 커넥터를 연결하라고 6단계에서 안내 |

**사용자가 직접 원할 때만 추천:** A6 gstack · A8~A12 · C9 taste-skill · C19 career-ops · C20 wshobson/agents · D 그룹(코딩을 안 하면) · E6 vibe-kanban · E7 multica · E9 rea-agents · G3 atticus-mac(macOS 26 이상) · I4 NanoClaw · I6 oh-my-hermes · J3 Phantombuster(SNS 약관 위반 위험을 먼저 알린다)

---

## 0. 기본 도구 (5단계 맨 처음, 고른 항목에 필요한 것만)

**macOS** (Homebrew가 없으면 https://brew.sh 안내대로 먼저 설치)
```bash
brew install git gh node python@3.13 uv ffmpeg
brew install oven-sh/bun/bun          # A6 gstack이나 I1 텔레그램을 남겼을 때만
```

**Windows** (PowerShell)
```powershell
winget install Git.Git GitHub.cli OpenJS.NodeJS.LTS Python.Python.3.13 astral-sh.uv Gyan.FFmpeg
powershell -c "irm bun.sh/install.ps1 | iex"     # A6 gstack이나 I1 텔레그램을 남겼을 때만 (b 규칙대로 먼저 읽기)
```
- Node는 22 이상이어야 한다(`node -v`). ffmpeg는 C14 · C15 · G2를 남겼을 때만 필요하다.
- Windows에서 `bash` 명령(A11, C5 등)은 Git과 함께 깔리는 **Git Bash**에서 실행한다.
- 원하면 텔레메트리를 끈다(셸 설정 파일에 추가): `DO_NOT_TRACK=1` · `DISABLE_TELEMETRY=1` · `CLAUDE_MEM_ONLINE_OPTIN=false`

---

## 설치 명령 (번호별 — 4단계 최종 목록에 있는 것만 실행)

### A. 일하는 방식
```bash
# A1 superpowers
claude plugin marketplace add anthropics/claude-plugins-official
claude plugin install superpowers@claude-plugins-official
# A2 andrej-karpathy-skills
claude plugin marketplace add multica-ai/andrej-karpathy-skills
claude plugin install andrej-karpathy-skills@karpathy-skills
# A3 agent-skills — SSH 클론이 막히는 경우가 있어 HTTPS 주소로 추가
claude plugin marketplace add https://github.com/addyosmani/agent-skills.git
claude plugin install agent-skills@addy-agent-skills
# A4 mattpocock-skills (A1과 같은 공식 마켓)
claude plugin install mattpocock-skills@claude-plugins-official
# A5 ponytail
claude plugin marketplace add DietrichGebert/ponytail
claude plugin install ponytail@ponytail
# A6 gstack (bun 필요)
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && (cd ~/.claude/skills/gstack && ./setup)
# A7 ECC — 훅 없는 최소 설치. 다른 설치 방법과 섞지 말 것(중복 설치됨)
npx -y ecc-universal@2.2.3 install --profile minimal --target claude
# A8 GSD — 훅 8종 + 상태 표시줄이 붙는다
npx -y @opengsd/gsd-core@latest --claude --global
# A9 oh-my-claudecode
claude plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
claude plugin install oh-my-claudecode@<마켓 이름>        # d 규칙으로 마켓 이름 확인
# A10 bmad
claude plugin marketplace add bmad-code-org/bmad-plugins
claude plugin install bmad-method@bmad
claude plugin install bmad-toolbox@bmad
# A11 agency-agents (283개)
git clone --depth 1 https://github.com/msitarzewski/agency-agents /tmp/aa && bash /tmp/aa/scripts/install.sh --tool claude-code --no-interactive
# A12 Archon — 설치 스크립트는 b 규칙대로 먼저 읽기
#   macOS: brew install coleam00/archon/archon   그다음 archon setup
#   Windows: irm https://archon.diy/install.ps1 를 받아 읽고 실행
```

### B. 사업 플러그인 (남긴 것만)
```bash
claude plugin marketplace add anthropics/knowledge-work-plugins
claude plugin install small-business@knowledge-work-plugins        # B1
claude plugin install productivity@knowledge-work-plugins          # B2
claude plugin install sales@knowledge-work-plugins                 # B3
claude plugin install marketing@knowledge-work-plugins             # B4
claude plugin install finance@knowledge-work-plugins               # B5
claude plugin install customer-support@knowledge-work-plugins      # B6
claude plugin install operations@knowledge-work-plugins            # B7
claude plugin install data@knowledge-work-plugins                  # B8
claude plugin install legal@knowledge-work-plugins                 # B9
claude plugin install human-resources@knowledge-work-plugins       # B10
claude plugin install brand-voice@knowledge-work-plugins           # B11
claude plugin install product-management@knowledge-work-plugins    # B12
```
- Claude 데스크톱 앱을 쓰면 앱의 플러그인 화면에서 같은 이름으로 추가해도 된다.

### C. 글 · 디자인 · 마케팅 · 문서 스킬
```bash
# C1 Anthropic 공식 스킬 (문서 4종 + 일반 스킬)
npx -y skills add anthropics/skills -g -a claude-code -y -s docx pptx xlsx pdf algorithmic-art doc-coauthoring internal-comms slack-gif-creator theme-factory webapp-testing
# C2 find-skills
npx -y skills add https://github.com/vercel-labs/skills --skill find-skills -g -a claude-code -y
# C3 humanizer
claude plugin marketplace add blader/humanizer && claude plugin install humanizer@humanizer
# C4 marketing-skills
claude plugin marketplace add coreyhaines31/marketingskills && claude plugin install marketing-skills@marketingskills
# C5 instagram-agent-skill — 스킬 폴더 ig-* 를 ~/.claude/skills/ 로 복사, voice.md 템플릿은 ~/.claude/instagram/ 로
git clone https://github.com/Jakeschincariol/instagram-agent-skill.git ~/src/instagram-agent-skill
cp -R ~/src/instagram-agent-skill/skills/ig-* ~/.claude/skills/
mkdir -p ~/.claude/instagram && cp ~/src/instagram-agent-skill/templates/voice.md ~/.claude/instagram/voice.md
#   → voice.md 는 사용자에게 자기 브랜드 말투를 물어 채운다
# C6 ppt-master
npx -y skills add hugohe3/ppt-master -g -a claude-code -y
python -m pip install -r ~/.claude/skills/ppt-master/requirements.txt      # macOS Homebrew 파이썬이면 --break-system-packages 추가
# C7 ui-ux-pro-max
claude plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill && claude plugin install ui-ux-pro-max@ui-ux-pro-max-skill
# C8 impeccable — 훅 없이 (플러그인판은 턴이 끝날 때마다 30초씩 검사함)
npx -y impeccable install --providers=claude --scope=global --no-hooks && npx -y impeccable telemetry off
# C9 taste-skill — 설치 후 바로 끈다(긴 작업에 끼어들어 30~45분, 토큰 수십만). 쓸 때만 enable
claude plugin marketplace add Leonxlnx/taste-skill && claude plugin install taste-skill@taste-skill
claude plugin disable taste-skill@taste-skill
# C10 diagram-design
claude plugin marketplace add cathrynlavery/diagram-design && claude plugin install diagram-design@diagram-design
# C11 archify
npx -y skills add tt-a1i/archify -g
# C12 last30days
claude plugin marketplace add mvanhorn/last30days-skill && claude plugin install last30days@last30days-skill
# C13 open-seo (DataForSEO 계정은 사용자가 직접)
claude plugin marketplace add every-app/open-seo && claude plugin install openseo@openseo
# C14 hyperframes
claude plugin marketplace add heygen-com/hyperframes && claude plugin install hyperframes@hyperframes
# C15 hypit — 첫 렌더 때 Chromium · WhisperX를 받는다. 모델 서비스는 별도 계정·과금
npx -y skills add hypit-ai/hypit -g
# C16 planning-with-files
npx -y skills add OthmanAdi/planning-with-files --skill planning-with-files -g
# C17 i-have-adhd
claude plugin marketplace add ayghri/i-have-adhd && claude plugin install i-have-adhd@i-have-adhd
# C18 caveman — 스킬만 (플러그인 · CLI 경로는 훅과 프록시를 깔아서 쓰지 않음)
npx -y skills add JuliusBrussee/caveman -g -a claude-code -y
# C19 career-ops
claude plugin marketplace add career-ops-hq/career-ops && claude plugin install career-ops@career-ops
# C20 wshobson/agents — 마켓만 추가하고, 플러그인은 사용자가 고른 것만 설치
claude plugin marketplace add wshobson/agents
#   예: claude plugin install python-development@claude-code-workflows
# C21 ai-engineering-from-scratch — 설치 후 Claude Code에서 /start-learning
npx -y skills add rohitg00/ai-engineering-from-scratch -g -a claude-code -y
```

### D. 기억 · 코드 이해
```bash
# D1 claude-mem
claude plugin marketplace add thedotmack/claude-mem && claude plugin install claude-mem@thedotmack
# D2 agentmemory
npx -y @agentmemory/agentmemory@latest
npx skills add rohitg00/agentmemory -y
# D3 beads
brew install beads                    # macOS
npm install -g @beads/bd              # Windows
# D4 graphify — 설치 후 README의 Claude Code 연결 명령 실행
uv tool install graphifyy
# D5 codegraph — Claude Code 설정을 자동으로 잡아 준다
npm i -g @colbymchenry/codegraph
# D6 codebase-memory-mcp — README의 운영체제별 설치 스크립트를 b 규칙대로
#   https://github.com/DeusData/codebase-memory-mcp
# D7 Understand-Anything
claude plugin marketplace add Egonex-AI/Understand-Anything && claude plugin install understand-anything@understand-anything
# D8 trail — 코드 저장소 안에서 init
npm i -g @trailhq/trail-code && trail telemetry disable
#   쓰려는 저장소에서: trail init --agents claude --no-statusline
# D9 repomix
claude mcp add repomix -- npx -y repomix --mcp
# D10 serena — 설치 후 README의 「Claude Code」 MCP 등록 방법대로
uv tool install -p 3.13 serena-agent
```

### E. 도구 · MCP
```bash
# E1 context7
npx ctx7 setup
# E2 playwright-mcp
claude mcp add playwright npx @playwright/mcp@latest
# E3 firecrawl — 키는 사용자가 firecrawl.dev에서 발급
npx -y firecrawl-cli@latest init --all --browser
# E4 Agent-Reach — 기본 채널만
uv tool install https://github.com/Panniantong/Agent-Reach/releases/latest/download/agent-reach.zip && agent-reach setup
# E5 github-mcp-server — README의 Claude Code 방법대로 (Docker 또는 원격). 토큰(PAT)은 사용자가 발급
#   https://github.com/github/github-mcp-server
# E6 vibe-kanban — 설치 없이 실행
npx vibe-kanban
# E7 multica — 설치 스크립트를 b 규칙대로
#   https://github.com/multica-ai/multica
# E8 Codex
npm install -g @openai/codex
claude plugin marketplace add openai/codex-plugin-cc && claude plugin install codex@openai-codex
# E9 rea-agents
npx -y rea-agents setup --client claude_code --yes
# E10 Higgsfield — 유료 플랜. 업체 권장 방식: CLI + 스킬 (claude.ai 앱에서는 커넥터 https://mcp.higgsfield.ai/mcp)
npm i -g @higgsfield/cli && higgsfield auth login      # 로그인은 사용자가 직접
npx -y skills add higgsfield-ai/skills -g -a claude-code -y
# E11 premiere-pro-mcp
npm i -g premiere-pro-mcp            # 연결은 README의 claude mcp add 명령대로
# E12 Gemini 도구 — 설치할 저장소가 없다. Claude가 아래 요령대로 도우미와 스킬을 직접 만든다
#   (바탕: sambutlerai 「Connect Claude to Gemini」 가이드 + 실제로 써 보며 고친 점)
#   1) 사용자가 aistudio.google.com/apikey 에서 키를 만들어 ~/.config/gemini/gemini.env 에 GEMINI_API_KEY=키 로 넣는다
#      프로젝트 폴더 .env 가 아니라 홈 아래에 둔다(OneDrive · iCloud 동기화 폴더로 키가 올라가지 않게). 키를 채팅으로 받지 않는다
#      Windows PowerShell 에서는 notepad 에 ~ 가 안 먹으니 "$HOME\.config\gemini\gemini.env" 로 연다
pip install -U google-genai          # 2.25 이상
#   2) ~/.claude/skills/gemini-tools/ 에 gemini.py 와 SKILL.md(언제 어떤 명령을 쓰는지)를 만든다
#      명령: models · text [--search] [--urls] · video <링크|파일> [--start --end] [--out] · image [--prompt 여러 개 · --ref · --aspect] · tts [--voice --style] · podcast
#      - 먼저 aistudio.google.com/docs 의 지금 문서를 읽고 Interactions API(client.interactions.create)로 짠다 — 모델 이름은 models 명령으로 확인
#      - Client 는 하나 만들어 계속 쓴다(임시 Client 는 지워지는 순간 연결을 닫아 요청이 실패함)
#      - 로컬 영상은 경로 말고 열린 파일 + mime_type 으로 올린다(경로를 주면 한글 파일 이름이 HTTP 헤더에서 깨짐)
#      - Windows 콘솔은 stdout · stderr 를 utf-8 로 바꾼다(한글 깨짐)
#   3) 확인: gemini.py text "안녕" 과 공개 유튜브 링크 video 가 답하면 끝. 무료 키에서 --search 는 429(결제 필요)가 정상
```

### F. 토큰 절약 · 상태 표시
```bash
# F1 rtk — 설치 후 README의 Claude Code 연결 단계까지 한다
brew install rtk                      # macOS
winget install rtk-ai.rtk             # Windows
# F2 claude-hud — 설치 후 README의 설정 명령 실행
claude plugin marketplace add jarrodwatts/claude-hud && claude plugin install claude-hud@claude-hud
# F3 headroom — MCP 방식만. ANTHROPIC_BASE_URL을 바꾸는 프록시 단계는 건너뛴다
uv tool install --python 3.13 "headroom-ai[all]"
```

### G. 앱
```bash
# G1 AppFlowy
brew install --cask appflowy                             # macOS
#   Windows: https://github.com/AppFlowy-IO/AppFlowy Releases 또는 winget search AppFlowy
# G2 OpenMontage (Windows는 make가 필요 — README 확인)
git clone --depth 1 https://github.com/calesthio/OpenMontage.git ~/OpenMontage && (cd ~/OpenMontage && make setup)
# G3 atticus-mac (macOS 26 이상) — 설치 스크립트를 받아 읽고 실행
curl -fsSL https://raw.githubusercontent.com/SaarthurR/atticus-mac/main/install.sh -o /tmp/atticus-install.sh
#   읽은 뒤: bash /tmp/atticus-install.sh  → 첫 실행에 손쉬운 사용 · 마이크 권한
```

### I. 개인 비서 에이전트 (고른 것만)
```bash
# I1 telegram 채널 — bun 필요. 봇 토큰은 사용자가 텔레그램 @BotFather 에서 /newbot 으로 직접 발급
claude plugin marketplace add anthropics/claude-plugins-official      # A1에서 이미 했으면 건너뜀
claude plugin install telegram@claude-plugins-official
#   Claude Code 안에서 사용자가 직접: /telegram:configure <봇 토큰>
#   쓸 때는 이렇게 켠다: claude --channels plugin:telegram@claude-plugins-official
#   봇에게 DM → 봇이 준 6자리 페어링 코드를 README대로 승인 (본인 계정만 허용)
# I2 ClaudeClaw — 설치 후 설정 마법사(모델 · 하트비트 · 텔레그램 · 보안).
#   allowedUserIds 에 본인 텔레그램 ID만 넣는다 (비워 두면 예전 버전은 누구나 조작 가능했음)
claude plugin marketplace add moazbuilds/claudeclaw
claude plugin install claudeclaw@<마켓 이름>              # d 규칙으로 마켓 이름 확인
# I3 AionUi — https://github.com/iOfficeAI/AionUi Releases 에서 운영체제에 맞는 설치 파일. 첫 실행에 Claude Code를 자동으로 찾는다
# I4 NanoClaw — Claude 세션 안이 아니라 일반 터미널에서 실행한다(README 지시). Docker 필요
git clone https://github.com/nanocoai/nanoclaw.git ~/nanoclaw
#   그다음 README의 nanoclaw.sh 를 b 규칙대로 읽고 실행. Claude 연결을 API 키로 고르면 쓰는 만큼 요금이 나간다
# I5 Hermes Agent — https://github.com/NousResearch/hermes-agent
#   Windows는 Claude 데스크톱 앱 안이 아니라 일반 PowerShell에서 설치한다(맨 위 Windows 참고)
#   설치 스크립트는 b 규칙대로 받아서 읽고 실행:
#     macOS · Linux · WSL2: curl -fsSL https://hermes-agent.nousresearch.com/install.sh -o /tmp/hermes-install.sh  → 읽고 → bash /tmp/hermes-install.sh
#     Windows(PowerShell): irm https://hermes-agent.nousresearch.com/install.ps1 -OutFile $env:TEMP\hermes-install.ps1  → 읽고 → 실행
#   Windows 백신이 %LOCALAPPDATA%\hermes\bin\uv.exe 를 막으면 README의 오탐 안내를 따른다
hermes setup          # 다른 에이전트 설정 가져오기를 물으면 Claude Code 선택 가능 (스킬 · 설정만, 키는 안 가져옴)
hermes model          # 위 「모델 고르기」 표를 보여 주고 사용자가 고른 방법으로 로그인 — 키 · 로그인은 사용자가 직접
#   텔레그램 등 메신저 연결은 README의 gateway 설정대로 (봇 토큰은 사용자가 발급)
#   데스크톱 앱(Hermes Desktop)을 원하면 사이트의 설치 파일
# I6 oh-my-hermes — I5 설치 뒤에. 설치 스크립트는 b 규칙대로
#   https://github.com/rlaope/oh-my-hermes  (macOS: brew install rlaope/tap/omh 도 가능) → omh setup
#   모델 별칭을 바꾸려 하면 사용자에게 묻고 바꾼다. 제거는 omh uninstall --all
```

### J. 외부 서비스 연결 (고른 것만)
```bash
# J 공통: 원격 MCP는 추가한 뒤 Claude Code에서 /mcp → 해당 서비스 → 로그인 (사용자가 직접)
#   claude.ai 앱(웹 · 데스크톱)에서도 쓰려면 claude.ai 설정 → 커넥터에서 같은 서비스를 찾거나, 아래 URL을 직접 추가한다
# J1 vidIQ — 무료 플랜 가능 (조사 1회에 크레딧 약 5)
claude plugin marketplace add vid-io/vidiq-mcp
claude plugin install vidiq@vidiq-plugins
# J2 Metricool — 무료 플랜 가능
claude mcp add --transport http metricool https://ai.metricool.com/mcp
# J3 Phantombuster — 유료(체험 후). 인스타 · 링크드인 자동 수집은 각 플랫폼 약관 위반으로 계정이 제한될 수 있다고 먼저 알린다
claude mcp add --transport http phantombuster https://mcp.phantombuster.com
# J4 Photoroom — 앱 구독이 아니라 유료 API 크레딧을 쓴다. Photoroom 계정에서 API를 먼저 켠다
claude mcp add --transport http Photoroom https://mcp.photoroom.com/mcp
# J5 Ideogram — Ideogram 구독 사용
claude mcp add ideogram --transport http https://mcp.ideogram.ai/mcp
# J6 HeyGen — 플랜 크레딧 사용. C14 「HyperFrames by HeyGen」과는 다른 제품
claude mcp add --transport http -s user heygen https://mcp.heygen.com/mcp/v1/
# J7 Zapier — 성공한 호출마다 Zapier task 2개를 쓴다
claude plugin marketplace add anthropics/claude-plugins-official      # A1에서 이미 했으면 건너뜀
claude plugin install zapier@claude-plugins-official
# J8 솔라피 — 로컬 MCP. API Key · Secret은 README대로 사용자가 직접 설정. 메시지마다 요금
#   문자는 개인도 가능(발신번호 등록 1~3 영업일). 카카오 알림톡은 카카오 비즈니스 채널(사업자등록) + 템플릿 승인이 필요
#   발송은 기본 꺼져 있고 보낼 때마다 확인을 받는다. 처음엔 SOLAPI_MCP_DISABLE_SEND=true 로 미리보기만 써 보길 권한다
claude mcp add solapi -- npx --latest -y @solapi/mcp-server       # README의 설정과 다르면 README를 따른다
# J9 PlayMCP (카카오) — 카카오 계정, 무료. playmcp.kakao.com 에서 쓸 서버를 도구함에 담는다 (최대 10개)
claude mcp add --transport http playmcp https://playmcp.kakao.com/mcp   # 카카오 공식 안내(kko.kakao.com/connectclaude)와 다르면 공식을 따른다
```

---

## 확인 (6단계)

| 확인 | 명령 | 기대 |
|---|---|---|
| 기본 도구 | `node -v; python --version; uv --version; gh --version; git --version` | 전부 버전이 나옴 (Node 22 이상) |
| 플러그인 | `claude plugin list` | 남긴 A · B · C · D · F 플러그인이 전부 보이고, taste-skill만 disabled |
| 스킬 | `~/.claude/skills` 폴더 목록 | C1 · C2 · C5 · C6 · C11 · C15 · C16 · C18 등 남긴 스킬 폴더가 있음 |
| MCP | `claude mcp list` | 남긴 D · E · J 항목이 connected (J는 `/mcp`에서 로그인한 뒤) |
| CLI | `rtk --version` · `graphify --help` · `codex --version` 등 남긴 것만 | 실행됨 |

보고 형식: `번호 | 이름 | 설치됨/건너뜀/실패 | 메모(키 필요 · 재시작 필요 등)`

**무거워지면:** `claude plugin disable <이름>` 으로 하나씩 끈다. GSD는 `npx @opengsd/gsd-core@latest --uninstall`, gstack은 `~/.claude/skills/gstack/bin/gstack-uninstall`.

**키나 로그인이 남은 것 (사용자가 직접):** C12 ScrapeCreators · C13 DataForSEO · E3 Firecrawl · E4 Agent-Reach 로그인 채널 · E5 GitHub 토큰 · E8 ChatGPT · E10 Higgsfield · E12 Google AI Studio 키 · I1 · I2 · I5 텔레그램 봇 토큰 · I5 모델 로그인이나 키 · J 그룹 각 서비스 로그인과 결제(J8은 API 키) · B 그룹 커넥터(Gmail · 캘린더 · Slack 등)

---

## 부록 · 바이블 화면 (0단계에서 Claude가 꺼내 연다 — 사람은 읽지 않아도 됩니다)

```html
<!-- BIBLE-START -->
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>뽀기's Custom Set-up version 바이블</title>
<style>
:root{
  --bg:#f6f6f3;--surface:#fff;--sunk:#efefeb;--ink:#1c1c1f;--muted:#66666d;--line:#e2e2dc;--accent:#3355cc;
  --ok:#2b8a3e;--mid:#b26a00;--heavy:#c92a2a;
  --gA:#3355cc;--gB:#0b7a5f;--gC:#7b3fe4;--gD:#55636f;--gE:#cc4a0e;--gF:#9c6b00;--gG:#b8235a;--gI:#4a3bb0;--gJ:#0c7489;--gH:#66666d;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){:root{
  --bg:#131315;--surface:#1c1c20;--sunk:#24242a;--ink:#ececef;--muted:#a3a3ab;--line:#303037;--accent:#8aa2ff;
  --ok:#69db7c;--mid:#ffc14d;--heavy:#ff8787;
  --gA:#8aa2ff;--gB:#4fd1a8;--gC:#b994ff;--gD:#9fb0bd;--gE:#ff9a5c;--gF:#f0c050;--gG:#ff7aa8;--gI:#a99bff;--gJ:#4cc9e0;--gH:#a3a3ab;
  color-scheme:dark;}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.65 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",sans-serif;word-break:keep-all}
.wrap{max-width:1080px;margin:0 auto;padding:0 18px}
a{color:var(--accent)}
code{font:13px/1.4 ui-monospace,"Cascadia Code",Consolas,monospace;background:var(--sunk);padding:1px 6px;border-radius:5px}
h2{font-size:24px;margin:0 0 6px;letter-spacing:-.01em}
h3{margin:0;font-size:17px}
.sub{color:var(--muted);margin:0 0 22px}
section{padding:46px 0 10px}
.hero{padding:56px 0 30px;border-bottom:1px solid var(--line)}
.eyebrow{color:var(--accent);font-weight:700;font-size:13px;letter-spacing:.06em;margin:0 0 8px}
.hero h1{font-size:clamp(30px,5vw,46px);line-height:1.15;margin:0 0 14px;letter-spacing:-.02em}
.lead{font-size:17px;max-width:720px;margin:0 0 20px}
.stats{display:flex;flex-wrap:wrap;gap:10px}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:6px 14px;font-weight:600;font-size:14px}
nav.toc{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
nav.toc .wrap{display:flex;gap:4px;overflow-x:auto;padding-top:8px;padding-bottom:8px}
nav.toc a{white-space:nowrap;text-decoration:none;color:var(--ink);font-size:14px;padding:6px 10px;border-radius:8px}
nav.toc a:hover{background:var(--sunk)}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;counter-reset:s}
.step{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px;position:relative}
.step .n{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--accent);color:var(--surface);font-weight:800;margin-bottom:8px}
.step b{display:block;font-size:16px}
.step p{margin:6px 0 0;font-size:14px;color:var(--muted)}
.step .me{margin-top:10px;font-size:13px;background:var(--sunk);border-radius:8px;padding:6px 8px;color:var(--ink)}
.concept{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;align-items:stretch}
.core{grid-column:2;grid-row:2;background:var(--accent);color:var(--surface);border-radius:18px;display:grid;place-items:center;text-align:center;padding:20px;font-weight:800;font-size:19px}
.core small{display:block;font-weight:500;font-size:13px;opacity:.9}
.cc{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px}
.cc .ic{font-size:22px}
.cc b{display:block;margin:2px 0}
.cc p{margin:0;font-size:14px;color:var(--muted)}
.cc .eg{margin-top:8px;font-size:13px}
@media (max-width:720px){.concept{grid-template-columns:1fr}.core{grid-column:auto;grid-row:auto;order:-1}}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}
.chip{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:8px 14px;font:inherit;font-size:14px;cursor:pointer}
.chip[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--surface);font-weight:700}
.result{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px}
.result .head{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;align-items:baseline}
.pills{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.pill{border:1px solid var(--line);border-radius:8px;padding:3px 9px;font-size:13px;background:var(--sunk);cursor:pointer;color:var(--ink);font-family:inherit}
.pill i{font-style:normal;font-weight:800;margin-right:4px}
.btn{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:8px;padding:6px 12px;font:inherit;font-size:14px;cursor:pointer}
.tools{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:0 0 16px}
.tools input[type=search]{flex:1 1 240px;min-width:0;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:10px;padding:10px 12px;font:inherit}
.legend{display:flex;flex-wrap:wrap;gap:6px;font-size:13px;color:var(--muted);margin-bottom:18px}
.group{margin:0 0 28px}
.ghead{display:flex;gap:12px;align-items:flex-start;margin-bottom:10px}
.gl{flex:none;width:38px;height:38px;border-radius:10px;display:grid;place-items:center;color:var(--surface);font-weight:800;font-size:18px}
.ghead p{margin:2px 0 0;color:var(--muted);font-size:14px}
.sim{font-size:13px;color:var(--muted);background:var(--sunk);border-radius:8px;padding:6px 10px;margin:-2px 0 10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.card{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--gc);border-radius:12px;padding:12px 14px;transition:box-shadow .2s,opacity .2s}
.card .top{display:flex;gap:8px;align-items:baseline}
.card .id{font-weight:800;color:var(--gc);font-size:13px}
.card .nm{font-weight:700}
.card .star{color:var(--mid);font-size:13px}
.card p{margin:4px 0 8px;font-size:14px;color:var(--muted)}
.card.hit{box-shadow:0 0 0 2px var(--accent)}
.card.flash{box-shadow:0 0 0 3px var(--accent)}
.dim .card:not(.hit){opacity:.35}
.badges{display:flex;flex-wrap:wrap;gap:5px}
.bd{font-size:12px;border-radius:6px;padding:1px 7px;border:1px solid var(--line);color:var(--muted)}
.bd.w0{color:var(--ok);border-color:currentColor}.bd.w1{color:var(--mid);border-color:currentColor}.bd.w2{color:var(--heavy);border-color:currentColor}
.bd.dev{background:var(--sunk)}
.bd.rec{color:var(--accent);border-color:currentColor;font-weight:700}
.hidden{display:none!important}
.tbl{overflow-x:auto;background:var(--surface);border:1px solid var(--line);border-radius:12px;margin-bottom:16px}
table{border-collapse:collapse;width:100%;min-width:600px;font-size:14px}
th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--sunk);font-size:13px}
tr:last-child td{border-bottom:0}
.no{color:var(--heavy);font-weight:700}.yes{color:var(--ok);font-weight:700}
.safe{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.box{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px}
.box b{display:block;margin-bottom:4px}
.box p,.box li{font-size:14px;color:var(--muted);margin:0}
.box ul{margin:6px 0 0;padding-left:18px}
.arrow{font-weight:800;color:var(--accent)}
.say{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}
.bubble{background:var(--surface);border:1px solid var(--line);border-radius:14px 14px 14px 4px;padding:12px 14px;font-size:14px}
.bubble small{display:block;color:var(--muted);font-size:12px;margin-bottom:2px}
.note{background:var(--sunk);border-radius:12px;padding:12px 14px;font-size:14px;margin-top:14px}
dl{display:grid;grid-template-columns:max-content 1fr;gap:6px 16px;margin:0}
dt{font-weight:700}dd{margin:0;color:var(--muted)}
@media (max-width:560px){dl{grid-template-columns:1fr}dd{margin-bottom:8px}}
footer{padding:40px 0 60px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);margin-top:40px}
</style>
</head>
<body>
<header class="hero"><div class="wrap">
  <p class="eyebrow">처음 쓰는 사람을 위한 그림 안내서</p>
  <h1>뽀기's Custom Set-up version 바이블</h1>
  <p class="lead">이 창은 설명서입니다. 실제 진행은 <b>Claude Code 대화창</b>에서 Claude가 하나씩 물어보면서 합니다. 이 창은 옆에 띄워 두고, Claude가 말하는 번호(A1, C4 같은 것)를 여기서 찾아보세요.</p>
  <div class="stats" id="stats"></div>
</div></header>

<nav class="toc"><div class="wrap">
  <a href="#flow">진행 순서</a><a href="#concepts">기본 개념</a><a href="#finder">나에게 맞는 도구</a><a href="#catalog">전체 목록</a><a href="#assistant">개인 비서</a><a href="#install">설치는 이렇게</a><a href="#use">설치 후 쓰는 법</a><a href="#caution">주의할 것</a><a href="#glossary">용어 사전</a>
</div></nav>

<main class="wrap">

<section id="flow">
  <h2>진행 순서 — 6단계</h2>
  <p class="sub">대화창에서 이 순서로 진행됩니다. <b>5단계 전에는 아무것도 설치하지 않습니다.</b></p>
  <div class="steps">
    <div class="step"><span class="n">1</span><b>설명</b><p>Claude가 도구 묶음 10개를 소개합니다.</p><div class="me">나: 읽고, 궁금한 그룹을 물어보기</div></div>
    <div class="step"><span class="n">2</span><b>질문</b><p>하는 일, 쓰는 구독, 예산, 노트북 사양을 묻습니다.</p><div class="me">나: 편하게 대답하기</div></div>
    <div class="step"><span class="n">3</span><b>추천</b><p>내 일에 맞는 도구 15~25개를 이유와 함께 보여 줍니다.</p><div class="me">나: 아래 「나에게 맞는 도구」와 비교해 보기</div></div>
    <div class="step"><span class="n">4</span><b>확정</b><p>빼거나 더해서 최종 목록을 정합니다.</p><div class="me">나: <code>C9 빼고 E3 추가</code> 또는 <code>추천대로</code></div></div>
    <div class="step"><span class="n">5</span><b>설치</b><p>고른 것만 GitHub에서 받아 설치합니다.</p><div class="me">나: 키 입력과 로그인만 직접</div></div>
    <div class="step"><span class="n">6</span><b>확인</b><p>결과표와 "처음 해 볼 것" 세 가지를 알려 줍니다.</p><div class="me">나: Claude Code 다시 켜기</div></div>
  </div>
</section>

<section id="concepts">
  <h2>기본 개념 — Claude Code에 붙는 것들</h2>
  <p class="sub">Claude Code는 "일하는 사람"이고, 아래 것들은 그 사람에게 쥐여 주는 매뉴얼·도구·연결선입니다.</p>
  <div class="concept">
    <div class="cc"><div class="ic">📘</div><b>스킬 (Skill)</b><p>특정 일을 하는 방법을 적은 업무 매뉴얼. 관련된 일이 오면 Claude가 스스로 꺼내 읽습니다.</p><div class="eg">예: Excel 만들기, 인스타 캡션 쓰기</div></div>
    <div class="cc"><div class="ic">🧰</div><b>플러그인 (Plugin)</b><p>스킬·명령·에이전트·연결을 한 상자에 묶은 설치 단위. "마켓"에서 받습니다.</p><div class="eg">예: <code>small-business</code> 상자 하나에 업무 스킬 여러 개</div></div>
    <div class="cc"><div class="ic">🔌</div><b>MCP</b><p>Claude를 바깥 프로그램에 연결하는 표준 플러그. 브라우저, GitHub, 웹 수집기 같은 것.</p><div class="eg">예: Claude가 직접 브라우저를 열어 확인</div></div>
    <div class="cc"><div class="ic">👥</div><b>서브에이전트</b><p>역할을 맡은 보조 Claude. 큰 일을 나눠 맡기고 결과를 모읍니다.</p><div class="eg">예: 조사 담당, 검토 담당</div></div>
    <div class="core">Claude Code<small>일하는 사람<br>(내 Claude 구독으로 돌아감)</small></div>
    <div class="cc"><div class="ic">⚙️</div><b>훅 (Hook)</b><p>정해진 순간에 자동으로 도는 규칙. 편하지만 느려지거나 토큰을 쓸 수 있어 이 세팅은 꼭 필요한 것만 씁니다.</p><div class="eg">예: 작업이 끝날 때마다 검사</div></div>
    <div class="cc"><div class="ic">🔗</div><b>커넥터</b><p>claude.ai 계정에 붙이는 Gmail·캘린더·Slack 연결. claude.ai 설정에서 직접 켭니다.</p><div class="eg">예: 메일 초안, 일정 확인</div></div>
    <div class="cc"><div class="ic">🏪</div><b>마켓 (Marketplace)</b><p>플러그인 진열대. 대부분 GitHub 저장소이고, 먼저 마켓을 추가한 뒤 플러그인을 고릅니다.</p><div class="eg">예: Anthropic 공식 마켓</div></div>
    <div class="cc"><div class="ic">📱</div><b>개인 비서 에이전트</b><p>폰 메신저로 일을 시키고 예약 작업을 돌리는 방식. I 그룹에서 고릅니다.</p><div class="eg">예: 텔레그램으로 "오늘 할 일 정리해 줘"</div></div>
  </div>
</section>

<section id="finder">
  <h2>나에게 맞는 도구 찾기</h2>
  <p class="sub">하는 일을 눌러 보세요(여러 개 가능). 「모두에게 기본」은 항상 들어갑니다. 아래 전체 목록에서도 파란 테두리로 표시됩니다.</p>
  <div class="chips" id="chips"></div>
  <div class="result">
    <div class="head"><b id="rcount"></b><span><button class="btn" id="onlyRec" aria-pressed="false">목록에서 추천만 보기</button> <button class="btn" id="clear">선택 지우기</button></span></div>
    <div class="pills" id="pills"></div>
    <div class="note">(키) 키 발급 필요 · (유료) 결제 필요 · 실제 추천은 Claude가 대화에서 내 답을 듣고 다시 맞춰 줍니다.</div>
  </div>
</section>

<section id="catalog">
  <h2>전체 목록</h2>
  <p class="sub">★ 거의 누구에게나 추천 · 색 막대는 그룹 · 무게는 설치·사용 부담입니다.</p>
  <div class="tools"><input type="search" id="q" placeholder="이름이나 기능으로 찾기 (예: 엑셀, 인스타, 텔레그램)" aria-label="도구 검색"></div>
  <div class="legend"><span class="bd w0">가벼움</span><span class="bd w1">보통</span><span class="bd w2">무거움</span><span class="bd dev">개발자용</span><span class="bd">키·계정 필요</span></div>
  <div id="groups"></div>
</section>

<section id="assistant">
  <h2>개인 비서 — 폰으로 일 시키기 (I 그룹)</h2>
  <p class="sub">하나만 고르면 됩니다. 돈이 어디서 나가는지가 가장 큰 차이입니다.</p>
  <div class="tbl"><table>
    <tr><th>번호 · 이름</th><th>어떻게 돌아가나</th><th>비용</th><th>노트북을 켜 둬야</th><th>이런 사람에게</th></tr>
    <tr><td><b>I1 텔레그램 채널</b><br>Anthropic 공식</td><td>텔레그램 메시지를 켜져 있는 Claude Code가 받아서 처리</td><td>Claude 구독 안</td><td>Claude Code 실행 중일 때만</td><td>가볍게 시작하고 싶은 사람</td></tr>
    <tr><td><b>I2 ClaudeClaw</b></td><td>백그라운드에 상주. 예약 작업, 텔레그램·디스코드·슬랙, 웹 대시보드</td><td>Claude 구독 안</td><td>노트북이 켜져 있으면 계속</td><td>헤르메스처럼 쓰고 싶은 Pro 사용자</td></tr>
    <tr><td><b>I3 AionUi</b></td><td>화면 있는 작업 앱. 깔린 Claude Code를 찾아 씀, 텔레그램 원격·예약</td><td>Claude 구독 안</td><td>앱이 켜져 있을 때</td><td>창으로 보며 쓰고 싶은 사람</td></tr>
    <tr><td><b>I4 NanoClaw</b></td><td>컨테이너 안에서 도는 비서, 메신저 10여 종</td><td>연결 방식에 따라</td><td>계속</td><td>Docker를 다룰 줄 아는 사람</td></tr>
    <tr><td><b>I5 Hermes Agent</b><br>Nous Research 공식</td><td>스스로 스킬을 만들고 고치며 배우는 비서. 메신저·데스크톱 앱·예약</td><td><b>모델 요금 별도</b> (아래 표)</td><td>계속</td><td>ChatGPT 구독이 있거나 API 비용을 낼 사람</td></tr>
  </table></div>
  <h3 style="margin:18px 0 8px">I5 헤르메스의 모델 요금</h3>
  <div class="tbl"><table>
    <tr><th>로그인 방법</th><th>되나</th><th>돈은 어디서</th></tr>
    <tr><td>ChatGPT 구독</td><td class="yes">됨</td><td>ChatGPT 요금제</td></tr>
    <tr><td>Claude Max</td><td class="yes">됨</td><td>Max 기본 사용량이 아니라 <b>따로 사 둔 추가 사용량 크레딧</b></td></tr>
    <tr><td>Claude Pro</td><td class="no">안 됨</td><td>—</td></tr>
    <tr><td>Anthropic API 키 · OpenRouter</td><td class="yes">됨</td><td>쓰는 만큼 종량제</td></tr>
  </table></div>
</section>

<section id="install">
  <h2>설치는 이렇게 — 안전하게</h2>
  <p class="sub">Claude가 도구 하나마다 이 순서를 지킵니다.</p>
  <div class="safe">
    <div class="box"><b><span class="arrow">①</span> README 먼저 확인</b><p>GitHub의 설명서를 그 자리에서 다시 읽고, 바뀐 설치법이 있으면 그걸 따릅니다.</p></div>
    <div class="box"><b><span class="arrow">②</span> 설치 스크립트는 먼저 읽기</b><p>인터넷에서 받은 스크립트는 바로 돌리지 않고, 무엇을 하는지 요약해 보여 준 뒤 실행합니다.</p></div>
    <div class="box"><b><span class="arrow">③</span> 설치</b><p>실패하면 한 번 더 시도하고, 그래도 안 되면 건너뛰고 기록합니다. 전체가 멈추지 않습니다.</p></div>
    <div class="box"><b><span class="arrow">④</span> 키·로그인은 내가 직접</b><p>키 값은 대화나 파일에 남기지 않습니다. 각 도구의 로그인 화면에서 직접 넣습니다.</p></div>
  </div>
  <div class="note"><b>Claude가 묻고 하는 것:</b> 설정 파일(CLAUDE.md, settings.json)에 규칙이나 자동 실행(훅)을 넣을 때는 무엇을 넣는지 보여 주고 동의를 받습니다.<br><b>Windows에서 Claude 데스크톱 앱을 쓰면:</b> 앱 밖에서도 쓸 프로그램(uv, gh, rtk, 헤르메스 등)은 일반 PowerShell에서 설치해야 앱 밖 터미널에서도 보입니다.</div>
</section>

<section id="use">
  <h2>설치 후 쓰는 법</h2>
  <p class="sub">대부분은 그냥 말로 시키면 됩니다. Claude가 맞는 스킬을 알아서 꺼냅니다.</p>
  <div class="say">
    <div class="bubble"><small>문서 · PPT</small>"지난달 매출 엑셀을 요약해서 PPT 5장으로 만들어 줘"</div>
    <div class="bubble"><small>마케팅</small>"우리 가게 말투로 인스타 릴스 캡션 3개 써 줘"</div>
    <div class="bubble"><small>법무</small>"이 계약서에서 우리에게 불리한 조항을 찾아 줘"</div>
    <div class="bubble"><small>리서치</small>"경쟁 업체 세 곳 홈페이지를 비교해서 표로 정리해 줘"</div>
    <div class="bubble"><small>고객 응대</small>"이 문의 메일에 정중한 답장 초안 써 줘"</div>
    <div class="bubble"><small>할 일</small>"이번 주 할 일을 급한 순서로 정리해 줘"</div>
  </div>
  <div class="safe" style="margin-top:14px">
    <div class="box"><b>/ 슬래시 명령</b><p>입력창에 <code>/</code>를 누르면 쓸 수 있는 명령 목록이 나옵니다. 플러그인 명령은 <code>/플러그인:명령</code> 모양입니다.</p></div>
    <div class="box"><b>무엇이 깔렸나 보기</b><p><code>/plugin</code> · <code>/mcp</code> 또는 터미널에서 <code>claude plugin list</code></p></div>
    <div class="box"><b>무거워지면 끄기</b><p><code>claude plugin disable 이름</code> — 지우지 않고 꺼 둘 수 있습니다. 다시 켜기는 <code>enable</code>.</p></div>
    <div class="box"><b>설치 후 한 번은 재시작</b><p>새 플러그인과 스킬은 Claude Code를 다시 켜야 나타납니다.</p></div>
  </div>
</section>

<section id="caution">
  <h2>주의할 것</h2>
  <div class="safe">
    <div class="box"><b>일부러 뺀 것</b><ul>
      <li>claude-code-router · cc-switch — 다른 모델로 보내는 도구. 꺼지면 Claude도 멈춤</li>
      <li>headroom 프록시 방식 — 같은 이유. F3은 MCP 방식만</li>
      <li>wide-trace/open-higgsfield — 별점 조작 의심, 키를 받아 감</li>
      <li>hermes-claude-auth — "인증 우회" 도구, 계정 정지 위험</li>
      <li>로컬 AI 모델 · 원격 접속 도구 — 이번 범위 밖</li></ul></div>
    <div class="box"><b>라이선스 · 약관 확인</b><ul>
      <li>J3 Phantombuster — 인스타 · 링크드인 자동 수집은 약관 위반으로 계정 제한 위험</li>
      <li>C15 hypit — 자체 라이선스, 상업용 전에 확인</li>
      <li>E3 firecrawl — AGPL-3.0</li>
      <li>H 시스템 프롬프트 모음 — GPL-3.0, 읽기만</li></ul></div>
    <div class="box"><b>키 · 결제가 필요한 것</b><ul>
      <li>C12 ScrapeCreators · C13 DataForSEO · E3 Firecrawl</li>
      <li>E5 GitHub 토큰 · E8 ChatGPT · E10 Higgsfield · E12 Google AI Studio 키</li>
      <li>I1 · I2 · I5 텔레그램 봇 토큰 · I5 모델 요금</li>
      <li>B 그룹 커넥터(Gmail · 캘린더 · Slack)</li>
      <li>J 그룹 각 서비스 계정 · 결제 (J1 · J2 · J9는 무료로 시작 가능, J8은 API 키 · 메시지당 요금)</li></ul></div>
    <div class="box"><b>토큰을 많이 쓰는 것</b><ul>
      <li>C9 taste-skill — 설치 후 꺼 둠, 쓸 때만 켬</li>
      <li>D1 claude-mem — 기록할 때마다 토큰 사용</li>
      <li>A7·A8·A11 큰 묶음 — 하나만 권장</li></ul></div>
  </div>
</section>

<section id="glossary">
  <h2>용어 사전</h2>
  <div class="box"><dl>
    <dt>토큰</dt><dd>Claude가 읽고 쓰는 글자 단위. 구독의 사용량은 토큰으로 계산됩니다.</dd>
    <dt>컨텍스트</dt><dd>Claude가 한 번에 기억하며 보는 대화·파일의 양. 꽉 차면 느려지고 앞부분을 요약합니다.</dd>
    <dt>GitHub · 저장소</dt><dd>프로그램을 올려 두는 사이트와 그 안의 프로젝트 폴더. 여기 도구들은 대부분 GitHub에 있습니다.</dd>
    <dt>README</dt><dd>저장소 맨 앞의 설명서. 설치 방법이 적혀 있습니다.</dd>
    <dt>CLI · 터미널</dt><dd>글자로 명령을 입력하는 창. Claude가 대신 입력해 줍니다.</dd>
    <dt>API 키</dt><dd>외부 서비스를 쓰기 위한 비밀번호 같은 값. 남에게 보이면 안 됩니다.</dd>
    <dt>종량제</dt><dd>구독료가 아니라 쓴 만큼 돈이 나가는 방식.</dd>
    <dt>CLAUDE.md</dt><dd>Claude가 매번 먼저 읽는 규칙 파일. 여기에 내 일하는 방식을 적어 둘 수 있습니다.</dd>
  </dl></div>
</section>

</main>
<footer><div class="wrap">2026-11-03 기준으로 정리했습니다. 도구는 자주 바뀌므로, 설치할 때 Claude가 각 README를 다시 확인합니다. 개인 정보나 계정 정보는 들어 있지 않습니다.</div></footer>

<script>
const G={
 A:{t:"일하는 방식",s:"Claude Code의 작업 습관 전체를 바꾸는 것",sim:"A7~A12는 모두 큰 묶음이라 하나나 둘만 골라도 됩니다."},
 B:{t:"사업 플러그인",s:"Anthropic 공식 업무 묶음. 사업하는 사람에게 가장 쓸모 있는 그룹",sim:"Gmail·캘린더·Slack 커넥터를 연결하면 더 잘 됩니다."},
 C:{t:"글 · 디자인 · 마케팅 · 문서",s:"문서 만들기, 글 다듬기, 마케팅, 디자인 스킬",sim:"C3·C17·C18은 모두 글을 다듬는 것 / C7·C8·C9는 디자인 / C10·C11은 다이어그램"},
 D:{t:"기억 · 코드 이해",s:"개발자용. 코딩을 안 하면 그룹째 빼도 됩니다",sim:"D1·D2·D3은 기억 / D4~D8·D10은 코드 그래프라 하나만 골라도 됩니다."},
 E:{t:"도구 · MCP",s:"브라우저, 웹 수집, 외부 서비스 연결",sim:""},
 F:{t:"토큰 절약 · 상태 표시",s:"사용량을 아끼고 눈으로 확인",sim:""},
 G:{t:"앱",s:"따로 설치하는 프로그램",sim:""},
 I:{t:"개인 비서 에이전트",s:"폰 메신저로 일 시키기 · 예약 작업 — 하나만 고르면 됩니다",sim:"I1~I4는 Claude 구독 안, I5는 모델 요금이 따로 듭니다."},
 J:{t:"외부 서비스 연결",s:"마케팅 · 콘텐츠 · 자동화 서비스를 Claude에 연결 — 각 서비스 계정과 요금은 따로",sim:"모두 업체 공식 연결 방법입니다. 연결 뒤 Claude Code에서 /mcp로 로그인합니다. Higgsfield는 E10에 있습니다."}
};
// w: 0 가벼움 1 보통 2 무거움 · k: 필요한 것 · s: ★ · dev: 개발자용
const T=[
 ["A1","superpowers","브레인스토밍 → 계획 → TDD → 디버깅 순서를 지키게 함",0,"",1],
 ["A2","andrej-karpathy-skills","카파시의 코딩 규칙을 CLAUDE.md 하나로",0,"",1,1],
 ["A3","agent-skills (Addy Osmani)","기획부터 출시까지 개발 흐름",0,"",1,1],
 ["A4","mattpocock-skills","TDD · 코드 리뷰 · PR · 버그 진단",0,"",1,1],
 ["A5","ponytail","코드를 최소로 쓰게 하는 규칙",0,"",0,1],
 ["A6","gstack (Garry Tan)","브라우저 QA · 리뷰 · 배포 등 도구 23개",1,"bun",0,1],
 ["A7","ECC","스킬 311 · 에이전트 71 · 명령 97 (훅 없는 최소판)",2,"",0],
 ["A8","GSD","프로젝트를 단계별로 계획하고 실행 (훅 8종)",2,"",0,1],
 ["A9","oh-my-claudecode","Claude Code 멀티 에이전트 팀",1,"",0,1],
 ["A10","bmad","기획서 · 설계 · 스프린트를 역할 에이전트로",1,"",0],
 ["A11","agency-agents","마케팅 · 법무 · 영업 등 역할 에이전트 283개",2,"",0],
 ["A12","Archon","AI 코딩 하네스를 만드는 도구",2,"별도 앱",0,1],
 ["B1","small-business","소상공인 업무: 매출 · 현금흐름 · 청구 · 마케팅 · 고객 응대",0,"",1],
 ["B2","productivity","할 일과 하루 계획, 업무 맥락 기억",0,"",1],
 ["B3","sales","미팅 준비 · 고객 조사 · 파이프라인 · 아웃리치",0,""],
 ["B4","marketing","콘텐츠 · 캠페인 · 성과 분석",0,""],
 ["B5","finance","회계 · 정산 · 재무 보고",0,""],
 ["B6","customer-support","문의 분류 · 답변 초안 · 지식베이스",0,""],
 ["B7","operations","거래처 관리 · 업무 절차 문서 · 리스크",0,""],
 ["B8","data","엑셀/SQL 데이터 분석 · 시각화",0,""],
 ["B9","legal","계약서 검토 · NDA",0,""],
 ["B10","human-resources","채용 · 온보딩 · 평가",0,""],
 ["B11","brand-voice","기존 글에서 브랜드 말투를 뽑아 규칙으로",0,""],
 ["B12","product-management","기획서 · 로드맵",0,""],
 ["C1","Anthropic 공식 스킬","Word · PowerPoint · Excel · PDF 만들기 외",0,"",1],
 ["C2","find-skills","필요한 스킬을 찾아 줌",0,"",1],
 ["C3","humanizer","AI 티 나는 문장 다듬기",0,"",1],
 ["C4","marketing-skills","카피 · SEO · 광고 · 이메일 등 마케팅 스킬 50여 개",0,"",1],
 ["C5","instagram-agent-skill","릴스 · 캡션 · 캐러셀 · DM 글쓰기 13종 (게시는 안 함)",0,"Python"],
 ["C6","ppt-master","PPT 생성",1,"Python"],
 ["C7","ui-ux-pro-max","UI/UX 디자인 시스템 · 배너 · 슬라이드",0,""],
 ["C8","impeccable","웹 디자인 품질 검사",0,""],
 ["C9","taste-skill","디자인 취향 다듬기 — 평소엔 꺼 둠",2,""],
 ["C10","diagram-design","다이어그램 그리기",0,""],
 ["C11","archify","아키텍처 다이어그램",0,""],
 ["C12","last30days","최근 30일 화제 리서치",0,"키(틱톡·인스타)"],
 ["C13","open-seo","SEO 감사 · 키워드",0,"DataForSEO"],
 ["C14","hyperframes","HTML로 영상 만들기 · 모션",1,"ffmpeg"],
 ["C15","hypit","바이럴 영상 클론 (자체 라이선스)",2,"ffmpeg"],
 ["C16","planning-with-files","계획을 파일로 남겨 끊겨도 이어감",0,""],
 ["C17","i-have-adhd","답을 앞에 두고 짧게",0,""],
 ["C18","caveman","답을 짧게 해서 토큰 절약",0,""],
 ["C19","career-ops","구직 지원 관리",0,""],
 ["C20","wshobson/agents","개발 분야별 플러그인 마켓",1,"",0,1],
 ["C21","ai-engineering-from-scratch","AI 엔지니어링 학습 과정, Claude가 튜터",0,"학습용"],
 ["D1","claude-mem","세션 사이에 기억 유지 (토큰 사용)",1,"",0,1],
 ["D2","agentmemory","코딩 에이전트의 장기 기억",1,"Node 20+",0,1],
 ["D3","beads","코딩 에이전트용 작업 기억",0,"",0,1],
 ["D4","graphify","코드·문서를 지식 그래프로",1,"uv",0,1],
 ["D5","codegraph","코드 지식 그래프 자동 유지",0,"",0,1],
 ["D6","codebase-memory-mcp","코드 구조 그래프 MCP",0,"",0,1],
 ["D7","Understand-Anything","코드베이스를 그래프로 설명",1,"",0,1],
 ["D8","trail","코드 그래프 검색 + 배운 점 공유",1,"",0,1],
 ["D9","repomix","저장소를 AI용 파일 하나로",0,"",0,1],
 ["D10","serena","의미 기반 코드 검색 · 편집",1,"uv",0,1],
 ["E1","context7","라이브러리 최신 문서를 넣어 줌",0,"",1,1],
 ["E2","playwright-mcp","Claude가 브라우저를 직접 조작",0,"",1],
 ["E3","firecrawl","웹 페이지 수집 · 정리 (AGPL)",0,"키"],
 ["E4","Agent-Reach","여러 플랫폼 읽기 채널",1,"uv"],
 ["E5","github-mcp-server","GitHub 공식 MCP",0,"GitHub 토큰",0,1],
 ["E6","vibe-kanban","코딩 에이전트용 칸반 보드",0,"",0,1],
 ["E7","multica","사람과 AI 에이전트를 한 팀으로",2,""],
 ["E8","Codex","Claude Code 안에서 OpenAI Codex 부르기",0,"ChatGPT 계정"],
 ["E9","rea-agents","리버스 엔지니어링 MCP",2,"",0,1],
 ["E10","Higgsfield","AI 이미지 · 짧은 영상 생성 (공식 CLI + 스킬)",0,"유료 플랜"],
 ["E11","premiere-pro-mcp","Claude에서 프리미어 프로 조작",0,"프리미어 프로"],
 ["E12","Gemini 도구","그림 · 영상 분석 · 음성 · 페이지 20개 읽기를 Gemini API로",0,"Google AI Studio 키"],
 ["F1","rtk","개발 명령 출력 토큰을 60~90% 줄임",0,"",1],
 ["F2","claude-hud","컨텍스트 사용량 · 도구 · 에이전트 표시",0,"",1],
 ["F3","headroom","출력을 압축 (MCP 방식만)",1,""],
 ["G1","AppFlowy","오픈소스 노션 대체 (메모 · 할 일 · DB)",0,""],
 ["G2","OpenMontage","영상 제작 자동화",2,"개발 도구"],
 ["G3","atticus-mac","단축키 음성 비서",0,"macOS 26+"],
 ["I1","텔레그램 채널 (공식)","폰 텔레그램으로 Claude Code에 일 시키기",0,"봇 토큰",1],
 ["I2","ClaudeClaw","상주형 비서 · 예약 작업 · 메신저 · 대시보드",1,"봇 토큰",1],
 ["I3","AionUi","화면으로 쓰는 24시간 작업 앱",1,""],
 ["I4","NanoClaw","컨테이너 안의 개인 비서",2,"Docker"],
 ["I5","Hermes Agent","스스로 배우는 개인 비서 (Nous Research)",1,"모델 요금 별도",1],
 ["I6","oh-my-hermes","I5 위에 얹는 병렬 실행 층",1,"I5 필요"],
 ["J1","vidIQ","유튜브 · 인스타에서 뜨는 콘텐츠와 급성장 채널 찾기",0,"무료 플랜 가능"],
 ["J2","Metricool","SNS 성과 분석 · 예약 발행",0,"무료 플랜 가능",1],
 ["J3","Phantombuster","인스타 · 링크드인 데이터 수집 자동화 (플랫폼 약관 위반 위험)",1,"유료"],
 ["J4","Photoroom","배경 제거 · 제품 사진 연출",0,"유료 API 크레딧"],
 ["J5","Ideogram","글자가 안 깨지는 포스터 · 로고",0,"Ideogram 구독"],
 ["J6","HeyGen","내 사진과 목소리로 말하는 짧은 영상",0,"플랜 크레딧"],
 ["J7","Zapier","앱끼리 이어서 자동화 (새 주문 → 시트 → 메일)",0,"Zapier 계정",1],
 ["J8","솔라피 (SOLAPI)","고객에게 문자 · 카카오 알림톡 발송",1,"메시지당 요금"],
 ["J9","PlayMCP (카카오)","카카오가 모아 둔 MCP 도구를 골라 연결 (예: 카톡 나에게 보내기)",0,"카카오 계정 · 무료"]
];
const H=[
 ["learn-claude-code","Claude Code 같은 하네스를 처음부터 만들며 배우는 교재","https://github.com/shareAI-lab/learn-claude-code"],
 ["claude-code-best-practice","Claude Code 사용 모범 사례","https://github.com/shanraisshan/claude-code-best-practice"],
 ["awesome-claude-skills","스킬 추천 목록","https://github.com/travisvn/awesome-claude-skills"],
 ["awesome-mcp-servers","MCP 서버 모음","https://github.com/punkpeye/awesome-mcp-servers"],
 ["system-prompts-and-models-of-ai-tools","AI 도구 시스템 프롬프트 모음 (GPL-3.0, 읽기만)","https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools"]
];
const BASIC=["A1","C1","C2","C3","F2"];
const USES=[
 ["사업 운영 전반",["B1","B2","B7"]],
 ["엑셀 · 숫자 · 회계",["B5","B8"]],
 ["문서 · 제안서 · PPT",["C6","C10","B11"]],
 ["마케팅 · SNS · 블로그",["B4","C4","C5","B11","J2","J1","C12","C13"]],
 ["영업 · 고객 응대",["B3","B6","J8"]],
 ["계약 · 법무",["B9"]],
 ["채용 · 인사",["B10"]],
 ["리서치 · 웹 자료",["E2","E4","E3","C12","E12"]],
 ["홈페이지 · 디자인",["C7","C8","E2"]],
 ["영상 · 이미지",["C14","E10","E12","J6","J5","E11","C15","G2"]],
 ["상품 사진 · 포스터",["J4","J5"]],
 ["앱끼리 자동화",["J7"]],
 ["문자 · 카카오 알림톡",["J8","J9"]],
 ["일정 · 할 일 · 메모",["B2","C16","G1"]],
 ["폰 메신저로 일 시키기",["I1","I2","I3","I5"]],
 ["코딩도 한다",["A3","A4","A5","E1","D9","D5","F1","E8"]],
 ["GitHub를 쓴다",["E5"]],
 ["답을 짧고 핵심만",["C17","C18"]],
 ["AI 공부",["C21"]],
 ["큰 묶음을 원한다",["A7"]]
];
const byId={};T.forEach(r=>byId[r[0]]=r);
const el=(tag,cls,txt)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e};
const W=["가벼움","보통","무거움"];
document.getElementById("stats").append(
 el("span","stat","그룹 10개"),el("span","stat","도구 "+T.length+"개"),el("span","stat","참고 링크 "+H.length+"개"),el("span","stat","설치는 고른 것만"));

const groupsEl=document.getElementById("groups"),cards={};
Object.keys(G).forEach(g=>{
 const sec=el("div","group");sec.dataset.g=g;
 const head=el("div","ghead"),lt=el("div","gl",g);lt.style.background="var(--g"+g+")";
 const tx=el("div");tx.append(el("h3",null,g+". "+G[g].t),el("p",null,G[g].s));head.append(lt,tx);sec.append(head);
 if(G[g].sim)sec.append(el("div","sim","비슷한 것: "+G[g].sim));
 const grid=el("div","grid");
 T.filter(r=>r[0].replace(/\d+/,"")===g).forEach(r=>{
  const [id,nm,d,w,k,s,dev]=r,c=el("article","card");c.id="t-"+id;c.style.setProperty("--gc","var(--g"+g+")");
  const top=el("div","top");top.append(el("span","id",id),el("span","nm",nm));if(s)top.append(el("span","star","★"));
  const b=el("div","badges");b.append(el("span","bd w"+w,W[w]));if(k)b.append(el("span","bd",k));if(dev)b.append(el("span","bd dev","개발자용"));
  c.append(top,el("p",null,d),b);c.dataset.text=(id+" "+nm+" "+d+" "+k+" "+G[g].t).toLowerCase();
  grid.append(c);cards[id]=c;
 });
 sec.append(grid);groupsEl.append(sec);
});
const hs=el("div","group"),hh=el("div","ghead"),hl=el("div","gl","H");hl.style.background="var(--gH)";
const ht=el("div");ht.append(el("h3",null,"H. 참고 자료"),el("p",null,"설치 없이 링크만 — 읽어 보면 좋은 곳"));hh.append(hl,ht);hs.append(hh);
const hg=el("div","grid");H.forEach(([n,d,u])=>{const c=el("article","card");c.style.setProperty("--gc","var(--gH)");const a=el("a","nm",n);a.href=u;a.target="_blank";a.rel="noopener";const top=el("div","top");top.append(a);c.append(top,el("p",null,d));c.dataset.text=(n+" "+d).toLowerCase();hg.append(c)});
hs.append(hg);groupsEl.append(hs);

const chipsEl=document.getElementById("chips"),sel=new Set();
const basic=el("button","chip","모두에게 기본");basic.setAttribute("aria-pressed","true");basic.disabled=true;chipsEl.append(basic);
USES.forEach(([t],i)=>{const b=el("button","chip",t);b.setAttribute("aria-pressed","false");b.onclick=()=>{sel.has(i)?sel.delete(i):sel.add(i);b.setAttribute("aria-pressed",sel.has(i));update()};chipsEl.append(b)});
let only=false;
function recIds(){const s=new Set(BASIC);sel.forEach(i=>USES[i][1].forEach(x=>s.add(x)));return [...s].sort((a,b)=>T.indexOf(byId[a])-T.indexOf(byId[b]))}
function update(){
 const ids=recIds();document.getElementById("rcount").textContent="추천 "+ids.length+"개";
 const p=document.getElementById("pills");p.replaceChildren();
 ids.forEach(id=>{const r=byId[id],b=el("button","pill");b.append(el("i",null,id),document.createTextNode(r[1]+(r[4]?" · "+r[4]:"")));b.onclick=()=>{const c=cards[id];c.scrollIntoView({behavior:"smooth",block:"center"});c.classList.add("flash");setTimeout(()=>c.classList.remove("flash"),1400)};p.append(b)});
 Object.entries(cards).forEach(([id,c])=>c.classList.toggle("hit",ids.includes(id)));
 groupsEl.classList.toggle("dim",only);filter();
}
function filter(){
 const q=document.getElementById("q").value.trim().toLowerCase();
 groupsEl.querySelectorAll(".group").forEach(sec=>{let any=0;sec.querySelectorAll(".card").forEach(c=>{const ok=(!q||c.dataset.text.includes(q))&&(!only||c.classList.contains("hit"));c.classList.toggle("hidden",!ok);if(ok)any=1});sec.classList.toggle("hidden",!any)});
}
document.getElementById("q").oninput=filter;
document.getElementById("clear").onclick=()=>{sel.clear();chipsEl.querySelectorAll(".chip:not([disabled])").forEach(b=>b.setAttribute("aria-pressed","false"));update()};
const ob=document.getElementById("onlyRec");ob.onclick=()=>{only=!only;ob.setAttribute("aria-pressed",only);ob.textContent=only?"목록 전체 보기":"목록에서 추천만 보기";update()};
update();
</script>
</body>
</html>
<!-- BIBLE-END -->
```
