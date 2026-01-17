import streamlit as st

# 파스텔 톤 색상 테마 - 이미지 스타일 기반
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
    
    # 그라디언트
    "GRADIENT_PEACH": "linear-gradient(135deg, #FFE5D9 0%, #FFF0EB 100%)",
    "GRADIENT_MINT": "linear-gradient(135deg, #D4EDDA 0%, #E8F5E9 100%)",
    "GRADIENT_LAVENDER": "linear-gradient(135deg, #E9D5FF 0%, #F3E8FF 100%)",
    "GRADIENT_BEIGE": "linear-gradient(135deg, #F5F0E8 0%, #FAF8F3 100%)",
    "GRADIENT_PRIMARY": "linear-gradient(135deg, #9F7AEA 0%, #F687B3 100%)",
    
    # 그림자
    "CARD_SHADOW": "0 4px 12px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(0, 0, 0, 0.04)",
    "CARD_SHADOW_HOVER": "0 8px 20px rgba(0, 0, 0, 0.12), 0 4px 8px rgba(0, 0, 0, 0.06)",
}

# 고급 커스텀 디자인 CSS - 프로페셔널한 UI/UX
STYLE_CSS = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css') layer(fonts);
    
    /* 폰트 로딩 최적화 */
    @font-face {{
        font-family: 'Pretendard';
        font-display: swap;
    }}
    
    /* 기본 레이아웃 - 파스텔 배경 */
    .main {{
        background: {COLORS["BG_MAIN"]};
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(255, 229, 217, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(233, 213, 255, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(212, 237, 218, 0.3) 0%, transparent 50%);
        background-attachment: fixed;
        padding: 1rem;
        max-width: 100%;
    }}
    .stApp {{
        background: {COLORS["BG_MAIN"]};
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(255, 229, 217, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(233, 213, 255, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(212, 237, 218, 0.3) 0%, transparent 50%);
        background-attachment: fixed;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', 'Inter', sans-serif;
    }}
    
    /* 전역 글씨체 설정 */
    * {{
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', 'Inter', sans-serif;
    }}
    
    /* 제목 스타일 - 파스텔 톤 */
    h1 {{
        color: {COLORS["TEXT"]};
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', 'Inter', sans-serif;
        text-align: center;
        padding: 1.2rem 1rem;
        background: {COLORS["BG_CARD"]};
        border-radius: 24px;
        box-shadow: {COLORS["CARD_SHADOW"]};
        font-size: 28px;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 0.8rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        letter-spacing: -0.02em;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }}
    
    /* 제목 커스텀 스타일 - 파스텔 톤 그라디언트 */
    .app-title {{
        color: white;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', 'Inter', sans-serif;
        text-align: center;
        padding: 1.5rem 2rem;
        background: {COLORS["GRADIENT_PRIMARY"]};
        border-radius: 24px;
        box-shadow: 0 8px 24px rgba(159, 122, 234, 0.3);
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        flex-wrap: nowrap;
        word-break: keep-all;
        position: relative;
        overflow: hidden;
    }}
    
    .app-title-main {{
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.2;
        white-space: nowrap;
        word-break: keep-all;
        letter-spacing: -0.03em;
        position: relative;
        z-index: 1;
    }}
    
    .app-title-subtitle {{
        font-size: 1rem;
        color: {COLORS["TEXT_MEDIUM"]};
        line-height: 1.6;
        text-align: center;
        padding: 1rem 1.5rem;
        margin-top: 1rem;
        word-break: keep-all;
        letter-spacing: -0.01em;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        border: 1px solid rgba(0, 0, 0, 0.05);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }}
    
    h2 {{
        font-size: 22px;
        font-weight: 600;
        color: {COLORS["TEXT"]};
        letter-spacing: -0.01em;
        line-height: 1.3;
        margin: 1.5rem 0 1rem 0;
    }}
    
    h3 {{
        font-size: 18px;
        font-weight: 600;
        color: {COLORS["TEXT_MEDIUM"]};
        line-height: 1.4;
        padding: 0.5rem 0;
        letter-spacing: -0.01em;
    }}
    
    /* 파스텔 톤 버튼 스타일 */
    .stButton>button {{
        background: {COLORS["PRIMARY"]};
        color: white;
        border: none;
        border-radius: 16px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(159, 122, 234, 0.3);
        min-height: 48px;
        width: 100%;
        transition: all 0.3s ease;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', 'Inter', sans-serif;
        letter-spacing: 0.01em;
    }}
    
    .stButton>button:hover {{
        background: #B794F4;
        box-shadow: 0 6px 16px rgba(159, 122, 234, 0.4);
        transform: translateY(-1px);
    }}
    
    .stButton>button:active {{
        transform: translateY(0);
    }}
    
    /* 파스텔 톤 카드 스타일 */
    .result-card {{
        background: {COLORS["BG_CARD"]};
        padding: 1.5rem;
        border-radius: 24px;
        margin: 1rem 0;
        box-shadow: {COLORS["CARD_SHADOW"]};
        border: 1px solid rgba(0, 0, 0, 0.05);
        border-left: 5px solid {COLORS["PRIMARY"]};
        white-space: normal;
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }}
    
    .result-card:hover {{
        transform: translateY(-2px);
        box-shadow: {COLORS["CARD_SHADOW_HOVER"]};
        border-left-color: {COLORS["SECONDARY"]};
    }}
    
    .cultural-context {{
        background: {COLORS["GRADIENT_BEIGE"]};
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        border: 1px solid rgba(246, 173, 85, 0.2);
        border-left: 5px solid {COLORS["WARNING"]};
        white-space: normal;
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 100%;
        line-height: 1.7;
        box-shadow: {COLORS["CARD_SHADOW"]};
        transition: all 0.3s ease;
    }}
    
    .cultural-context:hover {{
        transform: translateY(-2px);
        box-shadow: {COLORS["CARD_SHADOW_HOVER"]};
    }}
    
    /* 파스텔 톤 입력 필드 */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {{
        background: {COLORS["BG_CARD"]};
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 0.875rem 1.25rem;
        font-size: 16px;
        color: {COLORS["TEXT"]};
        transition: all 0.3s ease;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', 'Inter', sans-serif;
        min-height: 48px;
    }}
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {{
        border-color: {COLORS["PRIMARY"]};
        box-shadow: 0 0 0 4px rgba(159, 122, 234, 0.1);
        outline: none;
    }}
    
    .stSelectbox>div>div>select {{
        background: {COLORS["BG_CARD"]};
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 0.875rem 1.25rem;
        font-size: 16px;
        color: {COLORS["TEXT"]};
        transition: all 0.3s ease;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', 'Inter', sans-serif;
        min-height: 48px;
    }}
    
    .stSelectbox>div>div>select:focus {{
        border-color: {COLORS["PRIMARY"]};
        box-shadow: 0 0 0 4px rgba(159, 122, 234, 0.1);
        outline: none;
    }}
    
    /* 아이 관리 버튼 - 터치 최적화 */
    button[key*="edit_child"],
    button[key*="delete_child"] {{
        min-height: 44px !important;
        max-height: 50px !important;
        padding: 0.6rem 1rem !important;
        font-size: 1rem !important;
    }}
    
    /* 사이드바 - 모바일 최적화 */
    [data-testid="stSidebar"] {{
        padding: 1rem 0.5rem;
    }}
    
    [data-testid="stSidebar"] .stSelectbox {{
        margin-bottom: 1rem;
    }}
    
    /* 파스텔 톤 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {{
        background: #F7FAFC;
        border-radius: 16px;
        padding: 0.5rem;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        color: {COLORS["TEXT_LIGHT"]};
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 1rem;
        min-height: 48px;
        transition: all 0.3s ease;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', 'Inter', sans-serif;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: rgba(159, 122, 234, 0.1);
        color: {COLORS["TEXT"]};
    }}
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background: {COLORS["PRIMARY"]};
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(159, 122, 234, 0.3);
    }}
    
    /* Expander - 터치 최적화 */
    .streamlit-expanderHeader {{
        font-size: 0.95rem;
        padding: 0.8rem;
        min-height: 44px;
    }}
    
    /* 파스텔 톤 진행률 바 */
    .stProgress > div > div {{
        height: 10px;
        border-radius: 10px;
        background: {COLORS["PRIMARY"]};
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }}
    
    /* 파스텔 톤 체크박스 스타일 */
    .stCheckbox {{
        padding: 0.5rem 0;
    }}
    
    .stCheckbox > label {{
        font-size: 16px;
        font-weight: 500;
        line-height: 1.6;
        padding: 0.5rem 0;
        color: {COLORS["TEXT"]};
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', 'Inter', sans-serif;
        transition: color 0.2s ease;
    }}
    
    .stCheckbox > label:hover {{
        color: {COLORS["PRIMARY"]};
    }}
    
    /* 사이드바 스타일 - 파스텔 톤 */
    [data-testid="stSidebar"] {{
        background: {COLORS["BG_CARD"]};
        border-right: 1px solid rgba(0, 0, 0, 0.05);
    }}
    
    /* Expander 스타일 */
    .streamlit-expanderHeader {{
        background: {COLORS["BG_CARD"]};
        border-radius: 12px;
        border: 1px solid rgba(0, 0, 0, 0.05);
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
    }}
    
    .streamlit-expanderHeader:hover {{
        background: #F7FAFC;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }}
    
    /* 커스텀 아이콘 스타일 */
    .custom-icon {{
        display: inline-block;
        vertical-align: middle;
        margin-right: 6px;
        filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
    }}
    
    /* 파스텔 톤 메시지 스타일 */
    .stSuccess {{
        background: rgba(104, 211, 145, 0.1);
        border-left: 4px solid {COLORS["SUCCESS"]};
        border-radius: 16px;
        padding: 1rem;
        box-shadow: {COLORS["CARD_SHADOW"]};
    }}
    
    .stError {{
        background: rgba(252, 129, 129, 0.1);
        border-left: 4px solid {COLORS["ERROR"]};
        border-radius: 16px;
        padding: 1rem;
        box-shadow: {COLORS["CARD_SHADOW"]};
    }}
    
    .stWarning {{
        background: rgba(246, 173, 85, 0.1);
        border-left: 4px solid {COLORS["WARNING"]};
        border-radius: 16px;
        padding: 1rem;
        box-shadow: {COLORS["CARD_SHADOW"]};
    }}
    
    .stInfo {{
        background: rgba(159, 122, 234, 0.1);
        border-left: 4px solid {COLORS["PRIMARY"]};
        border-radius: 16px;
        padding: 1rem;
        box-shadow: {COLORS["CARD_SHADOW"]};
    }}
    
    /* 본문 텍스트 스타일 */
    p, body {{
        font-size: 16px;
        font-weight: 400;
        color: {COLORS["TEXT_MEDIUM"]};
        line-height: 1.6;
    }}
    
    small, .caption {{
        font-size: 14px;
        font-weight: 400;
        color: {COLORS["TEXT_LIGHT"]};
        line-height: 1.4;
    }}
    
    /* 파스텔 톤 이벤트 카드 (타임라인 스타일) */
    .event-card {{
        background: {COLORS["BG_CARD"]};
        border-radius: 20px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        box-shadow: {COLORS["CARD_SHADOW"]};
        border-left: 4px solid {COLORS["PRIMARY"]};
        transition: all 0.3s ease;
    }}
    
    .event-card:hover {{
        transform: translateX(4px);
        box-shadow: {COLORS["CARD_SHADOW_HOVER"]};
    }}
    
    .event-card.peach {{
        background: {COLORS["GRADIENT_PEACH"]};
        border-left-color: {COLORS["SECONDARY"]};
    }}
    
    .event-card.mint {{
        background: {COLORS["GRADIENT_MINT"]};
        border-left-color: {COLORS["SUCCESS"]};
    }}
    
    .event-card.lavender {{
        background: {COLORS["GRADIENT_LAVENDER"]};
        border-left-color: {COLORS["PRIMARY"]};
    }}
    
    /* 커스텀 아이콘 스타일 - SVG 아이콘 */
    .custom-icon {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 1.2em;
        height: 1.2em;
        max-width: 20px;
        max-height: 20px;
        margin-right: 0.5em;
        vertical-align: middle;
        flex-shrink: 0;
        color: {COLORS["TEXT_MEDIUM"]};
    }}
    
    .custom-icon svg {{
        width: 100%;
        height: 100%;
        max-width: 20px;
        max-height: 20px;
        stroke: currentColor;
        fill: currentColor;
        stroke-width: 1.5;
        stroke-linecap: round;
        stroke-linejoin: round;
        color: inherit;
    }}
    
    /* 아이콘 내부 path와 circle도 색상 상속 */
    .custom-icon svg path,
    .custom-icon svg circle,
    .custom-icon svg line,
    .custom-icon svg polyline,
    .custom-icon svg rect {{
        stroke: currentColor;
        fill: none;
        color: inherit;
    }}
    
    /* 제목의 아이콘 크기 조정 */
    h3 .custom-icon,
    h2 .custom-icon {{
        width: 1.1em;
        height: 1.1em;
        max-width: 18px;
        max-height: 18px;
        margin-right: 0.4em;
    }}
    
    /* 사이드바 아이콘 색상 조정 */
    [data-testid="stSidebar"] .custom-icon {{
        color: {COLORS["TEXT"]};
    }}
    
    /* 모바일 반응형 */
    @media (max-width: 768px) {{
        .main {{
            padding: 0.5rem;
        }}
        
        h1 {{
            font-size: 1.4rem;
            padding: 0.8rem 0.5rem;
        }}
        
        .app-title {{
            padding: 1rem 0.8rem;
            gap: 0.6rem;
        }}
        
        .app-title-main {{
            font-size: 1.4rem;
        }}
        
        .app-title-subtitle {{
            font-size: 0.9rem;
            padding: 0.6rem 0.8rem;
            line-height: 1.6;
        }}
        
        h3 {{
            font-size: 1rem;
        }}
        
        .result-card {{
            padding: 1rem;
            margin: 0.8rem 0;
            border-radius: 16px;
        }}
        
        .stButton>button {{
            padding: 0.7rem 1.2rem;
            font-size: 0.95rem;
        }}
        
        /* 컬럼 간격 줄이기 */
        [data-testid="column"] {{
            padding: 0.3rem;
        }}
        
        .metro-card {{
            padding: 1rem;
            border-radius: 16px;
        }}
    }}
    
    /* 매우 작은 화면 (360px 이하) */
    @media (max-width: 360px) {{
        h1 {{
            font-size: 1.1rem;
            padding: 0.5rem 0.3rem;
        }}
        
        .app-title {{
            padding: 0.7rem 0.4rem;
            gap: 0.3rem;
        }}
        
        .app-title-main {{
            font-size: 1.1rem;
        }}
        
        .app-title-subtitle {{
            font-size: 0.8rem;
            padding: 0.4rem 0.5rem;
        }}
        
        .stButton>button {{
            padding: 0.5rem 0.8rem;
            font-size: 0.9rem;
        }}
    }}
    </style>
    """
