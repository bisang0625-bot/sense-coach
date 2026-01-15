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
    """페이월(결제 안내) 팝업/화면 - 모바일 최적화 버전"""
    # 모바일 대응을 위한 공통 CSS 주입
    st.markdown("""
        <style>
            /* 프리미엄 화면일 때 사이드바 강제 숨김 (모바일 대응) */
            [data-testid="stSidebar"] {
                display: none !important;
            }
            [data-testid="stSidebarCollapsedControl"] {
                display: none !important;
            }
            
            /* 메인 영역 패딩 최소화 */
            .main .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                padding-top: 2rem !important;
                max-width: 100% !important;
            }
            
            @media (max-width: 768px) {
                .paywall-card {
                    margin-bottom: 1rem !important;
                }
            }
            .paywall-container {
                text-align: center;
                padding: 1rem 0;
            }
            .paywall-card {
                padding: 1.5rem;
                border-radius: 15px;
                height: 100%;
                display: flex;
                flex-direction: column;
            }
        </style>
    """, unsafe_allow_html=True)

    # 헤더 섹션
    st.markdown("""
        <div class="paywall-container">
            <h1 style="color: #6c5ce7; margin-bottom: 0.2rem; font-size: 1.8rem;">💎 눈치코치 프리미엄</h1>
            <p style="font-size: 1rem; color: #636e72;">더 똑똑하고 자유로운 알림장 분석을 시작하세요</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 혜택 카드 - 모바일에서는 세로로 자동 스택됨 (gap 조절)
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        st.markdown(f"""
            <div class="paywall-card" style="
                border: 1px solid #dfe6e9;
                background-color: #f9f9f9;
            ">
                <h3 style="color: #2d3436; margin-top: 0;">{PLANS['FREE']['name']}</h3>
                <p style="color: #636e72; font-size: 0.9rem;">{PLANS['FREE']['description']}</p>
                <ul style="color: #2d3436; padding-left: 1.2rem; font-size: 0.85rem; margin-bottom: 1rem;">
                    {"".join([f"<li>{feat}</li>" for feat in PLANS['FREE']['features']])}
                </ul>
            </div>
        """, unsafe_allow_html=True)
        st.button("현재 이용 중", disabled=True, use_container_width=True, key="current_plan_btn_mobile")
        
    with col2:
        st.markdown(f"""
            <div class="paywall-card" style="
                border: 2px solid #6c5ce7;
                background-color: #ffffff;
                box-shadow: 0 10px 20px rgba(108, 92, 231, 0.1);
            ">
                <h3 style="color: #6c5ce7; margin-top: 0;">{PLANS['PREMIUM']['name']} ✨</h3>
                <p style="color: #636e72; font-size: 0.9rem;">{PLANS['PREMIUM']['description']}</p>
                <ul style="color: #2d3436; list-style-type: none; padding-left: 0; font-size: 0.85rem; margin-bottom: 1rem;">
                    {"".join([f"<li>✅ {feat}</li>" for feat in PLANS['PREMIUM']['features']])}
                </ul>
                <h2 style="color: #2d3436; margin-top: auto; font-size: 1.5rem;">${PLANS['PREMIUM']['price']} <small style="font-size: 0.8rem; color: #636e72;">/ 월</small></h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top: 0.8rem;'></div>", unsafe_allow_html=True)
        if st.button("지금 업그레이드하기", type="primary", use_container_width=True, key="upgrade_now_btn_mobile"):
            st.info("💡 결제 시스템 연결 준비 중입니다. (Stripe/Play Store 연동 예정)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    # 닫기 버튼을 좀 더 명확하게 배치
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button("✖️ 닫기", use_container_width=True, key="close_paywall_btn_mobile"):
            st.session_state.show_paywall = False
            st.rerun()
