"""
Database Utilities (Streamlit-Independent Version)
공유 모듈 - FastAPI 및 기타 프레임워크에서 사용 가능
"""
import sqlite3
import json
import os
from datetime import datetime, date
from functools import lru_cache

# Supabase는 선택적 의존성 (설치되지 않아도 SQLite로 작동)
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

# Supabase 설정 (환경 변수에서 가져옴)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = None

use_supabase = SUPABASE_AVAILABLE and SUPABASE_URL and SUPABASE_KEY

if use_supabase:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 데이터베이스 연결 (싱글톤 패턴)
_db_connection = None

def get_db_connection():
    """데이터베이스 연결 반환 (싱글톤)"""
    global _db_connection
    if use_supabase:
        return None
    if _db_connection is None:
        _db_connection = sqlite3.connect('school_events.db', check_same_thread=False)
    return _db_connection

def init_database():
    """데이터베이스 초기화 및 테이블 생성"""
    if use_supabase:
        return
    
    conn = sqlite3.connect('school_events.db', check_same_thread=False)
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
    
    try:
        c.execute('ALTER TABLE events ADD COLUMN memo TEXT')
    except sqlite3.OperationalError:
        pass
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS checklist_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            is_checked INTEGER DEFAULT 0,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS children (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            display_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            subscription_tier TEXT DEFAULT 'FREE',
            expiry_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS usage_tracking (
            user_id TEXT,
            month_year TEXT,
            analysis_count INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, month_year)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_children():
    """저장된 아이 목록 조회"""
    if use_supabase:
        try:
            response = supabase.table("children").select("name").order("display_order").execute()
            return [row["name"] for row in response.data] if response.data else []
        except Exception as e:
            print(f"Supabase Error (get_children): {e}")
            return []
            
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT name FROM children ORDER BY display_order ASC, id ASC')
    return [row[0] for row in c.fetchall()]

def add_child(name):
    """아이 추가"""
    if use_supabase:
        try:
            response = supabase.table("children").select("display_order").order("display_order", desc=True).limit(1).execute()
            max_order = response.data[0]["display_order"] if response.data else 0
            supabase.table("children").insert({"name": name, "display_order": max_order + 1}).execute()
            return True
        except Exception as e:
            print(f"Supabase Error (add_child): {e}")
            return False

    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('SELECT MAX(display_order) FROM children')
        max_order = c.fetchone()[0] or 0
        c.execute('INSERT INTO children (name, display_order) VALUES (?, ?)', (name, max_order + 1))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False

def delete_child(name):
    """아이 삭제"""
    if use_supabase:
        supabase.table("children").delete().eq("name", name).execute()
        return

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM children WHERE name = ?', (name,))
    conn.commit()

def update_child_name(old_name, new_name):
    """아이 이름 수정"""
    if use_supabase:
        try:
            supabase.table("children").update({"name": new_name}).eq("name", old_name).execute()
            supabase.table("events").update({"child_tag": new_name}).eq("child_tag", old_name).execute()
            return True
        except:
            return False

    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('UPDATE children SET name = ? WHERE name = ?', (new_name, old_name))
        c.execute('UPDATE events SET child_tag = ? WHERE child_tag = ?', (new_name, old_name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False

def save_event(event_data):
    """이벤트 저장"""
    if use_supabase:
        try:
            new_event = {
                "event_name": event_data['event_name'],
                "event_date": event_data['event_date'],
                "event_time": event_data.get('event_time', ''),
                "country": event_data.get('country', ''),
                "child_tag": event_data.get('child_tag', '없음'),
                "translation": event_data.get('translation', ''),
                "cultural_context": event_data.get('cultural_context', ''),
                "tips": event_data.get('tips', ''),
                "checklist_items": json.dumps(event_data.get('checklist_items', []), ensure_ascii=False),
                "memo": event_data.get('memo', '')
            }
            response = supabase.table("events").insert(new_event).execute()
            event_id = response.data[0]["id"]
            
            valid_items = event_data.get('checklist_items', [])
            if valid_items:
                checklist_rows = [{"event_id": event_id, "item_name": item, "is_checked": 0} for item in valid_items]
                supabase.table("checklist_items").insert(checklist_rows).execute()
            
            return event_id
        except Exception as e:
            raise e

    conn = get_db_connection()
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
    for item in event_data.get('checklist_items', []):
        c.execute('INSERT INTO checklist_items (event_id, item_name, is_checked) VALUES (?, ?, 0)', (event_id, item))
    conn.commit()
    return event_id

def safe_json_loads(data):
    """문자열이면 JSON 파싱, 이미 객체면 그대로 반환"""
    if data is None:
        return []
    if isinstance(data, (list, dict)):
        return data
    try:
        return json.loads(data) if isinstance(data, str) else []
    except:
        return []

def get_events(future_only=False):
    """이벤트 조회"""
    if use_supabase:
        try:
            query = supabase.table("events").select("*, checklist_rel:checklist_items(id, item_name, is_checked)")
            if future_only:
                query = query.gte("event_date", date.today().isoformat())
            
            response = query.order("event_date").order("event_time").execute()
            events = []
            for row in response.data:
                event = {
                    'id': row['id'],
                    'event_name': row['event_name'],
                    'event_date': row['event_date'],
                    'event_time': row['event_time'],
                    'country': row['country'],
                    'child_tag': row['child_tag'],
                    'translation': row['translation'],
                    'cultural_context': row['cultural_context'],
                    'tips': row['tips'],
                    'checklist_items': safe_json_loads(row['checklist_items']),
                    'created_at': row['created_at'],
                    'memo': row.get('memo', ''),
                    'checklist_with_status': [
                        {'id': item['id'], 'name': item['item_name'], 'checked': bool(item['is_checked'])}
                        for item in row.get('checklist_rel', [])
                    ]
                }
                events.append(event)
            return events
        except Exception as e:
            print(f"Supabase Error (get_events): {e}")
            return []

    conn = get_db_connection()
    c = conn.cursor()
    if future_only:
        c.execute('SELECT * FROM events WHERE event_date >= ? ORDER BY event_date ASC, event_time ASC', (date.today().isoformat(),))
    else:
        c.execute('SELECT * FROM events ORDER BY event_date ASC, event_time ASC')
    
    events = []
    for row in c.fetchall():
        event = {
            'id': row[0], 'event_name': row[1], 'event_date': row[2], 'event_time': row[3],
            'country': row[4], 'child_tag': row[5], 'translation': row[6], 'cultural_context': row[7],
            'tips': row[8], 'checklist_items': json.loads(row[9]) if row[9] else [],
            'created_at': row[10], 'memo': row[11] if len(row) > 11 else ''
        }
        c.execute('SELECT id, item_name, is_checked FROM checklist_items WHERE event_id = ? ORDER BY id ASC', (event['id'],))
        event['checklist_with_status'] = [
            {'id': i_row[0], 'name': i_row[1], 'checked': bool(i_row[2])}
            for i_row in c.fetchall()
        ]
        events.append(event)
    return events

def delete_event(event_id):
    """이벤트 삭제"""
    if use_supabase:
        supabase.table("events").delete().eq("id", event_id).execute()
        return

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()

def update_checklist_item(item_id, is_checked):
    """체크리스트 항목 상태 업데이트"""
    if use_supabase:
        supabase.table("checklist_items").update({"is_checked": 1 if is_checked else 0}).eq("id", item_id).execute()
        return

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE checklist_items SET is_checked = ? WHERE id = ?', (1 if is_checked else 0, item_id))
    conn.commit()

def update_event(event_id, event_data):
    """이벤트 정보 업데이트"""
    if use_supabase:
        supabase.table("events").update({
            "event_name": event_data.get('event_name', ''),
            "event_date": event_data.get('event_date', ''),
            "event_time": event_data.get('event_time', ''),
            "country": event_data.get('country', ''),
            "child_tag": event_data.get('child_tag', '없음'),
            "memo": event_data.get('memo', '')
        }).eq("id", event_id).execute()
        return

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        UPDATE events 
        SET event_name = ?, event_date = ?, event_time = ?, country = ?, child_tag = ?, memo = ?
        WHERE id = ?
    ''', (
        event_data.get('event_name', ''), event_data.get('event_date', ''),
        event_data.get('event_time', ''), event_data.get('country', ''),
        event_data.get('child_tag', '없음'), event_data.get('memo', ''),
        event_id
    ))
    conn.commit()

def add_checklist_item(event_id, item_name):
    """체크리스트 항목 추가"""
    if use_supabase:
        supabase.table("checklist_items").insert({"event_id": event_id, "item_name": item_name.strip(), "is_checked": 0}).execute()
        return

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO checklist_items (event_id, item_name, is_checked) VALUES (?, ?, 0)', (event_id, item_name.strip()))
    conn.commit()

def delete_checklist_item(item_id):
    """체크리스트 항목 삭제"""
    if use_supabase:
        supabase.table("checklist_items").delete().eq("id", item_id).execute()
        return

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM checklist_items WHERE id = ?', (item_id,))
    conn.commit()

def update_checklist_item_name(item_id, new_name):
    """체크리스트 항목 이름 수정"""
    if use_supabase:
        supabase.table("checklist_items").update({"item_name": new_name.strip()}).eq("id", item_id).execute()
        return

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE checklist_items SET item_name = ? WHERE id = ?', (new_name.strip(), item_id))
    conn.commit()

def reset_all_data():
    """모든 데이터 삭제"""
    if use_supabase:
        supabase.table("events").delete().neq("id", 0).execute()
        supabase.table("children").delete().neq("id", 0).execute()
        return

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM events')
    c.execute('DELETE FROM checklist_items')
    c.execute('DELETE FROM children')
    conn.commit()

def get_user_tier(user_id):
    """사용자 구독 등급 조회"""
    if use_supabase:
        try:
            response = supabase.table("users").select("subscription_tier").eq("user_id", user_id).execute()
            if response.data:
                return response.data[0]["subscription_tier"]
            supabase.table("users").insert({"user_id": user_id, "subscription_tier": "FREE"}).execute()
            return "FREE"
        except:
            return "FREE"

    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    c.execute('SELECT subscription_tier FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    if row:
        tier = row[0]
    else:
        c.execute('INSERT INTO users (user_id, subscription_tier) VALUES (?, ?)', (user_id, 'FREE'))
        conn.commit()
        tier = 'FREE'
    conn.close()
    return tier

def get_usage(user_id):
    """현재 달의 사용량 조회"""
    month_year = datetime.now().strftime('%Y-%m')
    if use_supabase:
        try:
            response = supabase.table("usage_tracking").select("analysis_count").eq("user_id", user_id).eq("month_year", month_year).execute()
            return response.data[0]["analysis_count"] if response.data else 0
        except:
            return 0

    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    c.execute('SELECT analysis_count FROM usage_tracking WHERE user_id = ? AND month_year = ?', (user_id, month_year))
    row = c.fetchone()
    count = row[0] if row else 0
    conn.close()
    return count

def increment_usage(user_id):
    """사용량 1 증가"""
    month_year = datetime.now().strftime('%Y-%m')
    if use_supabase:
        try:
            current = get_usage(user_id)
            supabase.table("usage_tracking").upsert({
                "user_id": user_id, 
                "month_year": month_year, 
                "analysis_count": current + 1
            }).execute()
            return True
        except:
            return False

    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO usage_tracking (user_id, month_year, analysis_count) VALUES (?, ?, ?)', (user_id, month_year, 0))
    c.execute('UPDATE usage_tracking SET analysis_count = analysis_count + 1 WHERE user_id = ? AND month_year = ?', (user_id, month_year))
    conn.commit()
    conn.close()
    return True

def update_user_tier(user_id, new_tier):
    """사용자 구독 등급 업데이트"""
    if use_supabase:
        try:
            supabase.table("users").upsert({"user_id": user_id, "subscription_tier": new_tier}).execute()
            return True
        except:
            return False

    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    c.execute('UPDATE users SET subscription_tier = ? WHERE user_id = ?', (new_tier, user_id))
    conn.commit()
    conn.close()
    return True
