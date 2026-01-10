# 📁 프로젝트 파일 구조 (Project Structure)

눈치코치(Sense Coach) 프로젝트의 전체 파일 구조와 각 파일의 역할을 설명합니다.

---

## 📂 루트 디렉토리

```
Vibe Curator (Global School Alert Summarizer)/
├── app.py                          # 메인 Streamlit 애플리케이션
├── requirements.txt                # Python 의존성 패키지 목록
├── Dockerfile                      # Docker 컨테이너 설정
├── school_events.db               # SQLite 데이터베이스 (자동 생성)
│
├── PRD.md                          # 프로젝트 요구사항 문서
├── README.md                       # 프로젝트 소개 및 사용 가이드
│
├── APP_STORE_GUIDE.md             # 앱스토어 등록 완벽 가이드
├── DEPLOYMENT.md                   # 클라우드 배포 가이드
├── SUBMISSION_CHECKLIST.md         # 앱스토어 제출 체크리스트
├── ICON_GUIDE.md                   # 앱 아이콘 제작 가이드
├── SCREENSHOT_GUIDE.md             # 스크린샷 촬영 가이드
│
├── app_descriptions.md             # 앱스토어 설명 템플릿
├── app_store_metadata.json         # 앱스토어 메타데이터
├── privacy-policy.md               # 개인정보 처리방침
│
├── .streamlit/                     # Streamlit 설정 폴더
│   └── config.toml                 # Streamlit 테마 및 서버 설정
│
├── .env                            # 환경 변수 (Git 제외)
├── .gitignore                      # Git 무시 파일 목록
│
└── venv/                           # Python 가상 환경 (Git 제외)
```

---

## 📄 주요 파일 설명

### 핵심 애플리케이션 파일

#### `app.py`
- **역할**: 메인 Streamlit 애플리케이션
- **기능**:
  - UI 렌더링 (분석하기, 나의 일정 탭)
  - Google Gemini API 호출
  - 데이터베이스 관리 (SQLite3)
  - 이미지 처리 및 분석
  - 일정 저장, 수정, 삭제
  - 자녀 관리
  - 설정 관리
- **라인 수**: ~1900줄
- **주요 함수**:
  - `init_database()`: DB 초기화
  - `analyze_with_gemini()`: AI 분석
  - `parse_analysis_result()`: 결과 파싱
  - `render_dashboard()`: 대시보드 렌더링
  - `main()`: 메인 함수

#### `requirements.txt`
- **역할**: Python 패키지 의존성 목록
- **내용**:
  ```
  streamlit
  google-generativeai>=0.8.0
  python-dotenv
  Pillow
  ```

#### `school_events.db`
- **역할**: SQLite 데이터베이스
- **테이블**:
  - `events`: 저장된 일정
  - `checklist_items`: 준비물 체크리스트
  - `children`: 자녀 정보
- **생성**: 앱 실행 시 자동 생성
- **위치**: 로컬 저장 (Git 제외)

---

### 설정 파일

#### `.env`
- **역할**: 환경 변수 저장
- **내용**:
  ```
  GEMINI_API_KEY=your_api_key_here
  ```
- **보안**: Git에 커밋하지 않음 (.gitignore에 포함)

#### `.streamlit/config.toml`
- **역할**: Streamlit 테마 및 서버 설정
- **설정**:
  - Primary Color: #FFB6C1 (파스텔 핑크)
  - Background Color: #FFFFFF
  - Font: sans serif
  - Server port: 8501

#### `.gitignore`
- **역할**: Git 버전 관리에서 제외할 파일 지정
- **제외 항목**:
  - `.env` (API 키)
  - `venv/` (가상 환경)
  - `*.db` (데이터베이스)
  - `__pycache__/`

---

### 문서 파일

#### 프로젝트 문서

**`PRD.md`** (Product Requirements Document)
- 프로젝트 개요
- 목표 사용자
- 기술 스택
- 핵심 기능

