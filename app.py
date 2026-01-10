import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import io
import re
import sqlite3
from datetime import datetime, date
import json
import html as html_escape

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="눈치코치: Sense Coach",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 파스텔톤 스타일 CSS 적용 - 모바일 최적화
st.markdown("""
    <style>
    /* 기본 레이아웃 */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        max-width: 100%;
    }
    .stApp {
        background: linear-gradient(135deg, #fff5f5 0%, #ffeef0 50%, #fff0f5 100%);
    }
    
    /* 제목 스타일 - 모바일 최적화 */
    h1 {
        color: #8B7D9B;
        font-family: 'Noto Sans KR', sans-serif;
        text-align: center;
        padding: 0.8rem 0.5rem;
        background: linear-gradient(90deg, #FFB6C1, #FFC0CB, #FFDAB9);
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        font-size: 1.5rem;
        line-height: 1.4;
        margin-bottom: 0.5rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* 제목 커스텀 스타일 */
    .app-title {
        color: #8B7D9B;
        font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif;
        text-align: center;
        padding: 1rem 0.8rem;
        background: linear-gradient(90deg, #FFB6C1, #FFC0CB, #FFDAB9);
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.6rem;
        flex-wrap: nowrap;
        word-break: keep-all;
    }
    
    .app-title-main {
        font-size: 1.6rem;
        font-weight: bold;
        line-height: 1.4;
        white-space: nowrap;
        word-break: keep-all;
        letter-spacing: -0.02em;
    }
    
    .app-title-subtitle {
        font-size: 0.95rem;
        color: #555;
        line-height: 1.6;
        text-align: center;
        padding: 0.6rem 0.8rem;
        margin-top: 0.2rem;
        word-break: keep-all;
        letter-spacing: -0.01em;
    }
    
    h3 {
        font-size: 1rem;
        line-height: 1.4;
        padding: 0.3rem 0;
    }
    
    /* 버튼 스타일 - 모바일 터치 최적화 */
    .stButton>button {
        background: linear-gradient(90deg, #FFB6C1, #FFC0CB);
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
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #FFA0B0, #FFB0C0);
        box-shadow: 0 3px 6px rgba(0,0,0,0.15);
    }
    
    /* 카드 스타일 - 모바일 최적화 */
    .result-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #FFB6C1;
        white-space: normal;
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 100%;
    }
    
    .cultural-context {
        background: linear-gradient(135deg, #fff9e6 0%, #fff5e6 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        border-left: 4px solid #FFD700;
        white-space: normal;
        word-wrap: break-word;
        max-width: 100%;
        line-height: 1.5;
    }
    
    /* 입력 필드 - 터치 최적화 */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid #FFB6C1;
        font-size: 1rem;
        padding: 0.8rem;
        min-height: 44px;
    }
    
    .stSelectbox>div>div>select {
        border-radius: 10px;
        font-size: 1rem;
        padding: 0.8rem;
        min-height: 44px;
    }
    
    /* 아이 관리 버튼 - 터치 최적화 */
    button[key*="edit_child"],
    button[key*="delete_child"] {
        min-height: 44px !important;
        max-height: 50px !important;
        padding: 0.6rem 1rem !important;
        font-size: 1rem !important;
    }
    
    /* 사이드바 - 모바일 최적화 */
    [data-testid="stSidebar"] {
        padding: 1rem 0.5rem;
    }
    
    [data-testid="stSidebar"] .stSelectbox {
        margin-bottom: 1rem;
    }
    
    /* 탭 스타일 - 버튼처럼 보이게 개선 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.8rem;
        background: transparent;
        padding: 0.5rem 0;
        border-bottom: 2px solid #e0e0e0;
    }
    
    .stTabs [data-baseweb="tab"] {
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
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e8e8e8;
        color: #333;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #FFB6C1 0%, #FFC0CB 100%);
        color: white;
        border-color: #FFB6C1;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(255, 182, 193, 0.4);
        transform: translateY(-2px);
    }
    
    .stTabs [data-baseweb="tab"]:active {
        transform: translateY(0);
    }
    
    /* Expander - 터치 최적화 */
    .streamlit-expanderHeader {
        font-size: 0.95rem;
        padding: 0.8rem;
        min-height: 44px;
    }
    
    /* 진행률 바 */
    .stProgress > div > div {
        height: 8px;
        border-radius: 4px;
    }
    
    /* 체크박스 - 터치 최적화 */
    .stCheckbox {
        padding: 0.3rem 0;
    }
    
    .stCheckbox > label {
        font-size: 0.95rem;
        line-height: 1.4;
        padding: 0.4rem 0;
    }
    
    /* 모바일 반응형 */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        
        h1 {
            font-size: 1.3rem;
            padding: 0.6rem 0.4rem;
        }
        
        .app-title {
            padding: 0.8rem 0.5rem;
            gap: 0.4rem;
        }
        
        .app-title-main {
            font-size: 1.3rem;
        }
        
        .app-title-subtitle {
            font-size: 0.85rem;
            padding: 0.5rem 0.6rem;
            line-height: 1.5;
        }
        
        h3 {
            font-size: 0.9rem;
        }
        
        .result-card {
            padding: 0.8rem;
            margin: 0.5rem 0;
        }
        
        .stButton>button {
            padding: 0.6rem 1rem;
            font-size: 0.95rem;
        }
        
        /* 컬럼 간격 줄이기 */
        [data-testid="column"] {
            padding: 0.2rem;
        }
    }
    
    /* 매우 작은 화면 (360px 이하) */
    @media (max-width: 360px) {
        h1 {
            font-size: 1.1rem;
            padding: 0.5rem 0.3rem;
        }
        
        .app-title {
            padding: 0.7rem 0.4rem;
            gap: 0.3rem;
        }
        
        .app-title-main {
            font-size: 1.1rem;
        }
        
        .app-title-subtitle {
            font-size: 0.8rem;
            padding: 0.4rem 0.5rem;
        }
        
        .stButton>button {
            padding: 0.5rem 0.8rem;
            font-size: 0.9rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 데이터베이스 초기화
def init_database():
    """데이터베이스 초기화 및 테이블 생성"""
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    
    # 이벤트 테이블 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            event_date DATE NOT NULL,
            event_time TEXT,
            country TEXT,
            child_tag TEXT,
            translation TEXT,
            cultural_context TEXT,
            tips TEXT,
            checklist_items TEXT,
            memo TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 기존 테이블에 memo 컬럼 추가 (없는 경우)
    try:
        c.execute('ALTER TABLE events ADD COLUMN memo TEXT')
    except sqlite3.OperationalError:
        pass  # 컬럼이 이미 존재하면 무시
    
    # 체크리스트 항목 테이블 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS checklist_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            is_checked INTEGER DEFAULT 0,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
        )
    ''')
    
    # 아이 정보 테이블 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS children (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            display_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 기본 아이 정보 추가 (없는 경우만)
    c.execute('SELECT COUNT(*) FROM children')
    if c.fetchone()[0] == 0:
        c.execute('INSERT INTO children (name, display_order) VALUES (?, ?)', ('첫째', 1))
        c.execute('INSERT INTO children (name, display_order) VALUES (?, ?)', ('둘째', 2))
    
    conn.commit()
    conn.close()

def get_children():
    """저장된 아이 목록 조회"""
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    
    c.execute('SELECT name FROM children ORDER BY display_order ASC, id ASC')
    children = [row[0] for row in c.fetchall()]
    
    conn.close()
    return children if children else []

def add_child(name):
    """아이 추가"""
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    
    try:
        # display_order 계산
        c.execute('SELECT MAX(display_order) FROM children')
        max_order = c.fetchone()[0]
        next_order = (max_order or 0) + 1
        
        c.execute('INSERT INTO children (name, display_order) VALUES (?, ?)', (name, next_order))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False  # 중복 이름

def delete_child(name):
    """아이 삭제"""
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    
    c.execute('DELETE FROM children WHERE name = ?', (name,))
    conn.commit()
    conn.close()

def update_child_name(old_name, new_name):
    """아이 이름 수정"""
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    
    try:
        c.execute('UPDATE children SET name = ? WHERE name = ?', (new_name, old_name))
        # events 테이블의 child_tag도 업데이트
        c.execute('UPDATE events SET child_tag = ? WHERE child_tag = ?', (new_name, old_name))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        conn.close()
        return False  # 중복 이름

def save_event(event_data):
    """이벤트 저장"""
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO events 
        (event_name, event_date, event_time, country, child_tag, translation, cultural_context, tips, checklist_items, memo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        event_data['event_name'],
        event_data['event_date'],
        event_data.get('event_time', ''),
        event_data.get('country', ''),
        event_data.get('child_tag', '없음'),
        event_data.get('translation', ''),
        event_data.get('cultural_context', ''),
        event_data.get('tips', ''),
        json.dumps(event_data.get('checklist_items', []), ensure_ascii=False),
        event_data.get('memo', '')
    ))
    
    event_id = c.lastrowid
    
    # 체크리스트 항목 저장 (검증 후)
    valid_items = [item for item in event_data.get('checklist_items', []) if is_valid_checklist_item(item)]
    for item in valid_items:
        c.execute('''
            INSERT INTO checklist_items (event_id, item_name, is_checked)
            VALUES (?, ?, 0)
        ''', (event_id, item))
    
    conn.commit()
    conn.close()
    return event_id

def get_events(future_only=False):
    """이벤트 조회"""
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    
    if future_only:
        today = date.today().isoformat()
        c.execute('''
            SELECT * FROM events 
            WHERE event_date >= ?
            ORDER BY event_date ASC, event_time ASC
        ''', (today,))
    else:
        c.execute('''
            SELECT * FROM events 
            ORDER BY event_date ASC, event_time ASC
        ''')
    
    rows = c.fetchall()
    events = []
    
    for row in rows:
        # 컬럼 수에 따라 memo 필드 처리
        # 테이블 구조: id(0), event_name(1), event_date(2), event_time(3), country(4), 
        #             child_tag(5), translation(6), cultural_context(7), tips(8), 
        #             checklist_items(9), created_at(10), memo(11)
        row_len = len(row)
        event = {
            'id': row[0],
            'event_name': row[1],
            'event_date': row[2],
            'event_time': row[3],
            'country': row[4],
            'child_tag': row[5],
            'translation': row[6],
            'cultural_context': row[7],
            'tips': row[8],
            'checklist_items': json.loads(row[9]) if row[9] else [],
            'created_at': row[10],  # created_at은 항상 10번 인덱스
            'memo': row[11] if row_len > 11 else ''  # memo는 11번 인덱스 (있으면)
        }
        
        # 체크리스트 항목 로드
        c.execute('''
            SELECT id, item_name, is_checked 
            FROM checklist_items 
            WHERE event_id = ?
            ORDER BY id ASC
        ''', (event['id'],))
        
        checklist_with_status = []
        for item_row in c.fetchall():
            checklist_with_status.append({
                'id': item_row[0],
                'name': item_row[1],
                'checked': bool(item_row[2])
            })
        
        event['checklist_with_status'] = checklist_with_status
        events.append(event)
    
    conn.close()
    return events

def delete_event(event_id):
    """이벤트 삭제"""
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    
    c.execute('DELETE FROM events WHERE id = ?', (event_id,))
    # 체크리스트 항목은 CASCADE로 자동 삭제됨
    
    conn.commit()
    conn.close()

def update_checklist_item(item_id, is_checked):
    """체크리스트 항목 상태 업데이트"""
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    
    c.execute('''
        UPDATE checklist_items 
        SET is_checked = ? 
        WHERE id = ?
    ''', (1 if is_checked else 0, item_id))
    
    conn.commit()
    conn.close()

def update_event(event_id, event_data):
    """이벤트 정보 업데이트"""
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    
    c.execute('''
        UPDATE events 
        SET event_name = ?, event_date = ?, event_time = ?, country = ?, child_tag = ?, memo = ?
        WHERE id = ?
    ''', (
        event_data.get('event_name', ''),
        event_data.get('event_date', ''),
        event_data.get('event_time', ''),
        event_data.get('country', ''),
        event_data.get('child_tag', '없음'),
        event_data.get('memo', ''),
        event_id
    ))
    
    conn.commit()
    conn.close()

def add_checklist_item(event_id, item_name):
    """체크리스트 항목 추가 (검증 후)"""
    # 검증 통과 여부 확인
    if not is_valid_checklist_item(item_name):
        raise ValueError("유효하지 않은 준비물 항목입니다. 실제 필요한 준비물을 입력해주세요.")
    
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO checklist_items (event_id, item_name, is_checked)
        VALUES (?, ?, 0)
    ''', (event_id, item_name.strip()))
    
    conn.commit()
    conn.close()

def delete_checklist_item(item_id):
    """체크리스트 항목 삭제"""
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    
    c.execute('DELETE FROM checklist_items WHERE id = ?', (item_id,))
    
    conn.commit()
    conn.close()

def update_checklist_item_name(item_id, new_name):
    """체크리스트 항목 이름 수정 (검증 후)"""
    # 검증 통과 여부 확인
    if not is_valid_checklist_item(new_name):
        raise ValueError("유효하지 않은 준비물 항목입니다. 실제 필요한 준비물을 입력해주세요.")
    
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    
    c.execute('''
        UPDATE checklist_items 
        SET item_name = ? 
        WHERE id = ?
    ''', (new_name.strip(), item_id))
    
    conn.commit()
    conn.close()

# 국가별 교육 문화 정보
COUNTRY_INFO = {
    "네덜란드": {
        "name": "네덜란드",
        "culture": "네덜란드 교육 시스템은 매우 개방적이고 실용적입니다. Studiedag(공부하는 날)는 교사 연수일로 아이들이 등교하지 않습니다. Koningsdag(국왕의 날), Sinterklaas(성 니콜라스 축제) 등 중요한 기념일이 있습니다."
    },
    "미국": {
        "name": "미국",
        "culture": "미국 학교는 학부모 참여가 활발합니다. PTA(학부모 교사 협회) 모임, 필드트립, 포토데이 등 다양한 행사가 있습니다. Thanksgiving, Halloween, Martin Luther King Jr. Day 등 문화적 기념일이 중요합니다."
    },
    "독일": {
        "name": "독일",
        "culture": "독일 교육은 지역별로 차이가 큽니다. Schulfest(학교 축제), Wandertag(등산의 날) 등이 있습니다. 독일의 공휴일과 지역 축제일을 고려해야 합니다."
    },
    "영국": {
        "name": "영국",
        "culture": "영국 학교는 하우스 시스템과 엄격한 교복 규정이 있습니다. Parents' Evening(학부모 상담), Sports Day(운동회), INSET Day(교사 연수일) 등이 있습니다. Bank Holiday를 고려해야 합니다."
    },
    "기타": {
        "name": "기타 국가",
        "culture": "해당 국가의 교육 문화와 주요 기념일, 학교 행사 전통을 고려하여 분석하겠습니다."
    }
}

def get_prompt(country, text_input=None, has_image=False):
    """국가별 프롬프트 생성"""
    country_info = COUNTRY_INFO.get(country, COUNTRY_INFO["기타"])
    
    prompt = f"""당신은 {country_info['name']}의 교육 문화와 기념일을 잘 아는 전문가입니다.

다음 배경 정보를 바탕으로 학교 알림장을 분석해주세요:
{country_info['culture']}

사용자가 제공한 학교 알림장을 분석하여 다음 형식으로 정확하게 응답해주세요:

🌐 **원문 번역 (한국어)**:
[학교 알림장의 원문을 한국어로 정확하고 자연스럽게 번역해주세요. 전문 용어나 현지 특유의 표현이 있으면 주석을 달아주세요.]

📌 **행사명**: [행사 이름을 명확하게]
📅 **일시**: [날짜와 시간을 구체적으로]
✅ **준비물 체크리스트**:
- [준비물 1] (현지 용어가 있으면 함께 표기)
- [준비물 2]
- [준비물 3]
...

🌍 **Cultural Context (문화적 배경)**:
[해당 행사나 준비물과 관련된 {country_info['name']}의 교육 문화, 현지 관습, 중요한 맥락을 간결하게 설명해주세요. 불릿포인트 형식으로 핵심 사항을 나열하되, 각 포인트에 대한 설명은 최대 2-3문장으로 간략하게 작성해주세요. 특히 한인 부모가 놓치기 쉬운 부분, 현지에서 특별히 중요한 점, 해당 국가만의 특징적인 교육 관습을 핵심만 간결하게 강조해주세요.]

💡 **실용적인 팁**:
[실제로 준비할 때 유용한 팁, 주의사항, 추가로 알아두면 좋은 정보를 불릿포인트 형식으로 제공해주세요. 각 팁은 최대 2-3문장으로 간결하게 작성하고, 핵심만 전달해주세요.]

**중요한 작성 지침:**
- 🌍 Cultural Context (문화적 배경): 불릿포인트로 핵심 사항 나열, 각 포인트 설명은 2-3문장 이내로 간결하게
- 💡 실용적인 팁: 불릿포인트로 제시, 각 팁은 2-3문장 이내로 간결하게
- 두 섹션 모두 불필요한 부연 설명, 반복, 장황한 설명은 피하고 핵심만 전달해주세요
- 전체 설명 분량은 현재 수준의 약 60% 정도로 작성해주세요

응답은 한국어로 작성하고, 친근하고 따뜻한 톤으로 작성해주세요. 원문 번역은 자세하게, Cultural Context와 실용적인 팁은 간결하게 작성해주세요."""

    if text_input:
        prompt += f"\n\n다음 학교 알림장을 분석해주세요:\n\n{text_input}"
    elif has_image:
        prompt += "\n\n업로드된 이미지의 학교 알림장을 분석해주세요. 이미지에서 텍스트를 정확히 읽고 분석해주세요."
    else:
        prompt += "\n\n학교 알림장을 분석해주세요."

    return prompt

def analyze_with_gemini(text_input, image_input, country, api_key, model_name="gemini-pro"):
    """Google Gemini API를 사용하여 학교 알림장 분석"""
    try:
        # Gemini API 설정
        genai.configure(api_key=api_key)
        
        # 먼저 사용 가능한 모델 목록을 확인
        available_models = []
        try:
            for m in genai.list_models():
                if hasattr(m, 'supported_generation_methods'):
                    if 'generateContent' in m.supported_generation_methods:
                        available_models.append(m.name)
        except Exception as e:
            pass  # 목록 조회 실패 시 기본 모델 시도
        
        # 사용할 모델 결정
        model = None
        last_error = None
        
        # 이미지가 있으면 vision 모델 필요
        if image_input:
            # 최신 모델 이름 우선순위 (vision 지원 모델)
            try_models = [
                "models/gemini-1.5-flash-latest",
                "models/gemini-1.5-pro-latest",
                "models/gemini-pro-vision",
                "gemini-1.5-flash-latest",
                "gemini-1.5-pro-latest", 
                "gemini-pro-vision",
            ]
        else:
            # 텍스트만 있는 경우
            try_models = [
                "models/gemini-1.5-flash-latest",
                "models/gemini-1.5-pro-latest",
                "models/gemini-pro",
                "gemini-1.5-flash-latest",
                "gemini-1.5-pro-latest",
                "gemini-pro",
            ]
        
        # 사용 가능한 모델 목록이 있으면 그 중에서 선택
        if available_models:
            for test_model in try_models:
                if test_model in available_models or test_model.replace("models/", "") in [m.replace("models/", "") for m in available_models]:
                    try:
                        model = genai.GenerativeModel(test_model)
                        break
                    except:
                        continue
            
            # 위 모델 중 없으면 첫 번째 사용 가능한 모델 사용
            if model is None:
                for available in available_models:
                    try:
                        model = genai.GenerativeModel(available)
                        break
                    except:
                        continue
        
        # 모델 목록 없이 직접 시도
        if model is None:
            for test_model in try_models:
                try:
                    model = genai.GenerativeModel(test_model)
                    break
                except Exception as e:
                    last_error = str(e)
                    continue
        
        if model is None:
            raise Exception(f"사용 가능한 모델을 찾을 수 없습니다. 사용 가능한 모델: {available_models}. 마지막 에러: {last_error}")
        
        # 프롬프트 생성
        has_image = image_input is not None
        prompt = get_prompt(country, text_input, has_image)
        
        # 이미지가 있는 경우 멀티모달 처리
        if image_input:
            # 이미지를 PIL Image로 변환
            img = Image.open(image_input)
            
            # 이미지와 텍스트를 함께 전달 (Gemini Vision API)
            response = model.generate_content(
                [prompt, img],
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 4096,  # Cultural Context 섹션을 위해 토큰 수 증가
                }
            )
        else:
            # 텍스트만 있는 경우
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 4096,  # Cultural Context 섹션을 위해 토큰 수 증가
                }
            )
        
        # 응답 텍스트 추출
        if hasattr(response, 'text') and response.text:
            return response.text
        elif hasattr(response, 'candidates') and response.candidates:
            # 응답이 블록되었거나 비어있는 경우
            candidate = response.candidates[0]
            if hasattr(candidate, 'finish_reason'):
                if candidate.finish_reason == "SAFETY":
                    return "❌ 안전 필터에 의해 응답이 차단되었습니다. 다른 내용을 입력해주세요."
                elif candidate.finish_reason == "RECITATION":
                    return "❌ 저작권 문제로 응답이 차단되었습니다."
                elif candidate.finish_reason == "OTHER":
                    return "❌ 응답 생성 중 문제가 발생했습니다. 다시 시도해주세요."
            
            # candidates에 내용이 있는 경우
            if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                text_parts = []
                for part in candidate.content.parts:
                    if hasattr(part, 'text'):
                        text_parts.append(part.text)
                if text_parts:
                    return "\n".join(text_parts)
        
        return "❌ 응답을 생성할 수 없습니다. 응답 형식을 확인할 수 없습니다."
        
    except Exception as e:
        error_msg = str(e)
        # API 키 관련 오류
        if "API_KEY" in error_msg or "api_key" in error_msg or "API key" in error_msg:
            return f"❌ API 키 오류: {error_msg}\n\nGEMINI_API_KEY를 확인해주세요. .env 파일에 'GEMINI_API_KEY=your_key_here' 형식으로 설정하세요."
        # 할당량 관련 오류
        elif "quota" in error_msg.lower() or "rate limit" in error_msg.lower() or "429" in error_msg:
            return f"❌ API 할당량 초과: {error_msg}\n\n잠시 후 다시 시도해주세요."
        # 인증 오류
        elif "401" in error_msg or "403" in error_msg or "unauthorized" in error_msg.lower() or "forbidden" in error_msg.lower():
            return f"❌ 인증 오류: {error_msg}\n\nAPI 키가 올바르지 않습니다. Google AI Studio에서 새로운 API 키를 발급받아주세요."
        # 네트워크 오류
        elif "connection" in error_msg.lower() or "network" in error_msg.lower() or "timeout" in error_msg.lower():
            return f"❌ 네트워크 오류: {error_msg}\n\n인터넷 연결을 확인해주세요."
        # 기타 오류
        else:
            return f"❌ 오류가 발생했습니다: {error_msg}\n\n문제가 계속되면 API 키와 네트워크 연결을 확인해주세요."

def is_valid_checklist_item(item):
    """준비물 항목이 유효한지 검증"""
    if not item or not isinstance(item, str):
        return False
    
    # 공백 제거 후 검증
    cleaned = item.strip()
    
    # 빈 문자열 체크
    if not cleaned:
        return False
    
    # 너무 짧은 항목 제거 (2자 이하)
    if len(cleaned) <= 2:
        return False
    
    # 대시만 있는 항목 제거 (-, —, ─, – 등)
    dash_only_patterns = [r'^[-—─–]+$', r'^[-—─–\s]+$']
    for pattern in dash_only_patterns:
        if re.match(pattern, cleaned):
            return False
    
    # 불필요한 문구 패턴 체크
    invalid_patterns = [
        r'^없음',
        r'^없습니다',
        r'^없어요',
        r'^없다',
        r'특별한\s*준비물\s*없',
        r'준비물\s*없',
        r'^[-•]\s*$',  # 대시나 불릿만 있는 경우
        r'^\.+$',  # 점만 있는 경우
        r'^_+$',  # 언더스코어만 있는 경우
        r'^\s*$',  # 공백만 있는 경우
    ]
    
    for pattern in invalid_patterns:
        if re.search(pattern, cleaned, re.IGNORECASE):
            return False
    
    # 실제 준비물로 보이는 항목만 통과 (한글, 영문, 숫자, 기본 특수문자 포함)
    # 최소 3자 이상의 의미있는 텍스트가 있어야 함
    meaningful_chars = re.findall(r'[가-힣a-zA-Z0-9]+', cleaned)
    if not meaningful_chars or len(''.join(meaningful_chars)) < 3:
        return False
    
    return True

def parse_analysis_result(result, country):
    """분석 결과를 구조화된 데이터로 파싱"""
    parsed_data = {
        'event_name': '',
        'event_date': '',
        'event_time': '',
        'country': country,
        'checklist_items': [],
        'translation': '',
        'cultural_context': '',
        'tips': '',
        'memo': ''  # 메모는 빈 값으로 초기화
    }
    
    # 행사명 추출
    if "📌" in result:
        name_match = re.search(r'📌\s*\*\*행사명\*\*:?\s*([^\n📅✅🌍💡]+)', result)
        if name_match:
            parsed_data['event_name'] = name_match.group(1).strip()
    
    # 일시 추출
    if "📅" in result:
        date_match = re.search(r'📅\s*\*\*일시\*\*:?\s*([^\n📌✅🌍💡]+)', result)
        if date_match:
            date_str = date_match.group(1).strip()
            # 날짜 형식 추출 (YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY 등)
            # 다양한 날짜 패턴 시도
            date_patterns = [
                r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
                r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
                r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
                r'\d{4}년\s*\d{1,2}월\s*\d{1,2}일',  # 2024년 12월 25일
                r'\d{1,2}월\s*\d{1,2}일',  # 12월 25일
            ]
            
            extracted_date = None
            for pattern in date_patterns:
                match = re.search(pattern, date_str)
                if match:
                    extracted_date = match.group(0)
                    break
            
            if extracted_date:
                # 날짜를 YYYY-MM-DD 형식으로 변환 시도
                try:
                    # 한국어 날짜 형식 처리
                    if '년' in extracted_date:
                        date_parts = re.findall(r'\d+', extracted_date)
                        if len(date_parts) >= 3:
                            year = date_parts[0]
                            month = date_parts[1].zfill(2)
                            day = date_parts[2].zfill(2)
                            parsed_data['event_date'] = f"{year}-{month}-{day}"
                        elif len(date_parts) == 2:
                            # 올해로 가정
                            current_year = datetime.now().year
                            month = date_parts[0].zfill(2)
                            day = date_parts[1].zfill(2)
                            parsed_data['event_date'] = f"{current_year}-{month}-{day}"
                    elif '/' in extracted_date:
                        # MM/DD/YYYY 형식
                        parts = extracted_date.split('/')
                        if len(parts) == 3:
                            parsed_data['event_date'] = f"{parts[2]}-{parts[0].zfill(2)}-{parts[1].zfill(2)}"
                    elif '-' in extracted_date and len(extracted_date.split('-')[0]) == 4:
                        # YYYY-MM-DD 형식
                        parsed_data['event_date'] = extracted_date
                    else:
                        parsed_data['event_date'] = extracted_date
                except:
                    parsed_data['event_date'] = extracted_date
                
                # 시간 추출
                time_match = re.search(r'(\d{1,2}:\d{2}|\d{1,2}시|\d{1,2}시\s*\d{1,2}분)', date_str)
                if time_match:
                    parsed_data['event_time'] = time_match.group(0)
            else:
                # 날짜 패턴이 없으면 전체 문자열을 날짜로 저장 (나중에 수동 수정 가능)
                parsed_data['event_date'] = date_str.split()[0] if date_str.split() else ''
                if len(date_str.split()) > 1:
                    parsed_data['event_time'] = ' '.join(date_str.split()[1:])
    
    # 준비물 추출
    if "✅" in result:
        checklist_match = re.search(r'✅\s*\*\*준비물 체크리스트\*\*:?\s*([^🌍💡📌📅]+)', result, re.DOTALL)
        if checklist_match:
            checklist_text = checklist_match.group(1)
            # 리스트 항목 추출
            items = re.findall(r'[-•]\s*([^\n]+)', checklist_text)
            all_items = [item.strip() for item in items if item.strip()]
            # 검증을 통과한 항목만 필터링
            valid_items = [item for item in all_items if is_valid_checklist_item(item)]
            filtered_items = [item for item in all_items if not is_valid_checklist_item(item)]
            
            # 필터링된 항목이 있으면 사용자에게 알림 (session_state에 저장)
            if filtered_items:
                st.session_state[f'filtered_checklist_{country}'] = {
                    'filtered_count': len(filtered_items),
                    'filtered_items': filtered_items,
                    'valid_count': len(valid_items)
                }
            
            parsed_data['checklist_items'] = valid_items
    
    # 원문 번역 추출
    if "🌐" in result:
        translation_match = re.search(r'🌐[^📌📅✅🌍💡]*([^📌📅✅🌍💡]+)', result)
        if translation_match:
            translation_text = translation_match.group(1)
            # 제목 제거
            translation_text = re.sub(r'\*\*원문 번역[^:]*\*\*:?\s*', '', translation_text).strip()
            parsed_data['translation'] = translation_text
    
    # 문화적 배경 추출
    if "🌍" in result:
        cultural_match = re.search(r'🌍[^💡📌📅✅]*([^💡📌📅✅]+)', result, re.DOTALL)
        if cultural_match:
            cultural_text = cultural_match.group(1)
            # 제목 제거
            cultural_text = re.sub(r'\*\*Cultural Context[^:]*\*\*:?\s*', '', cultural_text, flags=re.IGNORECASE).strip()
            parsed_data['cultural_context'] = cultural_text
    
    # 실용적인 팁 추출
    if "💡" in result:
        tips_match = re.search(r'💡[^📌📅✅🌍]*([^📌📅✅🌍]+)', result, re.DOTALL)
        if tips_match:
            tips_text = tips_match.group(1)
            # 제목 제거
            tips_text = re.sub(r'\*\*실용적인 팁\*\*:?\s*', '', tips_text).strip()
            parsed_data['tips'] = tips_text
    
    return parsed_data

def calculate_dday(event_date_str):
    """D-day 계산"""
    try:
        if event_date_str and '-' in event_date_str:
            event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
            delta = (event_date - date.today()).days
            if delta == 0:
                return "D-Day", "#FF6B6B"
            elif delta > 0:
                return f"D-{delta}", "#4ECDC4" if delta <= 7 else "#95E1D3"
            else:
                return f"D+{abs(delta)}", "#A0A0A0"
    except:
        pass
    return "", "#D3D3D3"

def calculate_progress(checklist_items):
    """준비물 진행률 계산"""
    if not checklist_items:
        return 0, 0, 0
    total = len(checklist_items)
    checked = sum(1 for item in checklist_items if item.get('checked', False))
    percentage = int((checked / total) * 100) if total > 0 else 0
    return checked, total, percentage

def render_dashboard():
    """대시보드 UI 렌더링"""
    st.markdown("### 📅 나의 일정 (Dashboard)")
    
    # 데이터베이스 초기화
    init_database()
    
    # 선택된 이벤트 상태 초기화
    if 'selected_event_id' not in st.session_state:
        st.session_state.selected_event_id = None
    
    # 다가오는 이벤트 섹션
    st.markdown("#### 🔜 다가오는 이벤트")
    future_events = get_events(future_only=True)
    
    # 아이 태그 색상 설정
    tag_colors = {
        '첫째': '#FFB6C1',
        '둘째': '#87CEEB',
        '둘 다': '#DDA0DD',
        '없음': '#D3D3D3'
    }
    
    if future_events:
        # 컴팩트한 이벤트 카드 그리드
        for event in future_events:
            tag_color = tag_colors.get(event.get('child_tag', '없음'), '#D3D3D3')
            dday_text, dday_color = calculate_dday(event.get('event_date', ''))
            checked, total, progress = calculate_progress(event.get('checklist_with_status', []))
            
            # 선택된 이벤트인지 확인
            is_selected = st.session_state.selected_event_id == event['id']
            border_width = "3px" if is_selected else "1px"
            border_color = "#8B7D9B" if is_selected else "#E0E0E0"
            
            # 컴팩트 카드
            col_card, col_actions = st.columns([5, 1])
            
            with col_card:
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%);
                        padding: 0.8rem 1rem;
                        border-radius: 12px;
                        margin: 0.3rem 0;
                        border: {border_width} solid {border_color};
                        border-left: 4px solid {tag_color};
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        cursor: pointer;
                    ">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <span style="
                                background: {dday_color};
                                color: white;
                                padding: 0.3rem 0.6rem;
                                border-radius: 8px;
                                font-weight: bold;
                                font-size: 0.85rem;
                                min-width: 50px;
                                text-align: center;
                            ">{dday_text}</span>
                            <div>
                                <strong style="color: #333; font-size: 1rem;">{event['event_name']}</strong>
                                <div style="color: #888; font-size: 0.8rem;">
                                    📅 {event.get('event_date', '')} {event.get('event_time', '')} 
                                    <span style="background-color: {tag_color}; padding: 0.1rem 0.4rem; border-radius: 4px; margin-left: 5px; font-size: 0.75rem;">👶 {event.get('child_tag', '없음')}</span>
                                </div>
                            </div>
                        </div>
                        <div style="text-align: right; min-width: 80px;">
                            <div style="font-size: 0.75rem; color: #888;">준비물</div>
                            <div style="font-weight: bold; color: {'#4ECDC4' if progress == 100 else '#FFB347'};">{checked}/{total}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_actions:
                if st.button("📋", key=f"select_{event['id']}", help="상세보기", use_container_width=True):
                    if st.session_state.selected_event_id == event['id']:
                        st.session_state.selected_event_id = None
                    else:
                        st.session_state.selected_event_id = event['id']
                    st.rerun()
        
        # 선택된 이벤트 상세 정보
        if st.session_state.selected_event_id:
            selected_event = next((e for e in future_events if e['id'] == st.session_state.selected_event_id), None)
            if selected_event:
                render_event_detail(selected_event, tag_colors, is_past=False, prefix="detail")
    else:
        st.info("📭 다가오는 이벤트가 없습니다.")
    
    st.markdown("---")
    
    # 전체 일정 (접을 수 있는 섹션)
    with st.expander("📚 전체 일정 보기", expanded=False):
        all_events = get_events(future_only=False)
        
        if all_events:
            # 지난 일정과 미래 일정 분리
            past_events = []
            upcoming_events = []
            
            for event in all_events:
                is_past = False
                if event.get('event_date'):
                    try:
                        date_str = event['event_date']
                        if '-' in date_str:
                            event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                            if event_date < date.today():
                                is_past = True
                    except:
                        pass
                
                if is_past:
                    past_events.append(event)
                else:
                    upcoming_events.append(event)
            
            # 미래 일정 (접을 수 있는 섹션)
            if upcoming_events:
                with st.expander(f"🔜 예정된 일정 ({len(upcoming_events)}개)", expanded=True):
                    for event in upcoming_events:
                        render_event_compact_row(event, tag_colors, is_past=False, prefix="all")
            
            # 지난 일정 (접을 수 있는 섹션)
            if past_events:
                with st.expander(f"📜 지난 일정 ({len(past_events)}개)", expanded=False):
                    for event in past_events:
                        render_event_compact_row(event, tag_colors, is_past=True, prefix="past")
        else:
            st.info("📭 저장된 일정이 없습니다.")

def render_event_compact_row(event, tag_colors, is_past, prefix):
    """컴팩트한 이벤트 행 렌더링 (개별 상세 정보 접기/펼치기 기능 포함)"""
    tag_color = tag_colors.get(event.get('child_tag', '없음'), '#D3D3D3')
    dday_text, dday_color = calculate_dday(event.get('event_date', ''))
    opacity = "0.5" if is_past else "1"
    past_label = " (지난 일정)" if is_past else ""
    checked, total, progress = calculate_progress(event.get('checklist_with_status', []))
    
    # 일정 요약 정보 (상세보기 헤더로 사용)
    event_time_display = f" {event.get('event_time', '')}" if event.get('event_time') else ""
    summary_text = f"📌 {event['event_name']}{past_label} | 📅 {event.get('event_date', '')}{event_time_display} | 👶 {event.get('child_tag', '없음')} | ✅ {checked}/{total}"
    
    # expander 상태를 session_state에 저장 (체크박스 클릭 시에도 유지)
    expander_key = f"expanded_{prefix}_{event['id']}"
    
    # 편집 모드일 때는 expander를 닫고 상세 정보를 숨김
    if st.session_state.get(f'editing_{event["id"]}', False):
        st.session_state[expander_key] = False
        # 편집 모드일 때는 expander를 표시하지 않음
        # 편집 폼만 표시
        render_edit_mode(event, prefix)
        return  # 여기서 함수 종료
    
    # expander 상태 가져오기 (체크박스 클릭으로 업데이트된 상태 유지)
    expanded_state = st.session_state.get(expander_key, False)
    
    # 각 일정을 expander로 감싸서 상세 정보 접기/펼치기 가능하게 함
    with st.expander(summary_text, expanded=expanded_state):
        # 상세 정보 렌더링
        render_event_compact_detail(event, tag_colors, is_past, prefix)

def render_event_compact_detail(event, tag_colors, is_past, prefix):
    """일정 상세 정보 (컴팩트 버전) 렌더링"""
    tag_color = tag_colors.get(event.get('child_tag', '없음'), '#D3D3D3')
    checked, total, progress = calculate_progress(event.get('checklist_with_status', []))
    
    # 메모 내용
    memo_content = event.get('memo', '') or ''
    if memo_content:
        memo_escaped = html_escape.escape(memo_content)
        memo_display = memo_escaped.replace('\n', '<br>')
        st.markdown(f"""
            <div style="
                background: #FFF9E6;
                padding: 0.8rem;
                border-radius: 8px;
                border-left: 3px solid #FFD93D;
                margin-bottom: 1rem;
            ">
                <strong>📝 메모:</strong><br>{memo_display}
            </div>
        """, unsafe_allow_html=True)
    
    # 상세 정보 카드
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border-left: 4px solid {tag_color};
        ">
            <p><strong>📅 날짜:</strong> {event.get('event_date', '')} {event.get('event_time', '')}</p>
            <p><strong>👶 아이:</strong> <span style="background-color: {tag_color}; padding: 0.2rem 0.5rem; border-radius: 5px;">{event.get('child_tag', '없음')}</span></p>
            <p><strong>✅ 준비물 진행률:</strong> {checked}/{total} 완료</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 진행률 바
    if total > 0:
        st.progress(progress / 100, text=f"준비물 진행률: {checked}/{total}")
    
    # 준비물 체크리스트
    if event.get('checklist_with_status'):
        st.markdown("**✅ 준비물 체크리스트:**")
        
        cols = st.columns(2)
        for idx, item in enumerate(event['checklist_with_status']):
            with cols[idx % 2]:
                checked = st.checkbox(
                    item['name'],
                    value=item['checked'],
                    key=f"check_{prefix}_{event['id']}_{item['id']}",
                    disabled=is_past
                )
                if not is_past and checked != item['checked']:
                    # 체크박스 클릭 시 expander 상태 유지 (expander 안에 있으므로 항상 열린 상태로)
                    expander_key = f"expanded_{prefix}_{event['id']}"
                    st.session_state[expander_key] = True
                    
                    update_checklist_item(item['id'], checked)
                    st.rerun()
    
    # 편집/삭제 버튼
    col_edit, col_delete = st.columns(2)
    
    with col_edit:
        if st.button("✏️ 편집", key=f"edit_detail_{prefix}_{event['id']}", use_container_width=True):
            st.session_state[f'editing_{event["id"]}'] = True
            st.rerun()
    
    with col_delete:
        if st.button("🗑️ 삭제", key=f"delete_detail_{prefix}_{event['id']}", use_container_width=True):
            delete_event(event['id'])
            st.success("이벤트가 삭제되었습니다.")
            st.rerun()

def render_event_detail(event, tag_colors, is_past, prefix):
    """이벤트 상세 정보 렌더링"""
    st.markdown("---")
    st.markdown("#### 📋 일정 상세")
    
    tag_color = tag_colors.get(event.get('child_tag', '없음'), '#D3D3D3')
    checked, total, progress = calculate_progress(event.get('checklist_with_status', []))
    
    # 메모 내용
    memo_content = event.get('memo', '') or ''
    memo_html = ""
    if memo_content:
        memo_escaped = html_escape.escape(memo_content)
        memo_display = memo_escaped.replace('\n', '<br>')
        memo_html = f'<p style="background: #FFF9E6; padding: 0.8rem; border-radius: 8px; border-left: 3px solid #FFD93D;"><strong>📝 메모:</strong><br>{memo_display}</p>'
    
    # 상세 카드
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border-left: 5px solid {tag_color};
        ">
            <h3 style="color: #8B7D9B; margin-top: 0; margin-bottom: 1rem;">{event['event_name']}</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                <p><strong>📅 날짜:</strong> {event['event_date']} {event.get('event_time', '')}</p>
                <p><strong>👶 아이:</strong> <span style="background-color: {tag_color}; padding: 0.2rem 0.5rem; border-radius: 5px;">{event.get('child_tag', '없음')}</span></p>
                <p><strong>✅ 준비:</strong> {checked}/{total} 완료</p>
            </div>
            {memo_html}
        </div>
    """, unsafe_allow_html=True)
    
    # 진행률 바
    if total > 0:
        st.progress(progress / 100, text=f"준비물 진행률: {checked}/{total}")
    
    # 준비물 체크리스트
    if event.get('checklist_with_status'):
        st.markdown("**✅ 준비물 체크리스트:**")
        
        cols = st.columns(2)
        for idx, item in enumerate(event['checklist_with_status']):
            with cols[idx % 2]:
                checked = st.checkbox(
                    item['name'],
                    value=item['checked'],
                    key=f"check_{prefix}_{event['id']}_{item['id']}",
                    disabled=is_past
                )
                if not is_past and checked != item['checked']:
                    update_checklist_item(item['id'], checked)
                    st.rerun()
    
    # 버튼 영역
    col_edit, col_delete, col_close = st.columns([1, 1, 1])
    
    with col_edit:
        if st.button("✏️ 편집", key=f"edit_{prefix}_{event['id']}", use_container_width=True):
            st.session_state[f'editing_{event["id"]}'] = True
            st.rerun()
    
    with col_delete:
        if st.button("🗑️ 삭제", key=f"delete_{prefix}_{event['id']}", use_container_width=True):
            delete_event(event['id'])
            st.session_state.selected_event_id = None
            st.success("이벤트가 삭제되었습니다.")
            st.rerun()
    
    with col_close:
        if st.button("✖️ 닫기", key=f"close_{prefix}_{event['id']}", use_container_width=True):
            st.session_state.selected_event_id = None
            st.rerun()
    
    # 편집 모드
    if st.session_state.get(f'editing_{event["id"]}', False):
        render_edit_mode(event, prefix)

