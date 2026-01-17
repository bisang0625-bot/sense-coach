# CSS 마이그레이션 가이드 - 파스텔 톤 디자인

## 🎯 목표 스타일

이미지의 파스텔 톤, 부드러운 카드, 모던한 레이아웃을 '눈치코치 알림장'에 적용

## 📝 CSS 변경 가이드

### 1. 컬러 팔레트 변경

```python
# 기존 (현재)
COLORS = {
    "PRIMARY": "#6366F1",  # 인디고 블루
    "SECONDARY": "#8B5CF6",  # 바이올렛
    "ACCENT": "#EC4899",  # 핑크
}

# 변경 후 (이미지 스타일)
COLORS = {
    # 파스텔 배경 색상
    "PEACH": "#FFE5D9",      # 라이트 피치
    "MINT": "#D4EDDA",       # 라이트 민트
    "LAVENDER": "#E9D5FF",   # 라이트 라벤더
    "BEIGE": "#F5F0E8",      # 라이트 베이지
    "CREAM": "#FEFCF9",      # 크림 화이트
    
    # 메인 컬러 (조화로운 톤)
    "PRIMARY": "#9F7AEA",    # 소프트 퍼플
    "SECONDARY": "#F687B3",  # 소프트 핑크
    "ACCENT": "#FBD38D",     # 소프트 옐로우
    
    # 텍스트
    "TEXT": "#2D3748",       # 다크 그레이
    "TEXT_MEDIUM": "#4A5568", # 미디엄 그레이
    "TEXT_LIGHT": "#718096",  # 라이트 그레이
    
    # 강조 색상
    "SUCCESS": "#68D391",    # 소프트 그린
    "WARNING": "#F6AD55",    # 소프트 오렌지
    "ERROR": "#FC8181",      # 소프트 레드
    
    # 배경
    "BG_MAIN": "#FEFCF9",    # 메인 배경 (크림 화이트)
    "BG_CARD": "#FFFFFF",    # 카드 배경 (화이트)
    
    # 그림자
    "CARD_SHADOW": "0 4px 12px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(0, 0, 0, 0.04)",
    "CARD_SHADOW_HOVER": "0 8px 20px rgba(0, 0, 0, 0.12), 0 4px 8px rgba(0, 0, 0, 0.06)",
}
```

### 2. 메인 배경 변경

```css
/* 기존 */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 변경 후 */
.stApp {
    background: #FEFCF9;  /* 크림 화이트 */
    background-image: 
        radial-gradient(circle at 20% 50%, rgba(255, 229, 217, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(233, 213, 255, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 40% 20%, rgba(212, 237, 218, 0.3) 0%, transparent 50%);
    background-attachment: fixed;
}
```

### 3. 카드 스타일 변경

```css
/* 기존 */
.result-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
}

/* 변경 후 */
.result-card {
    background: #FFFFFF;
    border-radius: 24px;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(0, 0, 0, 0.04);
    border: 1px solid rgba(0, 0, 0, 0.05);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.result-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12), 0 4px 8px rgba(0, 0, 0, 0.06);
}
```

### 4. 타이포그래피 조정

```css
/* 헤더 */
h1 {
    font-size: 28px;
    font-weight: 700;
    color: #2D3748;
    letter-spacing: -0.02em;
    line-height: 1.2;
}

h2 {
    font-size: 22px;
    font-weight: 600;
    color: #2D3748;
    letter-spacing: -0.01em;
    line-height: 1.3;
}

h3 {
    font-size: 18px;
    font-weight: 600;
    color: #4A5568;
    line-height: 1.4;
}

/* 본문 */
body, p {
    font-size: 16px;
    font-weight: 400;
    color: #4A5568;
    line-height: 1.6;
}

/* 보조 텍스트 */
.caption, small {
    font-size: 14px;
    font-weight: 400;
    color: #718096;
    line-height: 1.4;
}
```

### 5. 버튼 스타일 변경

```css
/* 기존 */
.stButton>button {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

/* 변경 후 */
.stButton>button {
    background: #9F7AEA;  /* 소프트 퍼플 */
    color: white;
    border: none;
    border-radius: 16px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    font-size: 16px;
    box-shadow: 0 4px 12px rgba(159, 122, 234, 0.3);
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background: #B794F4;
    box-shadow: 0 6px 16px rgba(159, 122, 234, 0.4);
    transform: translateY(-1px);
}

.stButton>button:active {
    transform: translateY(0);
}
```

