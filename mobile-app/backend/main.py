"""
FastAPI Backend for Sense Coach Mobile App
"""
import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from PIL import Image
import io
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

from database_utils import (
    init_database, get_children, add_child, delete_child,
    update_child_name, save_event, get_events, delete_event,
    update_checklist_item, update_event, add_checklist_item,
    delete_checklist_item, update_checklist_item_name, reset_all_data,
    get_user_tier, get_usage, increment_usage, update_user_tier
)
from ai_logic import analyze_with_gemini, parse_analysis_result
from payment_config import PLANS

# FastAPI 앱 생성
app = FastAPI(
    title="Sense Coach API",
    description="눈치코치 알림장 분석 API",
    version="1.0.0"
)

# CORS 설정 (React Native에서 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 앱 시작 시 데이터베이스 초기화
@app.on_event("startup")
async def startup_event():
    init_database()

# ==================== Pydantic 모델 ====================

class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    country: str = "네덜란드"
    user_id: str

class ChildCreate(BaseModel):
    name: str

class ChildUpdate(BaseModel):
    old_name: str
    new_name: str

class EventCreate(BaseModel):
    event_name: str
    event_date: str
    event_time: Optional[str] = ""
    country: Optional[str] = ""
    child_tag: Optional[str] = "없음"
    translation: Optional[str] = ""
    cultural_context: Optional[str] = ""
    tips: Optional[str] = ""
    checklist_items: Optional[List[str]] = []
    memo: Optional[str] = ""

class EventUpdate(BaseModel):
    event_name: Optional[str] = None
    event_date: Optional[str] = None
    event_time: Optional[str] = None
    country: Optional[str] = None
    child_tag: Optional[str] = None
    memo: Optional[str] = None

class ChecklistItemUpdate(BaseModel):
    is_checked: bool

# ==================== API 엔드포인트 ====================

@app.get("/")
async def root():
    return {"message": "Sense Coach API v1.0.0", "status": "OK"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# -------------------- 분석 API --------------------

@app.post("/api/analyze")
async def analyze_notice(request: AnalyzeRequest):
    """학교 알림장 텍스트 분석"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API 키가 설정되지 않았습니다.")
    
    # 사용량 확인 (무제한으로 변경)
    tier = get_user_tier(request.user_id)
    usage = get_usage(request.user_id)
    # limit = PLANS.get(tier, {}).get("monthly_limit", 5)
    
    # if limit != -1 and usage >= limit:
    #     raise HTTPException(status_code=403, detail="월간 사용량을 초과했습니다.")
    
    # 분석 실행
    result = analyze_with_gemini(request.text, None, request.country, api_key)
    
    if result.startswith("❌"):
        raise HTTPException(status_code=500, detail=result)
    
    # 사용량 증가
    increment_usage(request.user_id)
    
    # 결과 파싱
    parsed_events = parse_analysis_result(result, request.country)
    
    return {
        "raw_result": result,
        "parsed_events": parsed_events,
        "usage": usage + 1,
        "limit": -1  # 무제한
    }

@app.post("/api/analyze/image")
async def analyze_image(
    file: UploadFile = File(...),
    country: str = Form("네덜란드"),
    user_id: str = Form(...)
):
    """이미지 분석"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API 키가 설정되지 않았습니다.")
    
    # 사용량 확인 (무제한으로 변경)
    tier = get_user_tier(user_id)
    usage = get_usage(user_id)
    # limit = PLANS.get(tier, {}).get("monthly_limit", 5)
    
    # if limit != -1 and usage >= limit:
    #     raise HTTPException(status_code=403, detail="월간 사용량을 초과했습니다.")
    
    # 이미지 읽기
    image_data = await file.read()
    image = io.BytesIO(image_data)
    
    # 분석 실행
    result = analyze_with_gemini(None, image, country, api_key)
    
    if result.startswith("❌"):
        raise HTTPException(status_code=500, detail=result)
    
    # 사용량 증가
    increment_usage(user_id)
    
    # 결과 파싱
    parsed_events = parse_analysis_result(result, country)
    
    return {
        "raw_result": result,
        "parsed_events": parsed_events,
        "usage": usage + 1,
        "limit": -1  # 무제한
    }

