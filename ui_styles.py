import streamlit as st

# 주요 색상 테마
COLORS = {
    "PRIMARY": "#FFB6C1",
    "SECONDARY": "#FFC0CB",
    "ACCENT": "#FFDAB9",
    "TEXT": "#8B7D9B",
    "BG_LINEAR": "linear-gradient(135deg, #fff5f5 0%, #ffeef0 50%, #fff0f5 100%)",
}

# 파스텔톤 스타일 CSS 적용 - 모바일 최적화
STYLE_CSS = f"""
    <style>
    /* 기본 레이아웃 */
    .main {{
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        max-width: 100%;
    }}
    .stApp {{
        background: {COLORS["BG_LINEAR"]};
    }}
    
    /* 제목 스타일 - 모바일 최적화 */
    h1 {{
        color: {COLORS["TEXT"]};
        font-family: 'Noto Sans KR', sans-serif;
        text-align: center;
        padding: 0.8rem 0.5rem;
        background: linear-gradient(90deg, {COLORS["PRIMARY"]}, {COLORS["SECONDARY"]}, {COLORS["ACCENT"]});
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        font-size: 1.5rem;
        line-height: 1.4;
        margin-bottom: 0.5rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    
    /* 제목 커스텀 스타일 */
    .app-title {{
        color: {COLORS["TEXT"]};
        font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif;
        text-align: center;
        padding: 1rem 0.8rem;
        background: linear-gradient(90deg, {COLORS["PRIMARY"]}, {COLORS["SECONDARY"]}, {COLORS["ACCENT"]});
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.6rem;
        flex-wrap: nowrap;
        word-break: keep-all;
    }}
    
    .app-title-main {{
        font-size: 1.6rem;
        font-weight: bold;
        line-height: 1.4;
        white-space: nowrap;
        word-break: keep-all;
        letter-spacing: -0.02em;
    }}
    
    .app-title-subtitle {{
        font-size: 0.95rem;
        color: #555;
        line-height: 1.6;
        text-align: center;
        padding: 0.6rem 0.8rem;
        margin-top: 0.2rem;
        word-break: keep-all;
        letter-spacing: -0.01em;
    }}
    
    h3 {{
        font-size: 1rem;
        line-height: 1.4;
        padding: 0.3rem 0;
    }}
    
    /* 버튼 스타일 - 모바일 터치 최적화 */
    .stButton>button {{
        background: linear-gradient(90deg, {COLORS["PRIMARY"]}, {COLORS["SECONDARY"]});
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.2rem;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        min-height: 44px;
        width: 100%;
    }}
    .stButton>button:hover {{
        background: linear-gradient(90deg, #FFA0B0, #FFB0C0);
        box-shadow: 0 3px 6px rgba(0,0,0,0.15);
    }}
    
    /* 카드 스타일 - 모바일 최적화 */
    .result-card {{
        background: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid {COLORS["PRIMARY"]};
        white-space: normal;
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 100%;
    }}
    
    .cultural-context {{
        background: linear-gradient(135deg, #fff9e6 0%, #fff5e6 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        border-left: 4px solid #FFD700;
        white-space: normal;
        word-wrap: break-word;
        max-width: 100%;
        line-height: 1.5;
    }}
    
    /* 입력 필드 - 터치 최적화 */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {{
        border-radius: 10px;
        border: 2px solid {COLORS["PRIMARY"]};
        font-size: 1rem;
        padding: 0.8rem;
        min-height: 44px;
    }}
    
    .stSelectbox>div>div>select {{
        border-radius: 10px;
        font-size: 1rem;
        padding: 0.8rem;
        min-height: 44px;
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
    
    /* 탭 스타일 - 버튼처럼 보이게 개선 */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.8rem;
        background: transparent;
        padding: 0.5rem 0;
        border-bottom: 2px solid #e0e0e0;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        font-size: 1rem;
        font-weight: 600;
        padding: 0.9rem 1.5rem;
        min-height: 48px;
        border-radius: 12px 12px 0 0;
        background: #f5f5f5;
        color: #666;
        border: 2px solid #e0e0e0;
        border-bottom: none;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: -2px;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: #e8e8e8;
        color: #333;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background: linear-gradient(135deg, {COLORS["PRIMARY"]} 0%, {COLORS["SECONDARY"]} 100%);
        color: white;
        border-color: {COLORS["PRIMARY"]};
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(255, 182, 193, 0.4);
        transform: translateY(-2px);
    }}
    
    .stTabs [data-baseweb="tab"]:active {{
        transform: translateY(0);
    }}
    
    /* Expander - 터치 최적화 */
    .streamlit-expanderHeader {{
        font-size: 0.95rem;
        padding: 0.8rem;
        min-height: 44px;
    }}
    
    /* 진행률 바 */
    .stProgress > div > div {{
        height: 8px;
        border-radius: 4px;
    }}
    
    /* 체크박스 - 터치 최적화 */
    .stCheckbox {{
        padding: 0.3rem 0;
    }}
    
    .stCheckbox > label {{
        font-size: 0.95rem;
        line-height: 1.4;
        padding: 0.4rem 0;
    }}
    
    /* 모바일 반응형 */
    @media (max-width: 768px) {{
        .main {{
            padding: 0.5rem;
        }}
        
        h1 {{
            font-size: 1.3rem;
            padding: 0.6rem 0.4rem;
        }}
        
        .app-title {{
            padding: 0.8rem 0.5rem;
            gap: 0.4rem;
        }}
        
        .app-title-main {{
            font-size: 1.3rem;
        }}
        
        .app-title-subtitle {{
            font-size: 0.85rem;
            padding: 0.5rem 0.6rem;
            line-height: 1.5;
        }}
        
        h3 {{
            font-size: 0.9rem;
        }}
        
        .result-card {{
            padding: 0.8rem;
            margin: 0.5rem 0;
        }}
        
        .stButton>button {{
            padding: 0.6rem 1rem;
            font-size: 0.95rem;
        }}
        
        /* 컬럼 간격 줄이기 */
        [data-testid="column"] {{
            padding: 0.2rem;
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
