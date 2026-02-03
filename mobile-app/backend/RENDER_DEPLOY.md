# 🚀 Render.com 백엔드 배포 가이드 (초보자용)

제가 대부분의 설정을 코드(`render.yaml`)로 이미 만들어두었습니다. 아래 단계만 따라 하시면 됩니다.

---

## 1단계: GitHub에 코드 올리기

터미널을 열고 아래 명령어를 입력하여 코드를 GitHub에 올리세요.
(이미 제가 커밋을 완료해두었으므로 `push`만 하면 됩니다)

```bash
git push
```

---

## 2단계: Render.com에서 배포하기

1. **[dashboard.render.com](https://dashboard.render.com)** 에 접속하여 로그인하세요.
2. 우측 상단 **[New +]** 버튼 클릭 → **[Blueprint]** 선택
3. **Connect a repository** 목록에서 `sense-coach` 선택 (보이지 않으면 "Configure account"를 눌러 권한 허용)
4. "Service Group Name"에 `sense-coach` 입력
5. **[Apply]** 버튼 클릭
6. **환경 변수 입력**:
   - `GEMINI_API_KEY` 입력칸이 나오면, 갖고 계신 Google Gemini API 키를 붙여넣으세요.
   - **[Update Environment Variables]** 클릭

---

## 3단계: 완료 확인

배포가 시작되면 몇 분 정도 걸립니다. 완료되면 **Service URL**이 표시됩니다.
예: `https://sense-coach-api.onrender.com`

> **중요**: 이 URL을 복사해서 저에게 알려주세요! 앱 설정을 변경해야 합니다.