def render_edit_mode(event, prefix):
    """편집 모드 UI 렌더링"""
    st.markdown("---")
    st.markdown(f"#### ✏️ 일정 편집: {event['event_name']}")
    
    # 날짜 편집
    current_date = event.get('event_date', '')
    date_key = f"date_{prefix}_{event['id']}"
    try:
        if current_date and '-' in current_date:
            date_value = datetime.strptime(current_date, '%Y-%m-%d').date()
        else:
            date_value = date.today()
    except:
        date_value = date.today()
    
    col_date, col_time = st.columns(2)
    with col_date:
        st.date_input("📅 날짜", value=date_value, key=date_key)
    
    with col_time:
        current_time = event.get('event_time', '') or ''
        time_key = f"time_{prefix}_{event['id']}"
        st.text_input("⏰ 시간", value=current_time, key=time_key, placeholder="예: 오전 10시")
    
    # 메모 편집
    current_memo = event.get('memo', '') or ''
    memo_edit_key = f"memo_{prefix}_{event['id']}"
    st.text_area("📝 메모", value=current_memo, key=memo_edit_key, placeholder="일정에 대한 메모를 입력하세요...", height=80)
    
    # 준비물 편집
    st.markdown("**✅ 준비물 관리:**")
    checklist_items = event.get('checklist_with_status', [])
    
    for idx, item in enumerate(checklist_items):
        col_name, col_del = st.columns([5, 1])
        with col_name:
            new_item_name = st.text_input(
                f"항목 {idx + 1}",
                value=item['name'],
                key=f"item_{prefix}_{event['id']}_{item['id']}",
                label_visibility="collapsed"
            )
            if new_item_name != item['name']:
                if f'checklist_updates_{event["id"]}' not in st.session_state:
                    st.session_state[f'checklist_updates_{event["id"]}'] = {}
                st.session_state[f'checklist_updates_{event["id"]}'][item['id']] = new_item_name
        
        with col_del:
            if st.button("🗑️", key=f"del_item_{prefix}_{event['id']}_{item['id']}", help="삭제"):
                delete_checklist_item(item['id'])
                st.rerun()
    
    # 새 준비물 추가
    col_new, col_add = st.columns([4, 1])
    with col_new:
        new_item = st.text_input("새 준비물", key=f"new_item_{prefix}_{event['id']}", placeholder="예: 도시락, 운동화, 색연필 등")
    with col_add:
        if st.button("➕", key=f"add_item_{prefix}_{event['id']}", help="추가"):
            if new_item and new_item.strip():
                try:
                    # 검증 후 추가
                    if not is_valid_checklist_item(new_item.strip()):
                        st.warning("⚠️ 유효하지 않은 준비물입니다. 실제 필요한 준비물(예: 도시락, 운동화 등)을 입력해주세요.")
                        st.info("💡 다음 항목은 추가할 수 없습니다: '-', '없음', 2자 이하, 대시만 있는 항목 등")
                    else:
                        add_checklist_item(event['id'], new_item.strip())
                        st.success(f"✅ '{new_item.strip()}'가 추가되었습니다!")
                        st.rerun()
                except ValueError as e:
                    st.warning(f"⚠️ {str(e)}")
                except Exception as e:
                    st.error(f"❌ 준비물 추가 중 오류가 발생했습니다: {str(e)}")
    
    # 저장/취소 버튼
    col_save, col_cancel = st.columns(2)
    with col_save:
        if st.button("💾 저장", key=f"save_{prefix}_{event['id']}", use_container_width=True, type="primary"):
            saved_date = st.session_state.get(date_key)
            saved_time = st.session_state.get(time_key, current_time)
            saved_memo = st.session_state.get(memo_edit_key, current_memo)
            
            saved_date_str = saved_date.strftime('%Y-%m-%d') if saved_date else current_date
            
            update_event(event['id'], {
                'event_name': event['event_name'],
                'event_date': saved_date_str,
                'event_time': saved_time if saved_time else '',
                'country': event.get('country', ''),
                'child_tag': event.get('child_tag', '없음'),
                'memo': saved_memo if saved_memo else ''
            })
            
            # 준비물 이름 변경사항 저장 (검증 후)
            validation_errors = []
            if f'checklist_updates_{event["id"]}' in st.session_state:
                for item_id, new_name in st.session_state[f'checklist_updates_{event["id"]}'].items():
                    if new_name and new_name.strip():
                        try:
                            if is_valid_checklist_item(new_name.strip()):
                                update_checklist_item_name(item_id, new_name.strip())
                            else:
                                validation_errors.append(f"'{new_name.strip()}' - 유효하지 않은 준비물입니다.")
                        except ValueError as e:
                            validation_errors.append(f"'{new_name.strip()}' - {str(e)}")
                        except Exception as e:
                            validation_errors.append(f"'{new_name.strip()}' - 저장 중 오류: {str(e)}")
                del st.session_state[f'checklist_updates_{event["id"]}']
            
            # 검증 오류가 있으면 알림
            if validation_errors:
                for error in validation_errors:
                    st.warning(f"⚠️ {error}")
                st.info("💡 실제 필요한 준비물(예: 도시락, 운동화, 색연필 등)을 입력해주세요.")
            
            st.session_state[f'editing_{event["id"]}'] = False
            if not validation_errors:
                st.success("일정이 수정되었습니다!")
            st.rerun()
    
    with col_cancel:
        if st.button("❌ 취소", key=f"cancel_{prefix}_{event['id']}", use_container_width=True):
            if f'checklist_updates_{event["id"]}' in st.session_state:
                del st.session_state[f'checklist_updates_{event["id"]}']
            st.session_state[f'editing_{event["id"]}'] = False
            st.rerun()