**`README.md`**
- 프로젝트 소개
- 설치 및 실행 방법
- 주요 기능 설명
- 사용법 가이드
- 기술 스택
- 기여 방법

#### 앱스토어 등록 가이드

**`APP_STORE_GUIDE.md`** (📘 가장 중요!)
- 앱스토어 등록 전체 프로세스
- iOS App Store 등록 상세 가이드
- Google Play Store 등록 상세 가이드
- 필요한 자료 목록
- 비용 안내
- 타임라인

**`DEPLOYMENT.md`**
- Streamlit Cloud 배포
- Docker 배포
- AWS EC2 배포
- 환경 변수 설정
- 도메인 연결
- SSL 인증서

**`SUBMISSION_CHECKLIST.md`**
- 단계별 체크리스트
- 사전 준비 항목
- 그래픽 자료 준비
- 메타데이터 준비
- 네이티브 앱 개발
- 제출 절차

**`ICON_GUIDE.md`**
- 필요한 아이콘 크기
- 디자인 가이드라인
- 아이콘 아이디어
- 제작 도구 및 방법
- 자동 리사이징

**`SCREENSHOT_GUIDE.md`**
- 필요한 스크린샷 개수
- 필요한 해상도
- 촬영할 화면 리스트
- 디자인 가이드
- 촬영 방법
- 도구 추천

#### 앱스토어 콘텐츠

**`app_descriptions.md`**
- iOS App Store 설명 (한국어/영어)
- Google Play Store 설명 (한국어/영어)
- 프로모션 텍스트
- 키워드

**`app_store_metadata.json`**
- 앱 메타데이터 (구조화된 JSON)
- 앱 이름, 부제목, 설명
- 카테고리, 연령 등급
- 지원 URL, 개인정보 처리방침 URL
- 기능 리스트
- 스크린샷 위치
- 권한 설정

**`privacy-policy.md`**
- 개인정보 처리방침 (한국어/영어)
- 수집하는 정보
- 사용 목적
- 제3자 제공
- 보안 조치
- 사용자 권리

---

### 배포 파일

#### `Dockerfile`
- **역할**: Docker 컨테이너 설정
- **내용**:
  - Python 3.9 이미지 기반
  - 의존성 설치
  - Streamlit 설정
  - 포트 8501 노출
  - 앱 실행 명령

---

## 🆕 앱스토어 등록을 위해 추가된 파일

이번에 추가된 파일들은 앱스토어 등록을 위한 완벽한 가이드를 제공합니다:

1. **APP_STORE_GUIDE.md** (15KB)
   - 앱스토어 등록 전체 프로세스
   - iOS/Android 등록 상세 가이드

2. **DEPLOYMENT.md** (12KB)
   - 클라우드 배포 방법
   - Streamlit Cloud, Docker, AWS

3. **SUBMISSION_CHECKLIST.md** (18KB)
   - 단계별 체크리스트
   - 진행 상황 추적

4. **ICON_GUIDE.md** (16KB)
   - 앱 아이콘 제작 완벽 가이드
   - 모든 크기 요구사항

5. **SCREENSHOT_GUIDE.md** (14KB)
   - 스크린샷 촬영 가이드
   - 디자인 팁

6. **app_descriptions.md** (10KB)
   - 앱스토어 설명 템플릿
   - 한국어/영어

7. **app_store_metadata.json** (4KB)
   - 구조화된 메타데이터
   - JSON 형식

8. **privacy-policy.md** (15KB)
   - 개인정보 처리방침
   - 한국어/영어

9. **Dockerfile** (1KB)
   - Docker 컨테이너 설정

10. **.streamlit/config.toml** (0.2KB)
    - Streamlit 테마 설정

---

## 📂 권장 폴더 구조 (앱스토어 등록 시)

앱스토어 등록을 위해 다음 폴더를 추가로 생성하는 것을 권장합니다:

