# hermes

AI 미디어아트 납품, 파충류샵 운영, 수입 무역을 혼자 굴리는 작업자. 이 저장소는 그 작업 전부의 루트다.
일은 **6개 도메인**으로 나뉘고 각 도메인은 별도 에이전트 팀으로 운영한다.

## 도메인

| 도메인 | 인덱스 | 팀 | 지금 상태 |
|---|---|---|---|
| 파충류샵 운영 | [domains/shop/CLAUDE.md](domains/shop/CLAUDE.md) | `shop` (3) | 상시 운영 — 블로그·영상·판매 문서·행사 |
| 미디어 아트 | [domains/mediaart/CLAUDE.md](domains/mediaart/CLAUDE.md) | `mediaart` (4) | 서천 『힐링미디어체험관』 v07 진행 중 (6테마 30분) / 다음은 공룡 테마 |
| 무역업 | [domains/trade/CLAUDE.md](domains/trade/CLAUDE.md) | `trade` (2) | ICU·수중러닝머신이 현재 메인 — 작업 공간은 **`D:\nuritech\`** (외장하드, 2026-10-17 hermes 밖으로 이동. 그 폴더에서 Claude 실행) |
| 피클볼 앱 | [domains/pickleball/CLAUDE.md](domains/pickleball/CLAUDE.md) | `pickleball` (1) | 기획 단계 — 코드 없음 |
| 개인 생활 | [domains/life/CLAUDE.md](domains/life/CLAUDE.md) | `life` (1) | 운동 기록 + 지식 정리 |
| 투자 | [domains/invest/CLAUDE.md](domains/invest/CLAUDE.md) | `invest` (1) | 기록·리서치까지 (범위 제한) |

## 공용

| 영역 | 인덱스 | 설명 |
|---|---|---|
| platform | [platform/CLAUDE.md](platform/CLAUDE.md) | 6개 도메인이 공유하는 인프라. **팀이 아니다** · **자동화 설계 v01 승인**(2026-10-25, 맥스튜디오 본진) · 0a 공용 뼈대 코드 완료(`platform/jobs/`, 2026-10-26) · **맥 세팅 지시서 [platform/맥_세팅_v01.md](platform/맥_세팅_v01.md)**(2026-10-27) · 다음 1 블로그 |
| hermes-vault | [VAULT.md](VAULT.md) | 옵시디언 노트 21개 (에이전트 스택·서천) |
| claude-setup | [claude-setup/README.md](claude-setup/README.md) | 남에게 주는 Claude Code 도구 세팅 패키지 — **독립 비공개 레포** github.com/tkrudrn-lab/claude-setup (hermes 커밋과 섞지 않음). 고칠 땐 그 폴더에서, 새 기능은 `claude-setup/ADDING.md` 체크리스트대로 |

## 매주 만지는 것

- **서천은 전부 `D:\서천군 영상 소스\`(USB 외장하드)에 있다** — 2026-09-25 영상, **2026-10-17 문서·음악·입찰·견적까지 전부 이관**(C 용량 부족). OneDrive `바탕 화면\서천군 릴스`는 이제 없다
- **서천 재개 시 먼저 `D:\서천군 영상 소스\서천군 릴스\v04_소스\서천_작업인수인계_20261017.md`** — 입찰(한서대 12분판) · 입찰 샘플 영상 · 본 제작 상태와 남은 일
- **★ 본편은 12분으로 간다(2026-10-29): `…\v04_소스\서천_12분_본편_씬구성_v10.md`(초안 · 결정 4건 대기)** — 제출 제안서 12분 장면표 + 최종 데모 33컷 전부. 30분 v09는 보류(재료 · 스크립트만 재사용)
- `…\v04_소스\서천_힐링미디어체험관_제작바이블_v07_6테마30분.md` — 캔버스 · 코너 · 출력 규칙 원장. 순서 · 시각은 12분 v10이 우선
- `naver-blog/` — 블로그 초안 공장
- `prompts/` — day1~day7 루틴 프롬프트

## 규칙

- **파일이 옮겨지거나 새 프로젝트가 시작되면 같은 턴에 이 라우터와 해당 영역 인덱스를 갱신한다.** 나중에 하지 않는다.
- 인덱스는 1페이지를 넘기지 않는다. 문서가 아니라 포인터다. 길어지면 하위 인덱스로 쪼갠다.
- 견적서 파일(`서천_미디어아트_견적서*.xlsx`)은 의도적으로 인덱스에서 제외한다. 금액 정보라 라우터에 노출하지 않는다.
- 도메인 문서가 가리키는 옵시디언 볼트 자산은 **경로 포인터일 뿐 저장소 안에 없다.** 볼트 통합은 아직 미승인이므로 볼트 파일을 옮기거나 고치지 않는다.

## 기존 인덱스 (위치 유지)

[SEOCHEON.md](SEOCHEON.md) · [STACK.md](STACK.md) · [LTX2.md](LTX2.md) · [VAULT.md](VAULT.md) — 도메인 문서에서 링크로 가리킨다. 파일은 옮기지 않았다.
