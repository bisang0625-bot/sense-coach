import sqlite3
import json
import re
import os
from datetime import datetime, date
import streamlit as st
from supabase import create_client, Client

# Supabase 설정 (Streamlit Secrets 또는 .env에서 가져옴)
# local .env: SUPABASE_URL, SUPABASE_KEY
# streamlit secrets: [supabase] url = "...", key = "..."
SUPABASE_URL = os.getenv("SUPABASE_URL") or st.secrets.get("supabase", {}).get("url")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or st.secrets.get("supabase", {}).get("key")

use_supabase = SUPABASE_URL and SUPABASE_KEY

if use_supabase:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def init_database():
    """데이터베이스 초기화 및 테이블 생성"""
    if use_supabase:
        # Supabase는 대시보드에서 직접 테이블을 생성하는 것이 권장되지만, 
        # 여기서는 연결 확인 정도로만 사용 (실제 테이블 생성 SQL은 가이드 제공)
        return
    
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
        pass
    
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
    
    # 기본 아이 정보 추가
    c.execute('SELECT COUNT(*) FROM children')
    if c.fetchone()[0] == 0:
        c.execute('INSERT INTO children (name, display_order) VALUES (?, ?)', ('첫째', 1))
        c.execute('INSERT INTO children (name, display_order) VALUES (?, ?)', ('둘째', 2))
    
    conn.commit()
    conn.close()

def get_children():
    """저장된 아이 목록 조회"""
    if use_supabase:
        try:
            response = supabase.table("children").select("name").order("display_order").execute()
            return [row["name"] for row in response.data] if response.data else []
        except Exception as e:
            st.error(f"Supabase Error (get_children): {e}")
            return []
            
    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    c.execute('SELECT name FROM children ORDER BY display_order ASC, id ASC')
    children = [row[0] for row in c.fetchall()]
    conn.close()
    return children if children else []

def add_child(name):
    """아이 추가"""
    if use_supabase:
        try:
            # max display_order 조회
            response = supabase.table("children").select("display_order").order("display_order", desc=True).limit(1).execute()
            max_order = response.data[0]["display_order"] if response.data else 0
            next_order = max_order + 1
            
            supabase.table("children").insert({"name": name, "display_order": next_order}).execute()
            return True
        except Exception as e:
            st.error(f"Supabase Error (add_child): {e}")
            return False

    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    try:
        c.execute('SELECT MAX(display_order) FROM children')
        max_order = c.fetchone()[0]
        next_order = (max_order or 0) + 1
        c.execute('INSERT INTO children (name, display_order) VALUES (?, ?)', (name, next_order))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def delete_child(name):
    """아이 삭제"""
    if use_supabase:
        supabase.table("children").delete().eq("name", name).execute()
        return

    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    c.execute('DELETE FROM children WHERE name = ?', (name,))
    conn.commit()
    conn.close()

def update_child_name(old_name, new_name):
    """아이 이름 수정"""
    if use_supabase:
        try:
            supabase.table("children").update({"name": new_name}).eq("name", old_name).execute()
            supabase.table("events").update({"child_tag": new_name}).eq("child_tag", old_name).execute()
            return True
        except Exception as e:
            return False

    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    try:
        c.execute('UPDATE children SET name = ? WHERE name = ?', (new_name, old_name))
        c.execute('UPDATE events SET child_tag = ? WHERE child_tag = ?', (new_name, old_name))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        conn.close()
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
            
            # 체크리스트 항목 저장
            valid_items = event_data.get('checklist_items', [])
            if valid_items:
                checklist_rows = [{"event_id": event_id, "item_name": item, "is_checked": 0} for item in valid_items]
                supabase.table("checklist_items").insert(checklist_rows).execute()
            
            return event_id
        except Exception as e:
            st.error(f"Supabase Error (save_event): {e}")
            raise e

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
    valid_items = event_data.get('checklist_items', [])
    for item in valid_items:
        c.execute('INSERT INTO checklist_items (event_id, item_name, is_checked) VALUES (?, ?, 0)', (event_id, item))
    conn.commit()
    conn.close()
    return event_id

