# 🚀 배포 가이드 (Deployment Guide)

이 문서는 눈치코치(Sense Coach) 앱을 클라우드에 배포하는 방법을 안내합니다.

---

## 📋 목차
1. [Streamlit Cloud 배포 (무료, 권장)](#streamlit-cloud-배포)
2. [Docker를 사용한 배포](#docker를-사용한-배포)
3. [AWS EC2 배포](#aws-ec2-배포)
4. [환경 변수 설정](#환경-변수-설정)
5. [도메인 연결](#도메인-연결)

---

## Streamlit Cloud 배포

Streamlit Cloud는 Streamlit 앱을 무료로 배포할 수 있는 가장 쉬운 방법입니다.

### 1단계: GitHub 저장소 생성

```bash
# Git 초기화 (아직 안 한 경우)
git init

# .gitignore 확인 (민감 정보 제외)
# .env 파일이 .gitignore에 포함되어 있는지 확인

# 파일 추가 및 커밋
git add .
git commit -m "Initial commit for Sense Coach app"

# GitHub 원격 저장소 생성 후 연결
git remote add origin https://github.com/bisang0625/sense-coach.git
git branch -M main
git push -u origin main
```

### 2단계: Streamlit Cloud 설정

1. **Streamlit Cloud 접속**
   - https://streamlit.io/cloud 방문
   - GitHub 계정으로 로그인

2. **새 앱 생성**
   - "New app" 클릭
   - Repository: `bisang0625/sense-coach` 선택
   - Branch: `main`
   - Main file path: `app.py`

3. **Advanced settings 클릭**
   - Python version: `3.9`

4. **Secrets 설정**
   - "Secrets" 섹션에 다음 내용 입력:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```

5. **Deploy! 클릭**
   - 몇 분 후 앱이 배포됩니다
   - URL: `https://yourusername-sense-coach-app-xxxxx.streamlit.app`

### 3단계: 배포 확인

- 배포된 URL로 접속하여 앱이 정상 작동하는지 확인
- 모든 기능 테스트:
  - 텍스트 분석
  - 이미지 업로드 및 분석
  - 일정 저장 및 조회
  - 대시보드 기능

---

## Docker를 사용한 배포

Docker를 사용하면 어떤 클라우드 플랫폼에서도 동일하게 실행할 수 있습니다.

### 1단계: Docker 이미지 빌드

```bash
# 프로젝트 디렉토리에서 실행
docker build -t sense-coach:latest .

# 빌드 확인
docker images
```

### 2단계: 로컬에서 테스트

```bash
# .env 파일이 있는 경우
docker run -p 8501:8501 --env-file .env sense-coach:latest

# 환경 변수를 직접 전달하는 경우
docker run -p 8501:8501 \
  -e GEMINI_API_KEY="your_api_key" \
  sense-coach:latest

# 브라우저에서 http://localhost:8501 접속
```

### 3단계: Docker Hub에 푸시 (선택사항)

```bash
# Docker Hub 로그인
docker login

# 태그 지정
docker tag sense-coach:latest yourusername/sense-coach:latest

# 푸시
docker push yourusername/sense-coach:latest
```

---

## AWS EC2 배포

### 1단계: EC2 인스턴스 생성

1. **AWS Console 접속**
   - EC2 서비스로 이동
   - "Launch Instance" 클릭

2. **인스턴스 설정**
   - Name: `sense-coach-server`
   - AMI: Ubuntu Server 22.04 LTS
   - Instance type: `t2.micro` (무료 티어) 또는 `t2.small` (권장)
   - Key pair: 새로 생성하거나 기존 것 사용
   - Security group:
     - SSH (22) - 내 IP만 허용
     - HTTP (80) - 모든 IP 허용
     - HTTPS (443) - 모든 IP 허용
     - Custom TCP (8501) - 모든 IP 허용

3. **인스턴스 시작**

### 2단계: 서버 설정

```bash
# SSH 접속
ssh -i your-key.pem ubuntu@your-ec2-public-ip

# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Docker 설치
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# 재접속 (Docker 그룹 적용)
exit
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### 3단계: 앱 배포

```bash
# Git에서 코드 가져오기
git clone https://github.com/yourusername/sense-coach.git
cd sense-coach

# 환경 변수 파일 생성
nano .env
# 내용:
# GEMINI_API_KEY=your_actual_api_key_here
# Ctrl+X, Y, Enter로 저장

# Docker 이미지 빌드
docker build -t sense-coach:latest .

# Docker 컨테이너 실행
docker run -d \
  --name sense-coach \
  --restart unless-stopped \
  -p 8501:8501 \
  --env-file .env \
  sense-coach:latest

# 상태 확인
docker ps
docker logs sense-coach
```

### 4단계: Nginx 리버스 프록시 설정 (선택사항)

```bash
# Nginx 설치
sudo apt install nginx -y

# Nginx 설정
sudo nano /etc/nginx/sites-available/sense-coach

# 내용:
```
```nginx
server {
    listen 80;
    server_name your-domain.com;  # 도메인 또는 EC2 퍼블릭 IP

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

```bash
# 설정 활성화
sudo ln -s /etc/nginx/sites-available/sense-coach /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5단계: SSL 인증서 설정 (Let's Encrypt)

```bash
# Certbot 설치
sudo apt install certbot python3-certbot-nginx -y

# SSL 인증서 발급
sudo certbot --nginx -d your-domain.com

# 자동 갱신 확인
sudo certbot renew --dry-run
```

---

## 환경 변수 설정

### Streamlit Cloud
```toml
# Secrets 메뉴에 추가
GEMINI_API_KEY = "your_api_key_here"
```

### Docker / 로컬
```bash
# .env 파일
GEMINI_API_KEY=your_api_key_here
```

### AWS / 시스템 환경 변수
```bash
# ~/.bashrc 또는 ~/.profile에 추가
export GEMINI_API_KEY="your_api_key_here"

# 적용
source ~/.bashrc
```

---
 
 ## Streamlit 'Cold Start' 방지 (필수)
 
 Streamlit Community Cloud(무료)는 앱이 일정 시간 동안 사용되지 않으면 "절전 모드"로 진입합니다. 이 경우 앱을 다시 켤 때 "Waking up..." 화면이 표시되며 30초 이상 로딩 시간이 발생합니다.
 **이는 사용자 경험에 치명적이므로, 아래 방법으로 반드시방지해야 합니다.**
 
 ### 방법 1: Keep-Alive 설정 (UptimeRobot 사용) - 무료 & 추천
 
 외부 모니터링 서비스를 사용하여 5분마다 앱을 자동으로 방문하게 하여 절전 모드 진입을 막습니다.
 
 1. **[UptimeRobot](https://uptimerobot.com/) 접속 및 무료 가입**
 2. **"Add New Monitor" 클릭**
 3. 설정 입력:
    - **Monitor Type**: `HTTP(s)`
    - **Friendly Name**: `Sense Coach App`
    - **URL (or IP)**: 배포된 Streamlit 앱 주소 (예: `https://sense-coach.streamlit.app`)
    - **Monitoring Interval**: `5 minutes` (중요!)
    - **Monitor Timeout**: `30 seconds`
 4. **"Create Monitor" 클릭**
 
 이제 UptimeRobot이 5분마다 앱을 깨워서 항상 켜져 있는 상태를 유지합니다.
 
 ---
 
 ## 도메인 연결

### Streamlit Cloud
1. Streamlit Cloud 대시보드에서 앱 선택
2. "Settings" → "Custom subdomain" 설정
3. 또는 커스텀 도메인 설정 (CNAME 레코드)

### AWS EC2 + 도메인
1. **도메인 구매** (예: Namecheap, GoDaddy)

2. **DNS 설정**
   - A 레코드 추가:
     - Name: `@` (또는 `www`)
     - Value: EC2 퍼블릭 IP
     - TTL: 300

3. **Nginx 설정 업데이트**
   ```bash
   sudo nano /etc/nginx/sites-available/sense-coach
   # server_name을 실제 도메인으로 변경
   ```

4. **SSL 인증서 재발급**
   ```bash
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

---

## 유지보수

### 앱 업데이트

**Streamlit Cloud:**
```bash
# GitHub에 푸시하면 자동 재배포
git add .
git commit -m "Update features"
git push origin main
```

**Docker:**
```bash
# 최신 코드 가져오기
git pull origin main

# 이미지 재빌드
docker build -t sense-coach:latest .

# 기존 컨테이너 중지 및 삭제
docker stop sense-coach
docker rm sense-coach

# 새 컨테이너 시작
docker run -d \
  --name sense-coach \
  --restart unless-stopped \
  -p 8501:8501 \
  --env-file .env \
  sense-coach:latest
```

### 로그 확인

**Streamlit Cloud:**
- 대시보드에서 "Logs" 탭 확인

**Docker:**
```bash
# 실시간 로그
docker logs -f sense-coach

# 최근 100줄
docker logs --tail 100 sense-coach
```

### 데이터베이스 백업

```bash
# SQLite DB 백업
docker cp sense-coach:/app/school_events.db ./backup_$(date +%Y%m%d).db

# 또는 EC2에서 직접
cp school_events.db backup_$(date +%Y%m%d).db
```

---

## 트러블슈팅

### 앱이 시작되지 않음
```bash
# 로그 확인
docker logs sense-coach

# 일반적인 원인:
# 1. API 키 누락 → .env 파일 확인
# 2. 포트 충돌 → lsof -i :8501
# 3. 메모리 부족 → free -h
```

### API 요청 실패
```bash
# API 키 확인
docker exec sense-coach env | grep GEMINI_API_KEY

# 네트워크 확인
docker exec sense-coach ping -c 3 google.com
```

### 데이터베이스 오류
```bash
# DB 파일 권한 확인
docker exec sense-coach ls -la school_events.db

# DB 재초기화 (주의: 데이터 손실)
docker exec sense-coach rm school_events.db
docker restart sense-coach
```

---

## 비용 안내

### Streamlit Cloud
- **무료 플랜**: 1개 비공개 앱, 무제한 공개 앱
- **유료 플랜**: $10/월 (더 많은 리소스)

### AWS EC2
- **t2.micro** (무료 티어): $0/월 (12개월)
- **t2.small**: ~$17/월
- **데이터 전송**: ~$0.09/GB (out)

### 도메인
- **.com 도메인**: $10-15/년
- **.app 도메인**: $15-20/년

---

## 다음 단계

1. ✅ 클라우드 배포 완료
2. ✅ 도메인 연결 (선택사항)
3. ✅ SSL 인증서 설정
4. ⏭️ 모바일 앱 개발 (APP_STORE_GUIDE.md 참고)
5. ⏭️ 마케팅 및 사용자 피드백 수집

---

## 참고 자료

- [Streamlit Cloud 문서](https://docs.streamlit.io/streamlit-community-cloud)
- [Docker 문서](https://docs.docker.com/)
- [AWS EC2 시작 가이드](https://docs.aws.amazon.com/ec2/)
- [Nginx 설정 가이드](https://nginx.org/en/docs/)
- [Let's Encrypt 문서](https://letsencrypt.org/docs/)
