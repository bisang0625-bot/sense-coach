# Sense Coach Mobile App - React Native Frontend

## 다음 단계
React Native 프로젝트는 다음 명령어로 생성합니다:

```bash
cd mobile-app/frontend
npx react-native init SenseCoach
cd SenseCoach
npm install react-native-webview axios
```

## 주요 화면
1. **HomeScreen** - 분석 입력 화면
2. **ResultScreen** - 분석 결과 화면
3. **DashboardScreen** - 일정 대시보드
4. **SettingsScreen** - 설정 화면

## API 연동
`mobile-app/backend/main.py`의 FastAPI 서버와 연동합니다.
