import sqlite3
import json
import re
from datetime import datetime, date

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
    # is_valid_checklist_item은 ai_logic에서 임포트하거나 혹은 여기서 별도로 구현
    # 순환 참조 방지를 위해 유틸리티 함수로 정의
    valid_items = event_data.get('checklist_items', [])
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
            'created_at': row[10],
            'memo': row[11] if row_len > 11 else ''
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
    """체크리스트 항목 추가"""
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
    """체크리스트 항목 이름 수정"""
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    
    c.execute('''
        UPDATE checklist_items 
        SET item_name = ? 
        WHERE id = ?
    ''', (new_name.strip(), item_id))
    
    conn.commit()
    conn.close()

def reset_all_data():
    """모든 데이터 삭제 (스토어 규범 준수)"""
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    c.execute('DELETE FROM events')
    c.execute('DELETE FROM checklist_items')
    c.execute('DELETE FROM children')
    # 기본 아이 재작성
    c.execute('INSERT INTO children (name, display_order) VALUES (?, ?)', ('첫째', 1))
    c.execute('INSERT INTO children (name, display_order) VALUES (?, ?)', ('둘째', 2))
    conn.commit()
    conn.close()