```
Vibe Curator (Global School Alert Summarizer)/
│
├── assets/                         # 앱스토어 자료
│   ├── app_icon/                   # 앱 아이콘
│   │   ├── original/               # 원본 디자인 파일
│   │   │   ├── icon_design.psd
│   │   │   ├── icon_design.ai
│   │   │   └── icon_design.fig
│   │   ├── ios/                    # iOS용 아이콘
│   │   │   ├── icon_1024.png      # App Store
│   │   │   ├── icon_180.png
│   │   │   ├── icon_120.png
│   │   │   └── ...
│   │   └── android/                # Android용 아이콘
│   │       ├── icon_512.png       # Play Store
│   │       ├── icon_192.png
│   │       └── ...
│   │
│   └── screenshots/                # 스크린샷
│       ├── ios/
│       │   ├── iphone_6.7/
│       │   │   ├── 01_main_screen_ko.png
│       │   │   ├── 02_text_input_ko.png
│       │   │   └── ...
│       │   └── ipad_pro_12.9/
│       └── android/
│           ├── phone/
│           └── tablet/
│
├── mobile_app/                     # 모바일 앱 코드 (추가 예정)
│   ├── ios/                        # iOS 네이티브 코드
│   ├── android/                    # Android 네이티브 코드
│   └── shared/                     # 공통 코드
│
└── docs/                           # 추가 문서 (선택)
    ├── api_docs.md
    ├── changelog.md
    └── contributing.md
```

---

## 🔄 파일 업데이트 이력

### 2026-01-10
- ✅ 앱스토어 등록 관련 문서 9개 추가
- ✅ README.md 업데이트 (앱 이름, 구조 개선)
- ✅ Streamlit 설정 파일 추가
- ✅ Docker 설정 파일 추가

### 이전
- 2026-01-09: 준비물 % 계산 제거
- 2026-01-08: 앱 이름 변경 (눈치코치)
- 2026-01-07: 모바일 반응형 디자인 개선
- 2026-01-06: 체크리스트 검증 로직 추가
- 2026-01-05: 편집 기능 개선
- 2026-01-04: 메모 기능 추가
- 2026-01-03: 대시보드 UI 개선

---

## 📝 다음 단계

### 즉시 할 수 있는 것
1. ✅ `README.md` 읽기
2. ✅ `.env` 파일 생성 및 API 키 설정
3. ✅ 앱 로컬 실행 테스트

### 배포 준비
1. ⏳ `DEPLOYMENT.md` 참고하여 클라우드 배포
2. ⏳ 도메인 구매 (선택)
3. ⏳ HTTPS 설정

### 앱스토어 등록
1. ⏳ `SUBMISSION_CHECKLIST.md` 확인
2. ⏳ `ICON_GUIDE.md` 참고하여 아이콘 제작
3. ⏳ `SCREENSHOT_GUIDE.md` 참고하여 스크린샷 촬영
4. ⏳ `APP_STORE_GUIDE.md` 따라 단계별 진행

---

## 💡 팁

### 파일 찾기
- **앱스토어 등록 시작**: `SUBMISSION_CHECKLIST.md` 먼저 읽기
- **배포 방법**: `DEPLOYMENT.md`
- **아이콘 만들기**: `ICON_GUIDE.md`
- **스크린샷 촬영**: `SCREENSHOT_GUIDE.md`
- **앱 설명 작성**: `app_descriptions.md`

### 개발
- **메인 코드**: `app.py`
- **환경 설정**: `.env`, `.streamlit/config.toml`
- **의존성**: `requirements.txt`

### 문서
- **프로젝트 소개**: `README.md`
- **기능 명세**: `PRD.md`
- **개인정보 정책**: `privacy-policy.md`

---

## 📞 문의

파일 구조나 특정 파일에 대해 궁금한 점이 있으시면:
- 이메일: support@sensecoach.app
- GitHub Issues: (저장소 URL)

---

**Last Updated**: 2026년 1월 10일
