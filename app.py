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

# 모듈화된 유틸리티 임포트
from database_utils import (
    init_database, get_children, add_child, delete_child, 
    update_child_name, save_event, get_events, delete_event, 
    update_checklist_item, update_event, add_checklist_item, 
    delete_checklist_item, update_checklist_item_name, reset_all_data
)
from ai_logic import analyze_with_gemini, parse_analysis_result, is_valid_checklist_item
from ui_styles import STYLE_CSS, COLORS
from subscription_manager import (
    get_or_create_user_id, check_can_analyze, process_analysis_usage, 
    render_membership_sidebar, render_paywall
)

# 환경 변수 로드
load_dotenv()

# 세션 상태 초기화 (페이지 설정 전)
if 'show_paywall' not in st.session_state:
    st.session_state.show_paywall = False

# 페이지 설정
st.set_page_config(
    page_title="눈치코치 알림장: Sense Coach",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="collapsed" if st.session_state.show_paywall else "expanded"
)

# 스타일 적용
st.markdown(STYLE_CSS, unsafe_allow_html=True)

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
                # 수정 모드가 활성화되어 있는지 확인 (이름 기반)
                is_editing = st.session_state.get(f'editing_child_{child}', False)
                
                if not is_editing:
                    # 일반 표시 모드
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
                        # 수정 버튼
                        if st.button("✏️", key=f"edit_child_{child}", help="수정", use_container_width=True, type="secondary"):
                            st.session_state[f'editing_child_{child}'] = True
                            st.rerun()
                    
                    with col_delete:
                        # 삭제 버튼
                        if st.button("🗑️", key=f"delete_child_{child}", help="삭제", use_container_width=True, type="secondary"):
                            delete_child(child)
                            st.success(f"✅ '{child}'가 삭제되었습니다.")
                            st.rerun()
                else:
                    # 수정 모드
                    st.markdown("""
                        <div style="
                            padding: 0.8rem;
                            background: #fff3cd;
                            border-radius: 8px;
                            margin-bottom: 0.5rem;
                            border-left: 3px solid #ffc107;
                        ">
                            <strong>✏️ 수정 모드</strong>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    new_name = st.text_input(
                        "새 이름 입력",
                        value=child,
                        key=f"edit_input_{child}",
                        label_visibility="visible"
                    )
                    
                    col_save_edit, col_cancel_edit = st.columns([1, 1])
                    with col_save_edit:
                        if st.button("💾 저장", key=f"save_edit_{child}", use_container_width=True, type="primary"):
                            if new_name and new_name.strip() and new_name.strip() != child:
                                if update_child_name(child, new_name.strip()):
                                    st.success(f"✅ '{child}'이(가) '{new_name.strip()}'으로 변경되었습니다.")
                                    # 이전 상태 삭제 및 새 상태로 업데이트
                                    del st.session_state[f'editing_child_{child}']
                                    st.rerun()
                                else:
                                    st.error("❌ 같은 이름의 아이가 이미 존재합니다.")
                            elif new_name and new_name.strip() == child:
                                del st.session_state[f'editing_child_{child}']
                                st.rerun()
                            else:
                                st.warning("⚠️ 아이 이름을 입력해주세요.")
                    
                    with col_cancel_edit:
                        if st.button("❌ 취소", key=f"cancel_edit_{child}", use_container_width=True):
                            del st.session_state[f'editing_child_{child}']
                            st.rerun()
                
                # 간격 조정
                st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
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
        
        # 멤버십 정보 표시
        render_membership_sidebar()
        
        # 데이터 관리 섹션 (스토어 규정 준수)
        st.markdown("<div style='margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #ffcccc;'></div>", unsafe_allow_html=True)
        st.markdown("### ⚠️ 데이터 관리")
        with st.expander("데이터 초기화", expanded=False):
            st.warning("이 작업을 수행하면 모든 일정과 아이 정보가 영구적으로 삭제됩니다.")
            if st.button("🚨 모든 데이터 초기화", use_container_width=True):
                reset_all_data()
                st.success("✅ 모든 데이터가 초기화되었습니다.")
                st.rerun()
        
        # 하단 법적 고지 및 지원 (사이드바 최하단)
        st.markdown("<div style='margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #e0e0e0; font-size: 0.8rem; color: #888;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div style="font-size: 0.8rem; color: #888; text-align: center;">
                <p>© 2026 눈치코치 알림장 (Sense Coach)</p>
                <a href="https://github.com/bisang0625-bot/sense-coach/blob/main/privacy-policy.md" target="_blank" style="color: #888; text-decoration: none;">개인정보 처리방침</a> | 
                <a href="#" style="color: #888; text-decoration: none;">이용약관</a><br>
                문의: <a href="mailto:support@sensecoach.app" style="color: #888; text-decoration: none;">support@sensecoach.app</a>
            </div>
        """, unsafe_allow_html=True)
    
    # 메인 영역 - 커스텀 제목 디자인
    st.markdown("""
        <div class="app-title">
            <span style="font-size: 2rem;">🎒</span>
            <div style="display: flex; flex-direction: column; align-items: center; gap: 0.2rem;">
                <span class="app-title-main" style="white-space: nowrap;">눈치코치 알림장</span>
                <span class="app-title-main" style="font-size: 1.2rem; font-weight: 600; opacity: 0.9;">Sense Coach</span>
            </div>
        </div>
        <div class="app-title-subtitle">
            🌍 현지 학교 알림장의 행간을 읽어주는<br>AI 문화 비서
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    # --- 메인 본문 ---
    # 페이월(프리미엄 혜택)이 활성화된 경우 최상단에서 렌더링하고 다른 콘텐츠 중단
    if st.session_state.get('show_paywall', False):
        render_paywall()
        st.stop()
        
    # 탭 생성
    tab1, tab2 = st.tabs(["🔍 분석하기 (Analysis)", "📅 나의 일정 (Dashboard)"])
    
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
            # 사용량 제한 확인
            can_analyze, current, max_val, tier = check_can_analyze()
            if not can_analyze:
                st.error(f"⚠️ 이번 달 분석 횟수({max_val}회)를 모두 사용하셨습니다.")
                st.info("💎 무제한 분석을 위해 프리미엄으로 업그레이드하세요!")
                if st.button("🚀 프리미엄 혜택 보기", key="paywall_btn_main"):
                    st.session_state.show_paywall = True
                    st.rerun()
                st.stop()

            # 입력 검증
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
                    
                    # 분석 성공 시 사용량 기록
                    process_analysis_usage()
                    
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
            
            # 저장 섹션 (다중 일정 지원)
            st.markdown("### 📌 일정 저장 및 관리")
            
            # 세션 상태에서 파싱된 데이터 가져오기 및 리스트 변환 확인
            parsed_data_raw = st.session_state.get('last_analysis_parsed', [])
            if isinstance(parsed_data_raw, dict):
                parsed_events = [parsed_data_raw]
            else:
                parsed_events = parsed_data_raw
            
            # 1. 일정 추가 버튼
            if st.button("➕ 일정 직접 추가하기", use_container_width=True):
                parsed_events.append({
                    'event_name': '', 
                    'event_date': '', 
                    'event_time': '',
                    'child_tag': parsed_events[0].get('child_tag') if parsed_events else None,
                    'country': country
                })
                st.session_state['last_analysis_parsed'] = parsed_events
                st.rerun()
            
            st.markdown("---")

            # 2. 각 일정별 카드 렌더링
            for i, event_data in enumerate(parsed_events):
                # 카드로 시각적 구분
                st.markdown(f"""
                <div style="
                    padding: 1rem;
                    border: 1px solid #e0e0e0;
                    border-radius: 10px;
                    margin-bottom: 1rem;
                    background-color: #fcfcfc;
                ">
                    <strong>📌 일정 {i+1}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # 일정 삭제 버튼 (우측 상단 배치를 위해 컬럼 사용)
                col_header, col_delete_btn = st.columns([5, 1])
                with col_delete_btn:
                    if st.button("🗑️", key=f"del_btn_{i}", help="이 일정 삭제"):
                        parsed_events.pop(i)
                        st.session_state['last_analysis_parsed'] = parsed_events
                        st.rerun()
                
                # 입력 필드 구성
                col_input_1, col_input_2, col_input_3 = st.columns([2, 1, 1])
                
                with col_input_1:
                    manual_event_name = st.text_input(
                        "행사명 (필수)", 
                        value=event_data.get('event_name', ''), 
                        key=f"event_name_{i}",
                        placeholder="예: 학부모 상담일"
                    )
                
                with col_input_2:
                    default_date_value = date.today()
                    date_str = event_data.get('event_date', '')
                    if date_str:
                        try:
                            default_date_value = datetime.strptime(date_str, "%Y-%m-%d").date()
                        except ValueError:
                            pass
                    
                    manual_event_date_obj = st.date_input(
                        "날짜 (필수)", 
                        value=default_date_value, 
                        key=f"event_date_{i}"
                    )
                    manual_event_date = manual_event_date_obj.strftime("%Y-%m-%d") if manual_event_date_obj else ""
                
                with col_input_3:
                    manual_event_time = st.text_input(
                        "시간 (선택)", 
                        value=event_data.get('event_time', ''), 
                        key=f"event_time_{i}",
                        placeholder="예: 14:00"
                    )
                
                # 아이 선택 및 저장 버튼
                # 데이터베이스에서 아이 목록 가져오기
                children_list = get_children()
                child_options = ['없음'] + children_list + ['둘 다'] if len(children_list) > 1 else ['없음'] + children_list
                
                col_child, col_save = st.columns([2, 1])
                with col_child:
                    child_tag = st.selectbox(
                        "👶 아이 선택",
                        options=child_options,
                        key=f"child_select_{i}",
                        index=0 # 기본값
                    )
                
                with col_save:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("💾 저장하기", key=f"save_btn_{i}", use_container_width=True, type="primary"):
                        if manual_event_name and manual_event_date:
                            try:
                                # 준비물 리스트 처리
                                # text_area의 key를 통해 현재 값을 가져옴
                                current_checklist_str = st.session_state.get(f"checklist_{i}", "")
                                # 줄바꿈으로 분리하고 빈 줄 제거
                                updated_checklist = [item.strip() for item in current_checklist_str.split('\n') if item.strip()]
                                
                                # 데이터 업데이트
                                event_data['event_name'] = manual_event_name
                                event_data['event_date'] = manual_event_date
                                event_data['event_time'] = manual_event_time
                                event_data['child_tag'] = child_tag
                                event_data['checklist_items'] = updated_checklist
                                
                                save_event(event_data)
                                st.toast(f"✅ '{manual_event_name}' 저장 완료!", icon="🎉")
                                # 저장 완료 표시를 위해 아이콘 추가 등 UI 업데이트 가능
                            except Exception as e:
                                st.error(f"❌ 저장 실패: {str(e)}")
                        else:
                            st.warning("⚠️ 행사명과 날짜를 입력해주세요.")
                
                # 추가 정보 (Checklist, Translation 등) 표시 - Expander로 숨김
                with st.expander("📝 상세 정보 및 준비물 보기/수정", expanded=False):
                    # 준비물 수정 기능 추가
                    current_items = event_data.get('checklist_items', [])
                    items_str = "\n".join(current_items) if current_items else ""
                    
                    new_items_str = st.text_area(
                        "✅ 준비물 (한 줄에 하나씩 입력)",
                        value=items_str,
                        key=f"checklist_{i}",
                        help="준비물을 수정하거나 추가할 수 있습니다. 각 항목을 줄바꿈으로 구분하세요."
                    )
                    
                    # 실시간 업데이트를 위해 session state에 반영하지는 않고, 저장 버튼 클릭 시 처리하도록 함
                    # 다만 UI 상에서 바로 반영되어 보이게 하려면 저장 로직에서 이 값을 참조해야 함
                    
                    if event_data.get('translation'):
                        st.markdown("**🌐 번역:**")
                        st.write(event_data['translation'])
                        
                    if event_data.get('tips'):
                        st.markdown("**💡 팁:**")
                        st.info(event_data['tips'])

            if not parsed_events:
                st.info("💡 표시할 일정이 없습니다. '일정 직접 추가하기' 버튼을 눌러보세요.")
            
            st.markdown("---")
            
    
    with tab2:
        try:
            render_dashboard()
        except Exception as e:
            st.error(f"❌ 대시보드 로드 중 오류가 발생했습니다: {str(e)}")
            st.info("💡 문제가 계속되면 페이지를 새로고침하고 다시 시도해주세요.")

if __name__ == "__main__":
    main()
