# Payment & Subscription Configuration

PLANS = {
    "FREE": {
        "name": "무료 회원",
        "description": "기본 분석 기능 제공",
        "max_analyses_per_month": 5,
        "max_children": 1,
        "price": 0,
        "features": [
            "월 5회 AI 분석",
            "자녀 1명 관리",
            "기본 대시보드"
        ]
    },
    "PREMIUM": {
        "name": "프리미엄 멤버십",
        "description": "무제한 분석 및 모든 기능 잠금 해제",
        "max_analyses_per_month": 9999,
        "max_children": 99,
        "price": 4.99,
        "currency": "USD",
        "features": [
            "무제한 AI 분석",
            "자녀 관리 무제한",
            "고급 문화 맥락 통찰",
            "캘린더 내보내기 (준비 중)",
            "광고 및 제한 없음"
        ]
    }
}

# Stripe 또는 기타 결제 연동 설정 (추후 확장 가능)
STRIPE_PRICE_ID = "price_placeholder_123"
SUPPORT_EMAIL = "support@sensecoach.app"