def main():
    # 데이터베이스 초기화
    init_database()
    
    # 사이드바
    with st.sidebar:
        st.markdown("### ⚙️ 설정")
        
        # 국가 선택 (session_state에 저장되어 다음 접속 시 복원)
        country_options = ["네덜란드", "미국", "독일", "영국", "기타"]
        
        # 이전에 선택한 국가가 있으면 복원, 없으면 기본값(네덜란드)
        if 'selected_country' not in st.session_state:
            st.session_state.selected_country = "네덜란드"
        
        # selectbox에서 현재 선택된 국가의 인덱스 찾기
        default_index = country_options.index(st.session_state.selected_country) if st.session_state.selected_country in country_options else 0
        
        country = st.selectbox(
            "🌍 국가 선택",
            options=country_options,
            index=default_index,
            key="country_selectbox"
        )
        
        # 국가가 변경되면 session_state에 저장
        if country != st.session_state.selected_country:
            st.session_state.selected_country = country
        
        # API 키 가져오기 (st.secrets > .env)
        api_key = None
        
        # st.secrets에서 확인
        try:
            if "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
        except:
            pass
        
        # 환경 변수에서 확인
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            st.warning("⚠️ API 키를 환경 변수에 설정해주세요.")
            st.info("💡 API 키는 [Google AI Studio](https://makersuite.google.com/app/apikey)에서 발급받을 수 있습니다.")
            st.info("📝 `.env` 파일에 `GEMINI_API_KEY=your_key_here`를 추가하거나 Streamlit Secrets에 설정하세요.")
        
        # 아이 관리 섹션 (자연스러운 구분선과 간격)
        st.markdown("<div style='margin-top: 2rem; padding-top: 1.5rem; border-top: 2px solid #e8e8e8;'></div>", unsafe_allow_html=True)
        st.markdown("### 👶 아이 관리")
        children_list = get_children()
        
        if children_list:
            st.markdown("**등록된 아이:**")
            for idx, child in enumerate(children_list):
                # 아이 항목을 한 행에 배치: 이름 + 버튼
                col_name, col_edit, col_delete = st.columns([3, 1, 1], gap="small")
                
                with col_name:
                    # 아이 이름 박스
                    st.markdown(f"""
                        <div style="
                            padding: 0.7rem 1rem;
                            background: #f8f9fa;
                            border-radius: 8px;
                            border: 1px solid #e0e0e0;
                            display: flex;
                            align-items: center;
                            min-height: 40px;
                        ">
                            <strong style="font-size: 1rem;">{child}</strong>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_edit:
                    # 수정 버튼 - 높이 제한
                    if st.button("✏️", key=f"edit_child_{idx}", help="수정", use_container_width=True, type="secondary"):
                        st.session_state[f'editing_child_{idx}'] = True
                        st.rerun()
                
                with col_delete:
                    # 삭제 버튼 - 높이 제한
                    if st.button("🗑️", key=f"delete_child_{idx}", help="삭제", use_container_width=True, type="secondary"):
                        delete_child(child)
                        st.success(f"✅ '{child}'가 삭제되었습니다.")
                        st.rerun()
                
                # 간격 조정
                st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
                
                # 수정 모드
                if st.session_state.get(f'editing_child_{idx}', False):
                    st.markdown("""
                        <div style="
                            padding: 0.8rem;
                            background: #fff3cd;
                            border-radius: 8px;
                            margin-top: 0.5rem;
                            margin-bottom: 0.5rem;
                            border-left: 3px solid #ffc107;
                        ">
                            <strong>✏️ 수정 모드</strong>
                        </div>
                    """, unsafe_allow_html=True)
                    new_name = st.text_input(
                        "새 이름 입력",
                        value=child,
                        key=f"edit_input_{idx}",
                        label_visibility="visible"
                    )
                    col_save_edit, col_cancel_edit = st.columns([1, 1])
                    with col_save_edit:
                        if st.button("💾 저장", key=f"save_edit_{idx}", use_container_width=True, type="primary"):
                            if new_name and new_name.strip() and new_name.strip() != child:
                                if update_child_name(child, new_name.strip()):
                                    st.success(f"✅ '{child}'이(가) '{new_name.strip()}'으로 변경되었습니다.")
                                    st.session_state[f'editing_child_{idx}'] = False
                                    st.rerun()
                                else:
                                    st.error("❌ 같은 이름의 아이가 이미 존재합니다.")
                            elif new_name and new_name.strip() == child:
                                st.session_state[f'editing_child_{idx}'] = False
                                st.rerun()
                            else:
                                st.warning("⚠️ 아이 이름을 입력해주세요.")
                    with col_cancel_edit:
                        if st.button("❌ 취소", key=f"cancel_edit_{idx}", use_container_width=True):
                            st.session_state[f'editing_child_{idx}'] = False
                            st.rerun()
        else:
            st.info("💡 등록된 아이가 없습니다. 아래에서 아이를 추가해주세요.")
        
        # 아이 추가 섹션
        st.markdown("<div style='margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #e0e0e0;'></div>", unsafe_allow_html=True)
        st.markdown("**➕ 아이 추가:**")
        new_child_name = st.text_input(
            "아이 이름 입력",
            key="new_child_input",
            placeholder="예: 첫째, 둘째, 민수, 영희"
        )
        if st.button("➕ 아이 추가", use_container_width=True):
            if new_child_name and new_child_name.strip():
                if add_child(new_child_name.strip()):
                    st.success(f"✅ '{new_child_name.strip()}'이(가) 추가되었습니다!")
                    st.rerun()
                else:
                    st.error("❌ 같은 이름의 아이가 이미 존재합니다.")
            else:
                st.warning("⚠️ 아이 이름을 입력해주세요.")
    
    # 메인 영역 - 커스텀 제목 디자인
    st.markdown("""
        <div class="app-title">
            <span style="font-size: 2rem;">🎒</span>
            <div style="display: flex; flex-direction: column; align-items: center; gap: 0.2rem;">
                <span class="app-title-main" style="white-space: nowrap;">눈치코치</span>
                <span class="app-title-main" style="font-size: 1.2rem; font-weight: 600; opacity: 0.9;">Sense Coach</span>
            </div>
        </div>
        <div class="app-title-subtitle">
            🌍 현지 학교 알림장의 행간을 읽어주는<br>AI 문화 비서
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # 탭 생성
    tab1, tab2 = st.tabs(["📝 분석하기", "📅 나의 일정 (Dashboard)"])
    
    with tab1:
        # 텍스트 입력
        st.markdown("### 📝 학교 알림장 입력")
        text_input = st.text_area(
            "알림장 내용을 붙여넣어주세요",
            height=200,
            placeholder="학교에서 받은 알림장의 내용을 여기에 붙여넣어주세요..."
        )
        
        # 이미지 업로드
        st.markdown("### 📷 이미지 업로드 (Vision AI 강화)")
        image_input = st.file_uploader(
            "알림장 스크린샷 또는 사진을 업로드하세요",
            type=["png", "jpg", "jpeg", "webp"],
            help="이미지에서 텍스트를 자동으로 추출하고 분석합니다. 텍스트 입력과 함께 사용하면 더 정확합니다."
        )
        
        if image_input:
            st.success(f"✅ 이미지 업로드 완료: {image_input.name}")
            st.info("✨ AI가 이미지에서 텍스트를 자동으로 읽어 분석합니다!")
        
        st.markdown("---")
        
        # 분석 버튼
        analyze_button = st.button("🔍 분석하기", use_container_width=True)
        
        # 분석 실행
        if analyze_button:
            # 입력 검증
            if not text_input and not image_input:
                st.error("⚠️ 텍스트 또는 이미지를 입력해주세요.")
                st.stop()
            
            if not api_key:
                st.error("⚠️ API 키를 설정해주세요.")
                st.error("💡 `.env` 파일에 `GEMINI_API_KEY=your_api_key`를 추가하거나 Streamlit Secrets에 설정해주세요.")
                st.stop()
            
            # 로딩 메시지 (이미지 여부에 따라 다르게 표시)
            if image_input:
                loading_msg = "🔍 이미지에서 텍스트를 추출하고 분석 중... 잠시만 기다려주세요!"
            else:
                loading_msg = "🤔 AI가 알림장을 분석하고 있어요... 잠시만 기다려주세요!"
            
            try:
                # 이미지가 있으면 자동으로 vision 모델 사용, 없으면 기본 모델 사용
                actual_model_name = "gemini-pro-vision" if image_input else "gemini-pro"
                
                with st.spinner(loading_msg):
                    result = analyze_with_gemini(text_input, image_input, country, api_key, actual_model_name)
                    
                    # 결과가 에러 메시지인지 확인
                    if not result:
                        st.error("❌ 분석 결과를 받을 수 없습니다. 다시 시도해주세요.")
                        st.stop()
                    
                    if result.startswith("❌"):
                        st.error(result)
                        st.stop()
                    
                    # 분석 결과를 session_state에 저장 (rerun 시에도 유지)
                    st.session_state['last_analysis_result'] = result
                    st.session_state['last_analysis_parsed'] = parse_analysis_result(result, country)
                    
            except Exception as e:
                st.error(f"❌ 분석 중 오류가 발생했습니다: {str(e)}")
                st.info("💡 문제가 계속되면 페이지를 새로고침하고 다시 시도해주세요.")
        
        # session_state에 저장된 결과가 있으면 표시 (selectbox rerun 시 유지)
        if 'last_analysis_result' in st.session_state:
            result = st.session_state['last_analysis_result']
            parsed_data = st.session_state.get('last_analysis_parsed', {})
            
            # 결과 출력
            st.markdown("---")
            st.markdown("### ✨ 분석 결과")
            
            # 결과를 섹션별로 파싱하여 표시
            # 원문 번역, 주요 정보, Cultural Context, 실용적인 팁 순서로 구분
            
            # 원문 번역 섹션 추출
            if "🌐" in result and ("원문 번역" in result or "번역" in result):
                # 번역 섹션 분리
                parts = result.split("🌐", 1)
                if len(parts) > 1:
                    translation_part = "🌐" + parts[1]
                    # 다음 섹션 마커 찾기
                    next_markers = ["📌", "🌍", "💡"]
                    translation_section = translation_part
                    
                    for marker in next_markers:
                        if marker in translation_part:
                            translation_section = translation_part.split(marker)[0].strip()
                            break
                    
                    # 번역 섹션 표시
                    if translation_section:
                        # 섹션 제목 제거하고 내용만 추출
                        clean_translation = translation_section.replace("🌐", "").replace("**원문 번역 (한국어)**", "").replace("**원문 번역**", "").replace("**", "").strip()
                        if clean_translation.startswith(":"):
                            clean_translation = clean_translation[1:].strip()
                        
                        if clean_translation:
                            # 원문 번역을 접을 수 있는 expander로 표시
                            with st.expander("🌐 원문 번역 (한국어) - 클릭하여 보기", expanded=False):
                                st.markdown(f'<div class="result-card" style="background: linear-gradient(135deg, #e8f4f8 0%, #f0f8f0 100%); border-left: 5px solid #4CAF50;">{clean_translation.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            # 주요 정보 표시 (행사명, 일시, 준비물 등)
            # result에서 번역 섹션을 제외한 나머지 추출
            display_content = result
            
            # 번역 섹션 제거 (이미 별도로 표시했으므로)
            if "🌐" in display_content:
                # 번역 섹션의 시작과 끝 찾기
                translation_start = display_content.find("🌐")
                # 번역 섹션 이후 첫 번째 주요 섹션 찾기 (📌, 🌍, 💡)
                after_translation = display_content[translation_start:]
                next_markers = ["📌", "🌍", "💡"]
                translation_end_pos = len(after_translation)
                
                # 번역 섹션 다음 주요 섹션 찾기
                for marker in next_markers:
                    pos = after_translation.find(marker, 1)  # 🌐 다음부터 찾기
                    if pos != -1 and pos < translation_end_pos:
                        translation_end_pos = pos
                
                # 번역 섹션 제거
                if translation_end_pos < len(after_translation):
                    # 번역 섹션 이후 내용만 사용
                    display_content = after_translation[translation_end_pos:]
                else:
                    # 번역 섹션이 마지막이면 번역 섹션 이전 내용 사용
                    display_content = display_content[:translation_start]
            
            # 주요 정보 표시 (📌 행사명, 📅 일시, ✅ 준비물)
            if display_content and display_content.strip():
                # 실용적인 팁 섹션 위치 찾기
                tips_pos = display_content.find("💡")
                tips_section = ""
                if tips_pos != -1:
                    tips_section = display_content[tips_pos:].strip()
                    display_content = display_content[:tips_pos].strip()
                
                # Cultural Context 섹션 위치 찾기
                cultural_pos = display_content.find("🌍")
                cultural_section = ""
                main_info = display_content
                
                if cultural_pos != -1:
                    # Cultural Context 이전이 주요 정보
                    main_info = display_content[:cultural_pos].strip()
                    # Cultural Context 섹션 추출
                    cultural_section = display_content[cultural_pos:].strip()
                    # Cultural Context 섹션에서 실용적인 팁이 포함되어 있으면 제거 (나중에 별도 처리)
                    if "💡" in cultural_section:
                        tips_pos_in_cultural = cultural_section.find("💡")
                        cultural_section = cultural_section[:tips_pos_in_cultural].strip()
                
                # 주요 정보 표시 (행사명, 일시, 준비물)
                if main_info:
                    st.markdown("### 📋 행사 정보 및 준비물")
                    st.markdown(f'<div class="result-card">{main_info.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                
                # Cultural Context 표시
                if cultural_section:
                    # 제목 제거
                    clean_cultural = cultural_section
                    patterns = [
                        r'🌍\s*\*\*Cultural Context \(문화적 배경\)\*\*:?\s*',
                        r'🌍\s*\*\*Cultural Context\*\*:?\s*',
                        r'\*\*Cultural Context \(문화적 배경\)\*\*:?\s*',
                        r'\*\*Cultural Context\*\*:?\s*',
                        r'Cultural Context \(문화적 배경\):?\s*',
                        r'Cultural Context:?\s*',
                    ]
                    for pattern in patterns:
                        clean_cultural = re.sub(pattern, '', clean_cultural, flags=re.IGNORECASE)
                    
                    clean_cultural = clean_cultural.strip()
                    if clean_cultural.startswith(':'):
                        clean_cultural = clean_cultural[1:].strip()
                    
                    if clean_cultural:
                        st.markdown("### 🌍 Cultural Context (문화적 배경)")
                        st.warning(clean_cultural)
            
            # 실용적인 팁 섹션을 별도로 표시 (Cultural Context 블록 밖에서 처리)
            # result 전체에서 찾아서 표시 (remaining_content가 잘릴 수 있으므로)
            if "💡" in result:
                tips_index_in_result = result.find("💡")
                if tips_index_in_result != -1:
                    # 💡 이후의 모든 내용을 가져옴 (텍스트 끝까지 전체 내용)
                    tips_section_raw = result[tips_index_in_result:].strip()
                    
                    if tips_section_raw:
                        # 섹션 제목만 정확하게 제거하고 내용 전체 보존
                        clean_tips = tips_section_raw
                        
                        # 다양한 제목 패턴 제거 (정규표현식 사용)
                        tips_patterns = [
                            r'^💡\s*\*\*실용적인 팁\*\*:?\s*',
                            r'^💡\s*\*\*팁\*\*:?\s*',
                            r'^\*\*실용적인 팁\*\*:?\s*',
                            r'^\*\*팁\*\*:?\s*',
                            r'^실용적인 팁:?\s*',
                            r'^팁:?\s*',
                        ]
                        
                        for pattern in tips_patterns:
                            clean_tips = re.sub(pattern, '', clean_tips, flags=re.IGNORECASE | re.MULTILINE)
                        
                        # 앞뒤 공백 제거
                        clean_tips = clean_tips.strip()
                        
                        # 콜론으로 시작하면 제거
                        if clean_tips.startswith(':'):
                            clean_tips = clean_tips[1:].strip()
                        
                        if clean_tips:
                            st.markdown("### 💡 실용적인 팁")
                            # Streamlit 네이티브 방식으로 표시 (HTML 대신 expander 사용하여 전체 내용 표시)
                            st.info(clean_tips)
            
            # 저장 버튼 및 복사/다운로드 버튼
            st.markdown("---")
            
            # 저장된 파싱 데이터 사용 (session_state에서)
            parsed_data = st.session_state.get('last_analysis_parsed', {})
            
            # 필터링된 준비물 항목이 있으면 사용자에게 알림
            filter_key = f'filtered_checklist_{st.session_state.get("selected_country", "네덜란드")}'
            if filter_key in st.session_state:
                filter_info = st.session_state[filter_key]
                if filter_info.get('filtered_count', 0) > 0:
                    with st.expander(f"ℹ️ 준비물 필터링 정보 ({filter_info['filtered_count']}개 항목 제외됨)", expanded=False):
                        st.warning(f"⚠️ {filter_info['filtered_count']}개의 불필요한 항목이 자동으로 제외되었습니다.")
                        st.info(f"✅ {filter_info['valid_count']}개의 유효한 준비물이 저장되었습니다.")
                        if filter_info.get('filtered_items'):
                            st.markdown("**제외된 항목:**")
                            for item in filter_info['filtered_items']:
                                st.markdown(f"- `{item}`")
                        st.markdown("💡 다음 항목은 자동으로 제외됩니다: '-', '없음', 2자 이하, 대시만 있는 항목 등")
                # 정보 표시 후 세션 상태에서 제거 (다음 분석 시 새로운 정보로 교체)
                # del st.session_state[filter_key]  # 주석 처리: 사용자가 확인할 수 있도록 유지
            
            # 저장 섹션
            if parsed_data.get('event_name') and parsed_data.get('event_date'):
                st.markdown("### 📌 일정 저장")
                
                # 데이터베이스에서 아이 목록 가져오기
                children_list = get_children()
                child_options = ['없음'] + children_list + ['둘 다'] if len(children_list) > 1 else ['없음'] + children_list
                
                col_tag, col_save_btn = st.columns([2, 1])
                with col_tag:
                    # 아이 태그 선택 (데이터베이스에서 가져온 목록 사용)
                    child_tag = st.selectbox(
                        "👶 아이 선택",
                        options=child_options,
                        key="child_tag_select",
                        help="어떤 아이의 일정인지 선택해주세요"
                    )
                    # '둘 다'가 아닌 경우 그대로 사용
                    child_tag_clean = child_tag
                    parsed_data['child_tag'] = child_tag_clean
                
                with col_save_btn:
                    st.markdown("<br>", unsafe_allow_html=True)  # 버튼 정렬을 위한 공백
                    if st.button("📌 내 일정에 저장하기", use_container_width=True, type="primary"):
                        try:
                            event_id = save_event(parsed_data)
                            st.success(f"✅ '{parsed_data['event_name']}' 일정이 저장되었습니다!")
                            st.balloons()
                            st.info("💡 '나의 일정 (Dashboard)' 탭에서 저장된 일정을 확인할 수 있습니다.")
                        except Exception as e:
                            st.error(f"❌ 저장 중 오류가 발생했습니다: {str(e)}")
            else:
                st.warning("⚠️ 행사명과 날짜가 추출되지 않아 저장할 수 없습니다.")
                st.info("💡 분석 결과에서 행사명(📌)과 일시(📅) 정보를 확인할 수 없는 경우 저장이 불가능합니다.")
            
            st.markdown("---")
            
            # 복사하기 및 다운로드 버튼
            st.markdown("### 📋 결과 관리")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("📋 결과 복사하기", use_container_width=True):
                    st.code(result, language=None)
                    st.success("결과가 코드 블록으로 표시되었습니다. 복사해서 사용하세요!")
            
            with col2:
                # 결과 다운로드 버튼
                st.download_button(
                    label="💾 결과 다운로드",
                    data=result,
                    file_name=f"school_alert_summary_{country}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    with tab2:
        try:
            render_dashboard()
        except Exception as e:
            st.error(f"❌ 대시보드 로드 중 오류가 발생했습니다: {str(e)}")
            st.info("💡 문제가 계속되면 페이지를 새로고침하고 다시 시도해주세요.")

if __name__ == "__main__":
    main()