### 6. 입력 필드 스타일

```css
.stTextInput>div>div>input,
.stTextArea>div>div>textarea {
    background: #FFFFFF;
    border: 2px solid #E2E8F0;
    border-radius: 16px;
    padding: 0.875rem 1.25rem;
    font-size: 16px;
    color: #2D3748;
    transition: all 0.3s ease;
}

.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus {
    border-color: #9F7AEA;
    box-shadow: 0 0 0 4px rgba(159, 122, 234, 0.1);
    outline: none;
}
```

### 7. 탭 스타일

```css
.stTabs [data-baseweb="tab-list"] {
    background: #F7FAFC;
    border-radius: 16px;
    padding: 0.5rem;
    gap: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #718096;
    border-radius: 12px;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: #9F7AEA;
    color: white;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(159, 122, 234, 0.3);
}
```

### 8. 카테고리 카드 스타일 (이미지 스타일)

```css
.category-card {
    background: linear-gradient(135deg, #FFE5D9 0%, #FFF0EB 100%);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.category-card::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
}

.category-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

/* 다른 카테고리 색상 */
.category-card.mint {
    background: linear-gradient(135deg, #D4EDDA 0%, #E8F5E9 100%);
}

.category-card.lavender {
    background: linear-gradient(135deg, #E9D5FF 0%, #F3E8FF 100%);
}

.category-card.beige {
    background: linear-gradient(135deg, #F5F0E8 0%, #FAF8F3 100%);
}
```

### 9. 이벤트 카드 스타일 (타임라인)

```css
.event-card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 1.25rem;
    margin: 0.75rem 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    border-left: 4px solid #9F7AEA;
    transition: all 0.3s ease;
}

.event-card:hover {
    transform: translateX(4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.event-card.peach {
    background: linear-gradient(135deg, #FFF5F0 0%, #FFFFFF 100%);
    border-left-color: #F687B3;
}

.event-card.mint {
    background: linear-gradient(135deg, #F0FFF4 0%, #FFFFFF 100%);
    border-left-color: #68D391;
}

.event-card.lavender {
    background: linear-gradient(135deg, #F5F3FF 0%, #FFFFFF 100%);
    border-left-color: #9F7AEA;
}
```

### 10. 태그/배지 스타일

```css
.badge {
    display: inline-block;
    padding: 0.375rem 0.75rem;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
    background: #EDF2F7;
    color: #4A5568;
}

.badge.primary {
    background: #9F7AEA;
    color: white;
}

.badge.success {
    background: #68D391;
    color: white;
}

.badge.warning {
    background: #FBD38D;
    color: #2D3748;
}
```

### 11. 메인 타이틀 스타일 (개선)

```css
.app-title {
    background: linear-gradient(135deg, #9F7AEA 0%, #F687B3 100%);
    color: white;
    border-radius: 24px;
    padding: 1.5rem 2rem;
    box-shadow: 0 8px 24px rgba(159, 122, 234, 0.3);
    margin-bottom: 2rem;
}

.app-title-subtitle {
    background: rgba(255, 255, 255, 0.9);
    color: #4A5568;
    border-radius: 16px;
    padding: 1rem 1.5rem;
    margin-top: 1rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
```

## 🚀 적용 순서

1. **1단계**: 컬러 팔레트 변경 (COLORS 딕셔너리)
2. **2단계**: 메인 배경 변경 (stApp)
3. **3단계**: 카드 스타일 개선 (result-card, event-card)
4. **4단계**: 버튼 및 입력 필드 스타일
5. **5단계**: 타이포그래피 조정
6. **6단계**: 탭 및 네비게이션 스타일
7. **7단계**: 미세 조정 및 테스트

## ⚠️ 주의사항

1. **Streamlit 제약**: 일부 레이아웃은 Streamlit의 구조적 제약으로 완벽히 구현 어려울 수 있음
2. **색상 대비**: 텍스트 가독성을 위해 색상 대비비 확인 필요
3. **반응형 디자인**: 모바일 환경에서도 잘 작동하도록 미디어 쿼리 적용
4. **성능**: backdrop-filter는 성능에 영향 줄 수 있으므로 필요시 제거

## 📌 다음 단계

이 가이드를 기반으로 `ui_styles.py` 파일을 업데이트하시겠습니까?
