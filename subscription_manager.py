import streamlit as st
import uuid
from database_utils import get_user_tier, get_usage, increment_usage
from payment_config import PLANS

def get_or_create_user_id():
    """사용자 고유 ID 생성 또는 가져오기 (세션 및 로컬 저장소 활용)"""
    if 'user_id' not in st.session_state:
        # 1. 쿼리 파라미터 확인 (외부 링크 등)
        params = st.query_params
        if 'uid' in params:
            st.session_state.user_id = params['uid']
        else:
            # 2. 새로운 랜덤 ID 생성 (실제 앱에서는 기기 ID 등을 활용하거나 로그인을 유도)
            st.session_state.user_id = str(uuid.uuid4())
    
    return st.session_state.user_id

def check_can_analyze():
    """AI 분석 가능 여부 확인"""
    user_id = get_or_create_user_id()
    tier = get_user_tier(user_id)
    plan = PLANS.get(tier, PLANS["FREE"])
    
    current_usage = get_usage(user_id)
    max_usage = plan["max_analyses_per_month"]
    
    can_analyze = current_usage < max_usage
    return can_analyze, current_usage, max_usage, tier

def get_membership_info():
    """멤버십 정보 요약"""
    user_id = get_or_create_user_id()
    tier = get_user_tier(user_id)
    plan = PLANS.get(tier, PLANS["FREE"])
    current_usage = get_usage(user_id)
    
    return {
        "tier": tier,
        "tier_name": plan["name"],
        "usage": current_usage,
        "max_usage": plan["max_analyses_per_month"],
        "features": plan["features"]
    }

def process_analysis_usage():
    """분석 완료 시 사용량 기록"""
    user_id = get_or_create_user_id()
    increment_usage(user_id)

def render_membership_sidebar():
    """사이드바에 멤버십 정보 표시"""
    info = get_membership_info()
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### 💎 멤버십: {info['tier_name']}")
    
    if info['tier'] == 'FREE':
        usage_pct = info['usage'] / info['max_usage'] if info['max_usage'] > 0 else 1
        st.sidebar.progress(min(usage_pct, 1.0), text=f"사용량: {info['usage']}/{info['max_usage']}")
        if info['usage'] >= info['max_usage']:
            st.sidebar.warning("⚠️ 이번 달 분석 횟수를 모두 사용했습니다.")
            if st.sidebar.button("🚀 프리미엄으로 업그레이드", use_container_width=True, type="primary"):
                st.session_state.show_paywall = True
        else:
            if st.sidebar.button("✨ 프리미엄 혜택 보기", use_container_width=True):
                st.session_state.show_paywall = True
    else:
        st.sidebar.success("✅ 프리미엄 혜택을 이용 중입니다.")
        st.sidebar.write(f"📊 이번 달 분석 횟수: {info['usage']}회")

def render_paywall():
    """페이월(결제 안내) 팝업/화면"""
    st.markdown("---")
    st.markdown("## 💎 눈치코치 프리미엄 멤버십")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### {PLANS['FREE']['name']}")
        st.write(PLANS['FREE']['description'])
        for feat in PLANS['FREE']['features']:
            st.write(f"- {feat}")
        st.button("현재 이용 중", disabled=True, use_container_width=True)
        
    with col2:
        st.markdown(f"### {PLANS['PREMIUM']['name']}")
        st.write(PLANS['PREMIUM']['description'])
        for feat in PLANS['PREMIUM']['features']:
            st.write(f"✅ {feat}")
        
        st.markdown(f"## ${PLANS['PREMIUM']['price']} / 월")
        if st.button("지금 업그레이드하기", type="primary", use_container_width=True):
            st.info("💡 결제 시스템 연결 준비 중입니다. (Stripe/Play Store 연동 예정)")
            # 여기서 실제 결제 페이지로 리다이렉트하거나 단계를 진행
    
    if st.button("✖️ 닫기"):
        st.session_state.show_paywall = False
        st.rerun()
