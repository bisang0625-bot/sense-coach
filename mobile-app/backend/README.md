# Sense Coach Mobile App - Backend

FastAPI 기반 백엔드 서버

## 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
export GEMINI_API_KEY="your_api_key_here"

# 서버 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API 문서
서버 실행 후 http://localhost:8000/docs 에서 Swagger UI 확인 가능
