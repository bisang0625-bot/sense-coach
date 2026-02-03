# 📱 눈치코치(Sense Coach) 앱스토어 등록 가이드

## 📋 목차
1. [개요](#개요)
2. [배포 전략](#배포-전략)
3. [iOS App Store 등록](#ios-app-store-등록)
4. [Google Play Store 등록](#google-play-store-등록)
5. [필요한 자료](#필요한-자료)
6. [비용 안내](#비용-안내)

---

## 개요

**눈치코치(Sense Coach)**는 현재 Streamlit 기반 웹앱입니다. 앱스토어에 등록하기 위해서는 다음 두 가지 방법 중 하나를 선택해야 합니다:

### 방법 1: 웹뷰 래퍼 앱 (추천)
- **장점**: 빠른 개발, 기존 코드 재사용, 업데이트 용이
- **단점**: 네이티브 기능 제한적
- **도구**: React Native WebView, Flutter WebView, PWA

### 방법 2: 네이티브 앱 재개발
- **장점**: 최고의 성능과 UX, 모든 네이티브 기능 사용 가능
- **단점**: 개발 시간과 비용이 많이 소요
- **도구**: React Native, Flutter, Swift/Kotlin

**이 가이드는 방법 1(웹뷰 래퍼)을 기준으로 작성되었습니다.**

---

## 배포 전략

### 1단계: Streamlit 앱 클라우드 배포
현재 로컬에서 실행되는 앱을 먼저 클라우드에 배포해야 합니다.

#### 옵션 A: Streamlit Cloud (무료, 가장 쉬움)
```bash
# 1. GitHub 저장소 생성 및 푸시
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/sense-coach.git
git push -u origin main

# 2. Streamlit Cloud에서 배포
# https://streamlit.io/cloud 방문
# GitHub 계정 연동 후 앱 배포
```

**Streamlit Cloud 설정:**
- Secrets에 `GEMINI_API_KEY` 추가
- Python 버전: 3.9+
- Main file: `app.py`

#### 옵션 B: AWS/Azure/GCP (유료, 더 많은 제어)
```bash
# Docker를 사용한 배포 예시
docker build -t sense-coach .
docker run -p 8501:8501 sense-coach
```

### 2단계: 도메인 및 HTTPS 설정
- 커스텀 도메인 구매 (예: sensecoach.app)
- SSL 인증서 설정 (Let's Encrypt 무료)
- 앱스토어는 HTTPS 필수

### 3단계: PWA 변환 (선택사항이지만 권장)
PWA로 만들면 설치 가능한 웹앱이 되어 네이티브 앱과 유사한 경험 제공

---

## iOS App Store 등록

### 준비 사항

#### 1. Apple Developer Program 가입
- **비용**: 연간 $99 (₩132,000)
- **가입**: https://developer.apple.com/programs/
- **필요 정보**: Apple ID, 신용카드, 사업자등록번호(법인의 경우)

#### 2. 개발 도구
- macOS 컴퓨터 (필수)
- Xcode 최신 버전
- CocoaPods 또는 Swift Package Manager

#### 3. 웹뷰 앱 생성 (React Native 예시)

**프로젝트 생성:**
```bash
# React Native CLI 설치
npm install -g react-native-cli

# 프로젝트 생성
npx react-native init SenseCoach
cd SenseCoach

# WebView 라이브러리 설치
npm install react-native-webview
```

**App.js 코드:**
```javascript
import React from 'react';
import { SafeAreaView, StyleSheet } from 'react-native';
import { WebView } from 'react-native-webview';

const App = () => {
  return (
    <SafeAreaView style={styles.container}>
      <WebView
        source={{ uri: 'https://your-streamlit-app-url.com' }}
        style={styles.webview}
        javaScriptEnabled={true}
        domStorageEnabled={true}
        startInLoadingState={true}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFB6C1',
  },
  webview: {
    flex: 1,
  },
});

export default App;
```

#### 4. 앱 아이콘 준비
**필요한 크기:**
- 1024x1024 (App Store용)
- 180x180 (iPhone)
- 167x167 (iPad Pro)
- 152x152 (iPad)
- 120x120 (iPhone 작은 크기)
- 87x87, 80x80, 76x76, 60x60, 58x58, 40x40, 29x29, 20x20

**도구**: https://appicon.co/

#### 5. 스크린샷 준비
**필요한 해상도:**
- iPhone 6.7" (1290 x 2796) - 최소 3장
- iPhone 6.5" (1242 x 2688)
- iPhone 5.5" (1242 x 2208)
- iPad Pro 12.9" (2048 x 2732)

#### 6. App Store Connect 설정
**앱 정보:**
```
앱 이름: 눈치코치 - Sense Coach
부제목: 현지 학교 알림장 행간 읽기 AI 비서
카테고리: 교육(Education) > 가족
연령 등급: 4+
가격: 무료 (또는 유료 설정)
```

**설명 (한국어):**
```
📚 해외 거주 한인 부모를 위한 스마트 학교 알림장 비서

눈치코치는 현지 학교의 복잡한 알림장을 단 몇 초 만에 분석하여 
핵심 정보만 간추려 드립니다.

✨ 주요 기능:
• 📝 텍스트 및 이미지 자동 분석
• 📅 일정 자동 추출 및 저장
• ✅ 준비물 체크리스트 생성
• 💡 현지 문화 맥락 설명
• 👶 자녀별 일정 관리
• 📊 스마트 대시보드

🌍 지원 국가:
네덜란드, 미국, 독일, 영국 및 기타 국가

🤖 AI 기술:
Google Gemini의 최신 Vision AI를 활용하여 
정확한 분석과 번역을 제공합니다.
```

**키워드:**
```
학교알림장, 학교공지, 교육, 해외생활, 이민, 육아, 학부모, AI비서, 번역, 일정관리
```

#### 7. 개인정보 처리방침
**필수**: 웹사이트에 개인정보 처리방침 게시 필요
- 수집하는 정보: Gemini API 사용 로그, 저장된 일정
- 사용 목적: 서비스 제공
- 보관 기간: 사용자 삭제 시까지
- 제3자 제공: Google (Gemini API)

#### 8. 심사 제출
**체크리스트:**
- [ ] 테스트 계정 제공 (API 키 포함)
- [ ] 개인정보 처리방침 URL
- [ ] 지원 URL 또는 이메일
- [ ] 스크린샷 업로드
- [ ] 앱 미리보기 영상 (선택사항)
- [ ] 메타데이터 작성

**심사 기간**: 평균 1-3일

---

## Google Play Store 등록

### 준비 사항

#### 1. Google Play Console 가입
- **비용**: 일회성 $25 (₩33,000)
- **가입**: https://play.google.com/console/signup
- **필요 정보**: Google 계정, 신용카드

#### 2. 안드로이드 앱 생성

**프로젝트 생성 (React Native):**
```bash
# 이미 생성된 경우 동일한 프로젝트 사용
cd SenseCoach

# Android 빌드
npx react-native run-android
```

**AndroidManifest.xml 권한 설정:**
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

#### 3. 앱 아이콘 준비
**필요한 크기:**
- 512x512 (Play Store용)
- 192x192, 144x144, 96x96, 72x72, 48x48 (앱 내 사용)

#### 4. 스크린샷 준비
**필요한 해상도:**
- 휴대전화: 1080 x 1920 이상 - 최소 2장
- 7인치 태블릿: 1024 x 1600 이상
- 10인치 태블릿: 1280 x 1920 이상

#### 5. 앱 서명 및 AAB 생성
```bash
# 키스토어 생성
keytool -genkeypair -v -storetype PKCS12 -keystore sense-coach.keystore \
  -alias sense-coach -keyalg RSA -keysize 2048 -validity 10000

# AAB(Android App Bundle) 생성
cd android
./gradlew bundleRelease
```

#### 6. Play Console 설정
**앱 정보:**
```
앱 이름: 눈치코치 - Sense Coach
짧은 설명: 현지 학교 알림장 AI 비서
카테고리: 교육
콘텐츠 등급: 모든 연령
가격: 무료
```

**자세한 설명:**
```
📚 해외 거주 한인 부모를 위한 스마트 학교 알림장 비서

현지 학교에서 받은 복잡한 알림장, 이제 걱정하지 마세요!
눈치코치가 AI로 자동 분석하여 중요한 정보만 쏙쏙 정리해 드립니다.

✨ 주요 기능
━━━━━━━━━━━━━━━━
📝 텍스트 및 사진 자동 분석
   - 학교 알림장을 텍스트로 입력하거나 사진으로 찍어 올리세요
   - Google Gemini AI가 즉시 분석합니다

📅 일정 자동 추출 및 저장
   - 행사명, 날짜, 시간을 자동으로 파악
   - 내 일정에 바로 저장

✅ 준비물 체크리스트
   - 필요한 준비물을 리스트로 정리
   - 체크박스로 하나씩 확인

💡 현지 문화 맥락 설명
   - "이 행사는 이 나라에서 이런 의미예요"
   - 처음 접하는 학교 문화도 쉽게 이해

👶 자녀별 일정 관리
   - 여러 자녀의 일정을 따로 관리
   - 아이 이름으로 구분된 일정표

📊 스마트 대시보드
   - 다가오는 일정 한눈에 보기
   - D-day 카운터로 일정 놓치지 않기
   - 메모 기능으로 추가 정보 기록

🌍 지원 국가
━━━━━━━━━━━━━━━━
네덜란드, 미국, 독일, 영국 및 기타 국가
각 나라의 교육 문화와 기념일을 고려한 분석 제공

🔒 안전한 데이터 보관
━━━━━━━━━━━━━━━━
모든 일정은 내 기기에 안전하게 저장됩니다.
```

#### 7. 콘텐츠 등급 설정
- Google Play 설문조사 작성
- 폭력성, 성적 콘텐츠 등 평가
- 교육 앱 → 대부분 "모든 연령" 등급

#### 8. 데이터 보안 섹션
- 수집하는 데이터 유형 선택
- 데이터 사용 방식 설명
- 암호화 여부 표시

#### 9. 심사 제출
**체크리스트:**
- [ ] AAB 파일 업로드
- [ ] 스크린샷 업로드
- [ ] 앱 아이콘 업로드
- [ ] 개인정보 처리방침 URL
- [ ] 콘텐츠 등급 완료
- [ ] 가격 및 배포 국가 설정

**심사 기간**: 평균 1-7일

---

## 필요한 자료

### 1. 그래픽 자료
- [ ] 앱 아이콘 (1024x1024, PNG, 투명 배경 없음)
- [ ] 스플래시 스크린 (2732x2732)
- [ ] 스크린샷 5-10장 (다양한 기능 보여주기)
- [ ] 프로모션 그래픽 (Play Store: 1024x500)
- [ ] 앱 미리보기 영상 (15-30초, 선택사항)

### 2. 텍스트 자료
- [ ] 앱 이름 및 부제목
- [ ] 짧은 설명 (80자)
- [ ] 자세한 설명 (4000자)
- [ ] 키워드 (100자)
- [ ] 새로운 기능 설명
- [ ] 지원 정보 (이메일, 웹사이트)

### 3. 법적 문서
- [ ] 개인정보 처리방침
- [ ] 서비스 이용약관
- [ ] 데이터 보안 정책
- [ ] 저작권 정보

### 4. 기술 자료
- [ ] 서버 URL (Streamlit 앱)
- [ ] API 키 관리 계획
- [ ] 에러 로깅 시스템
- [ ] 앱 버전 관리 계획

---

## 비용 안내

### 개발 비용

#### 직접 개발 (DIY)
- Apple Developer: $99/년
- Google Play: $25 (일회성)
- 도메인: $10-30/년
- 호스팅 (Streamlit Cloud 무료 또는 AWS): $0-50/월
- **총 예상 비용: $134 초기 + $100-700/년**

#### 외주 개발
- 웹뷰 래퍼 앱: $2,000-5,000
- 네이티브 앱 재개발: $10,000-50,000+
- 유지보수: $500-2,000/월

### 운영 비용
- API 사용료 (Gemini): $0-100/월 (사용량에 따라)
- 서버 호스팅: $0-100/월
- Apple Developer: $99/년
- 마케팅: 선택사항

---

## 다음 단계

### 즉시 시작 가능한 작업
1. ✅ GitHub 저장소 생성 및 코드 업로드
2. ✅ Streamlit Cloud에 앱 배포
3. ✅ 앱 아이콘 디자인 의뢰 또는 생성
4. ✅ 스크린샷 촬영 및 편집
5. ✅ 개인정보 처리방침 작성

### 전문가 도움이 필요한 작업
- 네이티브 앱 개발 (React Native/Flutter)
- 그래픽 디자인 (아이콘, 스크린샷)
- 법률 검토 (개인정보 처리방침)
- 앱 마케팅

### 추천 타임라인
- **1주차**: 클라우드 배포, 도메인 설정
- **2주차**: React Native 웹뷰 앱 개발
- **3주차**: 그래픽 자료 준비, 문서 작성
- **4주차**: Apple/Google 계정 생성, 앱 제출
- **5-6주차**: 심사 대기 및 피드백 반영
- **7주차**: 앱 출시 🎉

---

## 참고 링크

### 공식 문서
- [Apple App Store 심사 가이드라인](https://developer.apple.com/app-store/review/guidelines/)
- [Google Play Console 도움말](https://support.google.com/googleplay/android-developer)
- [React Native 공식 문서](https://reactnative.dev/docs/getting-started)

### 도구
- [Streamlit Cloud](https://streamlit.io/cloud)
- [App Icon Generator](https://appicon.co/)
- [Screenshot Designer](https://www.applaunchpad.com/)
- [Privacy Policy Generator](https://www.privacypolicies.com/)

### 커뮤니티
- [Streamlit Community](https://discuss.streamlit.io/)
- [React Native Discord](https://www.reactnative.dev/community/overview)
- [IndieHackers - 앱 출시](https://www.indiehackers.com/)

---

---
 
 ## 🚀 앱 성능 최적화 (중요)
 
 Streamlit 기반 앱은 초기 로딩 속도 이슈("Cold Start")가 발생할 수 있습니다. 사용자 이탈을 막기 위해 다음 조치를 권장합니다.
 
 ### 1. 서버 상시 가동 유지
 - **필수 조치**: `DEPLOYMENT.md`의 "Streamlit 'Cold Start' 방지" 섹션을 참고하여 UptimeRobot을 설정하세요.
 - 이렇게 하면 사용자가 앱을 켰을 때 "Waking up..." 화면 없이 바로 접속됩니다.
 
 ### 2. 로딩 화면(Splash Screen) 활용
 - React Native 앱 실행 직후 웹사이트가 로딩되는 동안 빈 화면이 보일 수 있습니다.
 - `react-native-splash-screen` 라이브러리를 사용하여 로딩이 완료될 때까지 예쁜 로고 화면을 보여주세요.
 
 ```javascript
 // App.js 예시
 import SplashScreen from 'react-native-splash-screen';
 
 const App = () => {
   useEffect(() => {
     // 웹뷰 로딩 완료 후 숨김
     SplashScreen.hide();
   }, []);
   
   // ...
 };
 ```
 
 ---
 
 ## 문의사항
추가 질문이 있으시면 다음 리소스를 활용하세요:
- Apple Developer Support
- Google Play Developer Support
- Streamlit Community Forum