# -------------------- 아이 관리 API --------------------

@app.get("/api/children")
async def list_children():
    """아이 목록 조회"""
    return {"children": get_children()}

@app.post("/api/children")
async def create_child(child: ChildCreate):
    """아이 추가"""
    success = add_child(child.name)
    if not success:
        raise HTTPException(status_code=400, detail="같은 이름의 아이가 이미 존재합니다.")
    return {"message": f"'{child.name}'이(가) 추가되었습니다."}

@app.delete("/api/children/{name}")
async def remove_child(name: str):
    """아이 삭제"""
    delete_child(name)
    return {"message": f"'{name}'이(가) 삭제되었습니다."}

@app.put("/api/children")
async def rename_child(child: ChildUpdate):
    """아이 이름 수정"""
    success = update_child_name(child.old_name, child.new_name)
    if not success:
        raise HTTPException(status_code=400, detail="이름 변경에 실패했습니다.")
    return {"message": f"'{child.old_name}'이(가) '{child.new_name}'으로 변경되었습니다."}

# -------------------- 이벤트 API --------------------

@app.get("/api/events")
async def list_events(future_only: bool = False):
    """이벤트 목록 조회"""
    events = get_events(future_only=future_only)
    return {"events": events}

@app.post("/api/events")
async def create_event(event: EventCreate):
    """이벤트 저장"""
    event_id = save_event(event.dict())
    return {"message": "이벤트가 저장되었습니다.", "event_id": event_id}

@app.get("/api/events/{event_id}")
async def get_event(event_id: int):
    """특정 이벤트 조회"""
    events = get_events()
    event = next((e for e in events if e['id'] == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="이벤트를 찾을 수 없습니다.")
    return {"event": event}

@app.put("/api/events/{event_id}")
async def modify_event(event_id: int, event: EventUpdate):
    """이벤트 수정"""
    update_event(event_id, event.dict(exclude_none=True))
    return {"message": "이벤트가 수정되었습니다."}

@app.delete("/api/events/{event_id}")
async def remove_event(event_id: int):
    """이벤트 삭제"""
    delete_event(event_id)
    return {"message": "이벤트가 삭제되었습니다."}

# -------------------- 체크리스트 API --------------------

@app.put("/api/checklist/{item_id}")
async def update_checklist(item_id: int, item: ChecklistItemUpdate):
    """체크리스트 항목 상태 업데이트"""
    update_checklist_item(item_id, item.is_checked)
    return {"message": "체크리스트가 업데이트되었습니다."}

@app.post("/api/events/{event_id}/checklist")
async def add_checklist(event_id: int, item_name: str = Form(...)):
    """체크리스트 항목 추가"""
    add_checklist_item(event_id, item_name)
    return {"message": f"'{item_name}'이(가) 추가되었습니다."}

@app.delete("/api/checklist/{item_id}")
async def remove_checklist(item_id: int):
    """체크리스트 항목 삭제"""
    delete_checklist_item(item_id)
    return {"message": "체크리스트 항목이 삭제되었습니다."}

# -------------------- 사용자 API --------------------

@app.get("/api/user/{user_id}/membership")
async def get_membership(user_id: str):
    """멤버십 정보 조회"""
    tier = get_user_tier(user_id)
    usage = get_usage(user_id)
    plan = PLANS.get(tier, PLANS["FREE"])
    
    return {
        "user_id": user_id,
        "tier": tier,
        "usage": usage,
        "limit": plan["monthly_limit"],
        "plan_name": plan["name"]
    }

# -------------------- 데이터 관리 API --------------------

@app.delete("/api/data/reset")
async def reset_data():
    """모든 데이터 초기화 (주의!)"""
    reset_all_data()
    return {"message": "모든 데이터가 초기화되었습니다."}
