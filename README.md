# 📚 눈치코치 - Sense Coach

> 현지 학교 알림장의 행간을 읽어주는 AI 문화 비서

해외 거주 한인 부모를 위한 스마트 학교 알림장 분석 앱입니다. 복잡한 학교 알림장을 AI가 자동으로 분석하여, 일정·준비물·문화적 배경까지 한번에 정리해 드립니다.

## 🚀 시작하기

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 Google Gemini API 키를 입력하세요:

`.env` 파일 내용:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

**API 키 발급 방법:**
1. [Google AI Studio](https://makersuite.google.com/app/apikey)에 접속
2. Google 계정으로 로그인
3. "Create API Key" 버튼 클릭
4. 생성된 API 키를 복사하여 `.env` 파일에 입력

**또는 Streamlit Secrets 사용:**
Streamlit Cloud에 배포하는 경우, `st.secrets`에 `GEMINI_API_KEY`를 설정할 수 있습니다.

### 3. 앱 실행

```bash
streamlit run app.py
```

## ✨ 주요 기능

### 📝 자동 분석
- **텍스트 입력**: 알림장 내용을 복사 붙여넣기
- **이미지 업로드**: 사진을 찍어서 업로드하면 자동 인식
- **Vision AI**: Google Gemini의 강력한 Vision 기능으로 정확한 텍스트 추출

### 📅 스마트 일정 관리
- **자동 추출**: 행사명, 날짜, 시간을 AI가 자동으로 파악
- **자녀별 관리**: 여러 자녀의 일정을 따로 관리
- **D-day 카운터**: 다가오는 일정을 놓치지 않도록 알림
- **메모 기능**: 추가 정보를 메모로 저장

### ✅ 준비물 체크리스트
- **자동 생성**: 필요한 준비물을 리스트로 자동 정리
- **진행률 표시**: 준비 상황을 시각적으로 확인
- **체크박스**: 하나씩 체크하며 준비

### 💡 문화적 배경 설명
- **국가별 맞춤**: 네덜란드, 미국, 독일, 영국 등 국가별 교육 문화 반영
- **현지 맥락**: "이 행사는 이 나라에서 이런 의미예요"
- **실용적인 팁**: 학부모가 알아야 할 실질적인 조언

### 📊 대시보드
- **다가오는 일정**: 예정된 이벤트를 한눈에 확인
- **지난 일정**: 과거 일정 자동 아카이브
- **상세 정보**: 각 일정의 세부 내용 관리
- **편집 기능**: 일정 수정, 삭제, 메모 추가

## 🎨 디자인

깔끔하고 따뜻한 파스텔톤 스타일을 적용하여 사용자 친화적인 UI를 제공합니다.

## 🎯 사용법

### 간단한 3단계!

1. **입력**: 알림장 텍스트를 입력하거나 사진을 업로드
2. **분석**: '분석하기' 버튼 클릭
3. **저장**: 결과 확인 후 '내 일정에 저장하기'

### 상세 가이드

1. **설정하기**
   - 사이드바에서 국가 선택 (네덜란드, 미국, 독일, 영국 등)
   - 자녀 이름 추가 (여러 자녀 관리 가능)

2. **분석하기 탭**
   - 텍스트 입력: 알림장 내용을 복사하여 붙여넣기
   - 이미지 업로드: 사진을 찍어서 업로드 (JPG, PNG)
   - '분석하기' 버튼 클릭

3. **결과 확인**
   - 📌 행사명
   - 📅 일시
   - ✅ 준비물 체크리스트
   - 💡 문화적 배경
   - 🔍 실용적인 팁
   - 🌐 원문 번역 (접어서 표시)

4. **일정 저장**
   - 자녀 선택 (첫째, 둘째 등)
   - '내 일정에 저장하기' 클릭
   - 🎉 저장 완료!

5. **나의 일정 탭**
   - 다가오는 일정: D-day와 함께 표시
   - 준비물 체크: 하나씩 체크하며 준비
   - 일정 편집: 날짜, 시간, 준비물, 메모 수정
   - 일정 삭제: 불필요한 일정 제거

## 🔧 기술 스택

### Backend
- **Python 3.9+**: 코어 언어
- **Streamlit**: 웹 프레임워크
- **SQLite3**: 로컬 데이터베이스
- **Python-dotenv**: 환경 변수 관리

### AI
- **Google Gemini API**: AI 분석 엔진
  - `gemini-1.5-flash`: 빠른 분석
  - `gemini-1.5-pro`: 정확한 분석
  - Vision AI: 이미지 텍스트 추출
  - Multimodal: 텍스트 + 이미지 동시 처리

### UI/UX
- **Custom CSS**: 모바일 최적화 디자인
- **Pastel Theme**: 따뜻하고 친근한 파스텔톤
- **Responsive**: 스마트폰, 태블릿, 데스크톱 지원

---

## 📱 모바일 앱 버전

눈치코치는 웹앱으로 시작하여, iOS App Store와 Google Play Store로 확장 예정입니다.

### 앱스토어 등록 가이드
자세한 내용은 다음 문서를 참고하세요:
- 📘 [`APP_STORE_GUIDE.md`](APP_STORE_GUIDE.md) - 앱스토어 등록 완벽 가이드
- 📦 [`DEPLOYMENT.md`](DEPLOYMENT.md) - 클라우드 배포 가이드
- ✅ [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) - 제출 체크리스트
- 🎨 [`ICON_GUIDE.md`](ICON_GUIDE.md) - 앱 아이콘 제작 가이드
- 📸 [`SCREENSHOT_GUIDE.md`](SCREENSHOT_GUIDE.md) - 스크린샷 촬영 가이드
- 📝 [`app_descriptions.md`](app_descriptions.md) - 앱 설명 템플릿
- 🔒 [`privacy-policy.md`](privacy-policy.md) - 개인정보 처리방침

---

## 🌍 지원 국가

현재 다음 국가의 교육 문화를 지원합니다:
- 🇳🇱 **네덜란드**: Studiedag, Sinterklaas 등 현지 행사 설명
- 🇺🇸 **미국**: PTA, Field Trip, Thanksgiving 등
- 🇩🇪 **독일**: Schultüte, Elternabend 등
- 🇬🇧 **영국**: Parents' Evening, School Uniform 등
- 🌏 **기타 국가**: 일반적인 학교 문화 분석

더 많은 국가가 곧 추가될 예정입니다!

---

## 🤝 기여하기

이 프로젝트는 오픈소스입니다. 기여를 환영합니다!

### 기여 방법
1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 이슈 리포트
버그를 발견하거나 기능 제안이 있으신가요?
[GitHub Issues](https://github.com/yourusername/sense-coach/issues)에서 알려주세요!

---

## 📞 문의 및 지원

- **이메일**: support@sensecoach.app
- **웹사이트**: https://sensecoach.app (준비 중)
- **GitHub**: https://github.com/yourusername/sense-coach

---

## 📄 라이선스

이 프로젝트는 개인 사용 및 교육 목적으로 만들어졌습니다.
상업적 사용을 원하시면 별도로 연락 주세요.

---

## 🙏 감사의 말

이 앱은 해외에서 자녀를 키우며 학교 알림장 때문에 고생하는 
모든 한인 부모님들을 위해 만들어졌습니다.

여러분의 피드백과 응원이 앱을 더 좋게 만듭니다. 
감사합니다! 💖

---

**Made with ❤️ for Korean parents living abroad**
