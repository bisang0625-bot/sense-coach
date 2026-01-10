1. Project Overview
Project Name: Vibe Curator (Global School Alert Summarizer)

Objective: 해외 거주 한인 부모를 위해 복잡한 학교 알림장을 분석하고, 현지 문화 맥락을 반영한 '준비물 & 액션 아이템' 요약 제공.

Target User: 네덜란드, 미국 등 해외 거주 한국인 학부모.

2. Tech Stack
Language: Python 3.10+

Frontend/Hosting: Streamlit (UI 구현 및 배포가 가장 빠름)

AI Engine: OpenAI gpt-4o-mini (속도 및 비용 효율성) 및 gpt-4o (이미지 분석용)

Environment: .env를 통한 API Key 관리

3. Core Features (MVP)
국가 설정 (Country Selector): 사이드바에서 네덜란드, 미국, 독일, 영국, 기타 국가 선택.

알림장 입력:

텍스트 붙여넣기 기능.

이미지(스크린샷) 업로드 및 OCR 분석 기능.

AI 요약 엔진:

[Must-Have] 행사 날짜 및 시간.

[Must-Have] 준비물 체크리스트 (현지 용어 + 한국어 설명).

[Unique Value] 문화적 맥락 설명 (예: "네덜란드에서 Studiedag는 아이들이 등교하지 않는 날입니다.").

결과 시각화: 깔끔한 카드 형태의 UI와 복사하기 버튼.