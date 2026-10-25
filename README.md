# 생명의 다리 (Bridge to Life) — 스마트폰 앱

그림·모션·음성으로 복음을 전하는 다국어 앱입니다. 인터넷 주소 하나로 배포하고, 휴대폰 홈 화면에 앱처럼 설치해 오프라인에서도 쓸 수 있습니다(PWA).

## 1. 인터넷에 올리기 (한 번만)
이 폴더 전체를 무료 정적 호스팅에 올리면 됩니다.
- **Netlify Drop**: https://app.netlify.com/drop 에 이 폴더를 끌어다 놓기 → 주소가 바로 생깁니다.
- **GitHub Pages**: 새 저장소에 이 폴더 내용을 올리고 Settings → Pages 켜기.
※ 휴대폰 설치와 오프라인 기능은 https 주소에서만 동작합니다. 파일을 더블클릭해 여는 방식(file://)으로는 언어·음성 다운로드가 되지 않습니다.

## 2. 휴대폰에 설치
- **iPhone (Safari)**: 주소 열기 → 공유 버튼 → "홈 화면에 추가"
- **Android (Chrome)**: 주소 열기 → 메뉴(⋮) → "앱 설치" 또는 "홈 화면에 추가"
한 번 열어 두면 이후에는 인터넷 없이도 실행됩니다.

## 3. 화면 이동 (전도 현장용)
- 맨 위 왼쪽 **↩ 뒤로**: 방금 보던 장면으로 돌아갑니다 (번호로 건너뛴 뒤에도 그대로 돌아옴).
- **⌂ 처음으로**: 표지로 바로 갑니다.
- 아래 **단계 버튼 줄(새싹·1~8)**: 원하는 장면으로 바로 이동.
- 본문 위 **‘단계 목록’**: 모든 장면의 제목과 성경 구절을 보고 골라서 이동.
- 좌우로 밀기, 이전/다음 버튼도 그대로 됩니다.

## 4. 언어 추가하기 (제작 후에도 계속)
기본 내장: 한국어, English, 日本語, 简体中文, Bahasa Indonesia
온라인 목록 예시: Español (lang/es.json) — 앱의 [언어] → "온라인 언어 목록"에서 [받기]

새 언어를 추가하는 방법:
1. `lang/en.json`(또는 앱의 [언어] → "현재 언어 파일 저장")을 복사해 `lang/fr.json`처럼 저장
2. `meta.code`(예: "fr"), `meta.tts`(음성 언어, 예: "fr-FR"), `nativeName`, `bible`을 바꾸고 `ui`, `labels`, `steps` 문장을 번역
   - `steps`는 반드시 9개(표지 + 1~8단계)여야 합니다.
   - 구절의 `say`는 음성으로 읽을 장·절 표현입니다(예: "Jean chapitre 3, verset 16").
   - 아랍어처럼 오른쪽에서 왼쪽으로 쓰는 언어는 `"dir": "rtl"`
3. `lang/index.json`의 `languages` 목록에 한 줄 추가 → 서버에 다시 올리면, 이미 설치한 사람도 앱에서 바로 받을 수 있습니다.
   - 내용을 고쳤다면 `version` 숫자를 올리세요. 앱에 "↑ 받기"(업데이트) 버튼이 뜹니다.
4. 서버 없이 나눠 줄 때: .json 파일을 카톡·메일로 보내고, 받는 사람이 [언어] → "내 기기의 언어 파일 열기"로 추가.

## 5. 듣기 — AI 음성 고르기
앱의 [설정 ⚙] → "읽어 줄 목소리"에서 언어마다 목소리를 고르고 ▶로 미리 들어 볼 수 있습니다.

**방법 A. 휴대폰에 무료 AI 음성 받기 (가장 쉬움)**
- iPhone: 설정 › 손쉬운 사용 › 읽기 및 말하기 › 음성 › 언어 선택 › ‘고품질(Premium)’ 또는 ‘향상된(Enhanced)’ 음성 다운로드
- Android: 설정 › 일반 관리 › 텍스트 음성 변환 › Google 엔진 › ⚙ › 음성 데이터 설치
- 받은 뒤 앱 설정을 다시 열면 **‘AI 고품질’** 표시와 함께 나타납니다.
  (Safari는 기기에 따라 일부 Premium 음성을 웹앱에 보여 주지 않을 수 있습니다. 그때는 ‘향상된’ 음성을 받거나 방법 B를 쓰세요.)

**방법 B. AI 음성 팩 (미리 녹음한 고품질 음성, 오프라인 재생)**
누구의 휴대폰에서든 같은 목소리로 들리게 하고 싶을 때 씁니다.
1. Mac에서 터미널을 열고 이 폴더로 이동: `cd 폴더경로/BridgeToLife_PWA`
2. 음성 팩 만들기 (Mac 내장 음성, 인터넷 불필요):
   `python3 tools/make_voice_pack.py ko --voice "Yuna (Premium)" --name "유나 (AI 고품질)"`
   - Mac 음성 받기: 시스템 설정 › 손쉬운 사용 › 읽기 및 말하기 › 시스템 음성 › 음성 관리
   - 사용 가능한 음성 이름 보기: `say -v '?'`
   - Microsoft 신경망 음성을 쓰려면: `pip3 install edge-tts` 후
     `python3 tools/make_voice_pack.py ko --engine edge --voice ko-KR-SunHiNeural --name "선희 (AI)"`
3. `voice/` 폴더에 음성 팩이 생기고 `voice/index.json` 목록에 자동으로 추가됩니다.
4. 폴더 전체를 서버에 다시 올리면 → 앱 [설정] → "AI 음성 팩 받기"에서 [받기].
   한 번 받으면 휴대폰에 저장되어 인터넷 없이 재생됩니다.
5. 서버 없이 나눠 줄 때: `voice/<음성팩>` 폴더의 파일을 휴대폰으로 보내고, 앱에서 "음성 팩 파일 열기"로 pack.json과 음성 파일을 함께 선택.
- 언어 파일 문장을 고치면 음성 팩도 다시 만들어야 합니다(`--version 2`처럼 숫자를 올리면 앱에서 업데이트됨).
- 만든 음성을 공개 배포할 때는 사용한 음성 엔진의 이용 약관을 확인하세요.

추천 음성: ko Yuna / ko-KR-SunHiNeural · en Ava / en-US-AvaNeural · ja Kyoko / ja-JP-NanamiNeural · zh-CN Tingting / zh-CN-XiaoxiaoNeural · id Damayanti / id-ID-GadisNeural · es Mónica / es-ES-ElviraNeural

## 6. 앱을 고친 뒤
`sw.js` 첫 줄의 `VERSION` 값(bridge-v2 → bridge-v3)을 올려야 설치된 휴대폰에도 새 버전이 반영됩니다.

## 성경 번역본
개역개정(한국어), ESV(English), 口語訳(日本語), 和合本(简体中文), Terjemahan Baru(Bahasa Indonesia), Reina-Valera 1960(Español).
배포 전에 각 언어 원어민·사역자에게 구절과 문장을 한 번 검토받기를 권합니다.