def get_events(future_only=False):
    """이벤트 조회"""
    if use_supabase:
        try:
            query = supabase.table("events").select("*, checklist_items(id, item_name, is_checked)")
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
                    'checklist_items': json.loads(row['checklist_items']) if row['checklist_items'] else [],
                    'created_at': row['created_at'],
                    'memo': row.get('memo', ''),
                    'checklist_with_status': [
                        {'id': item['id'], 'name': item['item_name'], 'checked': bool(item['is_checked'])}
                        for item in row.get('checklist_items', [])
                    ]
                }
                events.append(event)
            return events
        except Exception as e:
            st.error(f"Supabase Error (get_events): {e}")
            return []

    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    if future_only:
        today = date.today().isoformat()
        c.execute('SELECT * FROM events WHERE event_date >= ? ORDER BY event_date ASC, event_time ASC', (today,))
    else:
        c.execute('SELECT * FROM events ORDER BY event_date ASC, event_time ASC')
    
    rows = c.fetchall()
    events = []
    for row in rows:
        row_len = len(row)
        event = {
            'id': row[0], 'event_name': row[1], 'event_date': row[2], 'event_time': row[3],
            'country': row[4], 'child_tag': row[5], 'translation': row[6], 'cultural_context': row[7],
            'tips': row[8], 'checklist_items': json.loads(row[9]) if row[9] else [],
            'created_at': row[10], 'memo': row[11] if row_len > 11 else ''
        }
        c.execute('SELECT id, item_name, is_checked FROM checklist_items WHERE event_id = ? ORDER BY id ASC', (event['id'],))
        event['checklist_with_status'] = [
            {'id': i_row[0], 'name': i_row[1], 'checked': bool(i_row[2])}
            for i_row in c.fetchall()
        ]
        events.append(event)
    conn.close()
    return events

def delete_event(event_id):
    """이벤트 삭제"""
    if use_supabase:
        supabase.table("events").delete().eq("id", event_id).execute()
        return

    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    c.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()

def update_checklist_item(item_id, is_checked):
    """체크리스트 항목 상태 업데이트"""
    if use_supabase:
        supabase.table("checklist_items").update({"is_checked": 1 if is_checked else 0}).eq("id", item_id).execute()
        return

    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    c.execute('UPDATE checklist_items SET is_checked = ? WHERE id = ?', (1 if is_checked else 0, item_id))
    conn.commit()
    conn.close()

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

    conn = sqlite3.connect('school_events.db')
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
    conn.close()

def add_checklist_item(event_id, item_name):
    """체크리스트 항목 추가"""
    if use_supabase:
        supabase.table("checklist_items").insert({"event_id": event_id, "item_name": item_name.strip(), "is_checked": 0}).execute()
        return

    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    c.execute('INSERT INTO checklist_items (event_id, item_name, is_checked) VALUES (?, ?, 0)', (event_id, item_name.strip()))
    conn.commit()
    conn.close()

def delete_checklist_item(item_id):
    """체크리스트 항목 삭제"""
    if use_supabase:
        supabase.table("checklist_items").delete().eq("id", item_id).execute()
        return

    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    c.execute('DELETE FROM checklist_items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

def update_checklist_item_name(item_id, new_name):
    """체크리스트 항목 이름 수정"""
    if use_supabase:
        supabase.table("checklist_items").update({"item_name": new_name.strip()}).eq("id", item_id).execute()
        return

    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    c.execute('UPDATE checklist_items SET item_name = ? WHERE id = ?', (new_name.strip(), item_id))
    conn.commit()
    conn.close()

def reset_all_data():
    """모든 데이터 삭제"""
    if use_supabase:
        # Supabase API는 대량 삭제에 제약이 있을 수 있으므로 주의 (일반적으로 빈 테이블로 초기화)
        supabase.table("events").delete().neq("id", 0).execute()
        supabase.table("children").delete().neq("id", 0).execute()
        # 기본 아이 재작성
        supabase.table("children").insert([{"name": '첫째', "display_order": 1}, {"name": '둘째', "display_order": 2}]).execute()
        return

    conn = sqlite3.connect('school_events.db')
    c = conn.cursor()
    c.execute('DELETE FROM events')
    c.execute('DELETE FROM checklist_items')
    c.execute('DELETE FROM children')
    c.execute('INSERT INTO children (name, display_order) VALUES (?, ?)', ('첫째', 1))
    c.execute('INSERT INTO children (name, display_order) VALUES (?, ?)', ('둘째', 2))
    conn.commit()
    conn.close()
