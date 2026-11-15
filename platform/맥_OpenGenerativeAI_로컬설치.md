# 맥 — Open Generative AI 로컬 무료 설치 (단독 지시서, 2026-10-30)

> 맥스튜디오 Claude Code에 이 파일 내용을 그대로 붙여넣는다. 이 작업만 한다(다른 이관·세팅은 하지 않는다).
> 역할: **작은 시안(구도·색·썸네일·참고 이미지) = 이 앱 로컬 무료**, 큰 작업(360° 이어 그리기 · 영상 · 최종본) = Higgsfield. MuAPI 키는 넣지 않는다.

---

맥에 Open Generative AI를 로컬 무료 모드로 설치하고 시안 1장까지 확인해줘. 순서대로, 각 단계 끝에 한 줄로 결과만 알려줘.

1. 이미 `/Applications/Open Generative AI.app` 이 있으면 2로. 없으면 github.com/Anil-matcha/Open-Generative-AI 의 Releases 최신판에서 **arm64 .dmg** 를 받아(파일명·크기 먼저 보여주고 내 OK 받고) `/Applications` 에 설치. 체크섬 파일이 있으면 대조.
2. 앱을 열어. "확인되지 않은 개발자"로 막히면 시스템 설정 › 개인정보 보호 및 보안 › "그래도 열기"를 누르라고 나한테 알려만 줘(보안 설정은 내가 바꾼다).
3. 여기는 내가 한다 — 앱의 **Local Models** 화면에서 ① **Install Engine** ② **Z-Image Turbo** 다운로드(3.4GB, 텍스트 인코더 · VAE 같이 받음). API 키 칸은 비워 둔다. 끝나면 내가 "다 받았어"라고 말한다.
4. 받은 파일 위치를 찾아줘: `~/Library/Application Support/open-generative-ai/local-ai/` 아래 `bin`(엔진)·`models`(모델). 없으면 `find ~/Library -iname "z_image_turbo*" -o -iname "sd-cli*"` 로.
5. 엔진을 직접 불러 시안 1장: 엔진 `--help` 로 플래그를 먼저 확인하고, 대략
   `<엔진> --diffusion-model <z_image_turbo-Q4_K.gguf> --vae <ae.safetensors> --llm <Qwen3-4B…gguf> -p "a misty coastal pine forest at dawn, real photograph" --cfg-scale 1.0 --steps 8 -W 1344 -H 576 -o ~/Desktop/ogai_test.png`
   직접 호출이 안 되면 앱 화면에서 같은 프롬프트로 1장 만들어도 된다(그건 내가 누른다).
6. 걸린 시간 · 해상도 · 엔진/모델 경로 · 쓴 명령을 맥 Claude 메모리에 "Open Generative AI 로컬" 항목으로 남겨줘. 앞으로 작은 시안은 이 명령으로 만든다.

끝. 품질이 부족하면 나중에 앱에서 Z-Image Base(3.5GB, 50단계) 또는 SDXL Base(6.9GB)를 추가로 받는다.
