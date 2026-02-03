# Render.com 배포 가이드

## 1. GitHub에 코드 업로드

이 `backend` 폴더를 GitHub 저장소에 업로드하세요.

## 2. Render.com 설정

1. https://render.com 에서 무료 계정 생성
2. "New Web Service" 클릭
3. GitHub 저장소 연결
4. 설정:
   - **Name**: sense-coach-api
   - **Root Directory**: mobile-app/backend
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 3. 환경 변수 설정

Render 대시보드에서 Environment 탭에 추가:
- `GEMINI_API_KEY`: [Google AI Studio에서 발급받은 API 키]

## 4. 배포

"Create Web Service" 클릭하면 자동 배포됩니다.

배포 완료 후 URL 예시: `https://sense-coach-api.onrender.com`
