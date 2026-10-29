"""로컬 판정 — Jev(TypeSafe)와 같은 질문 모양을 맥 Ollama(qwen3)로 돌린다. 무료, 데이터가 집 밖으로 안 나간다.

    from judge import judge
    a = judge("결제가 3일째 실패해요", {
        "dept":   {"type": "choice", "instructions": "어느 팀이 맡나?", "criteria": {"billing": "결제·환불", "tech": "버그·장애"}},
        "anger":  {"type": "score",  "instructions": "고객이 얼마나 화났나?", "criteria": ["차분", "답답", "매우 화남"]},
        "urgent": {"type": "noul",   "instructions": "지금 급한가?"},
    })
    a["dept"]["choice"], a["anger"]["score"], a["urgent"]["noul"]   # 'billing', 2, 0.9

    python judge.py "<state>" questions.json      # 시험용, 답을 JSON으로 출력

설정 paths.env: HERMES_JUDGE_URL(기본 http://localhost:11434) · HERMES_JUDGE_MODEL(기본 main-64k, 늘 떠 있는 모델).
노트북에서는 URL을 맥 테일스케일 IP(http://100.114.236.66:11434)로 — 'mac-studio' 이름이면 Ollama 호스트 검사가 403.
호출이 실패하면 예외가 난다. 실패를 '아니오'로 읽지 말 것. Jev로 바꿀 땐 이 파일만 바꾼다(질문·답 모양 동일).
"""
import json
import sys
import urllib.request

from common import load_env

urlopen = urllib.request.urlopen  # 테스트가 바꿔 끼운다

SYSTEM = ("너는 판정기다. 주어진 state 만 보고 각 질문에 따로 답한다. "
          "noul 은 '예'일 확률(0~1), score 는 단계 번호, choice 는 선택지 이름. 설명 없이 JSON만.")


def _text(v) -> str:
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)


def _schema_and_line(qid: str, q: dict) -> tuple[dict, str]:
    if not isinstance(q, dict):
        raise ValueError(f"{qid}: 질문은 {{type, instructions, criteria}} 객체여야 한다")
    kind, crit, ask = q.get("type"), q.get("criteria"), q.get("instructions")
    if not ask:
        raise ValueError(f"{qid}: instructions 없음")
    ask = _text(ask)
    if kind == "choice":
        if not isinstance(crit, dict) or not crit:
            raise ValueError(f"{qid}: choice 는 criteria {{선택지: 설명}} 필요")
        opts = "; ".join(f"{k} = {_text(v)}" if v is not None else k for k, v in crit.items())
        return {"type": "string", "enum": list(crit)}, f"- {qid} (choice): {ask} 선택지: {opts}"
    if kind == "score":
        if not isinstance(crit, list) or not 2 <= len(crit) <= 10:
            raise ValueError(f"{qid}: score 는 낮음→높음 단계 2~10개 필요")
        levels = "; ".join(f"{i} = {_text(v)}" for i, v in enumerate(crit))
        return ({"type": "integer", "minimum": 0, "maximum": len(crit) - 1},
                f"- {qid} (score 0~{len(crit) - 1}): {ask} 단계: {levels}")
    if kind == "noul":
        crit = crit if isinstance(crit, dict) else {}
        yes_no = ", ".join(f"{label} = {_text(crit[k])}" for k, label in (("true", "예"), ("false", "아니오")) if k in crit)
        yes_no = f" ({yes_no})" if yes_no else ""
        return {"type": "number", "minimum": 0, "maximum": 1}, f"- {qid} (예일 확률 0~1): {ask}{yes_no}"
    raise ValueError(f"{qid}: type 은 choice·score·noul 중 하나")


def _check(qid: str, q: dict, v) -> dict:
    kind = q["type"]
    if kind == "choice" and isinstance(v, str) and v in q["criteria"]:
        return {"choice": v}
    number = isinstance(v, (int, float)) and not isinstance(v, bool)  # True 를 '확실한 예'로 읽지 않게
    if kind == "score" and number and v == int(v) and 0 <= v < len(q["criteria"]):
        return {"score": int(v)}
    if kind == "noul" and number and 0 <= v <= 1:
        return {"noul": float(v)}
    raise ValueError(f"{qid}: 모델 답이 범위 밖 — {v!r}")


def judge(state, questions: dict, model: "str | None" = None) -> dict:
    """state(문자열이나 JSON 가능한 값)와 Jev 모양 질문들 → {질문id: {choice|score|noul: 값}}."""
    if state is None or (isinstance(state, str) and not state.strip()):
        raise ValueError("state 가 비었다 — 빈 입력에는 판정하지 않는다(앞 단계 실패일 수 있음)")
    try:
        env = load_env("paths")
    except FileNotFoundError:
        env = {}
    url = env.get("HERMES_JUDGE_URL", "http://localhost:11434").rstrip("/") + "/api/chat"
    parts = {qid: _schema_and_line(qid, q) for qid, q in questions.items()}  # 잘못된 질문은 호출 전에 거른다
    prompt = f"state:\n{_text(state)}\n\n질문:\n" + "\n".join(line for _, line in parts.values())
    body = {
        "model": model or env.get("HERMES_JUDGE_MODEL", "main-64k"),
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
        "format": {"type": "object", "properties": {qid: s for qid, (s, _) in parts.items()},
                   "required": list(parts)},
        "stream": False, "think": False, "options": {"temperature": 0},
    }
    req = urllib.request.Request(url, data=json.dumps(body, ensure_ascii=False).encode(),
                                 headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=180) as resp:
        content = json.loads(resp.read().decode()).get("message", {}).get("content")
    answers = json.loads(content) if content else None
    if not isinstance(answers, dict):
        raise ValueError(f"Ollama 답이 JSON 객체가 아니다 — {content!r:.200}")
    # ponytail: noul 은 모델이 말한 확률이라 Jev처럼 보정돼 있지 않다 — 0.7/0.3 문턱이 자주 틀리면 Jev로 교체
    return {qid: _check(qid, q, answers.get(qid)) for qid, q in questions.items()}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 1
    with open(argv[1], encoding="utf-8") as f:
        questions = json.load(f)
    print(json.dumps(judge(argv[0], questions), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):  # 윈도우 파이프는 cp949
        s.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
