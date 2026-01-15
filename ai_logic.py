import google.generativeai as genai
from PIL import Image
import re
from datetime import datetime

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
 
사용자가 제공한 학교 알림장을 분석하여, 포함된 **모든 일정**을 찾아서 분석해주세요.
알림장에 여러 개의 행사나 일정이 포함되어 있다면, 반드시 **각 일정별로 구분**하여 아래 형식을 반복해서 작성해주세요.
각 일정 사이에는 `---EVENT_SEPARATOR---` 라는 구분선을 반드시 넣어주세요.

형식:

🌐 **원문 번역 (한국어)**:
[해당 일정과 관련된 원문 부분만 한국어로 번역]

📌 **행사명**: [행사 이름]
📅 **일시**: [날짜와 시간] (YYYY-MM-DD HH:MM 형식 권장)
✅ **준비물 체크리스트**:
- [준비물 1]
- [준비물 2]
...

🌍 **Cultural Context (문화적 배경)**:
[해당 행사와 관련된 문화적 배경 약 2-3문장]

💡 **실용적인 팁**:
[해당 행사 준비를 위한 팁 약 2-3문장]

---EVENT_SEPARATOR---

(다음 일정이 있으면 위 형식을 반복, 없으면 종료)

**중요한 작성 지침:**
- 일정이 하나라도, 형식을 정확히 지켜주세요.
- 일정이 여러 개라면 `---EVENT_SEPARATOR---`로 명확히 구분해주세요.
- Cultural Context와 실용적인 팁은 핵심만 간결하게 작성해주세요.
"""

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
        
        # 사용할 모델 후보 리스트 (Flash 계열 우선 시도하여 비용/속도 최적화)
        # 2026년 기준 사용 가능한 모델 우선순위 조정
        model_candidates = [
            "gemini-2.0-flash",       # STABLE 2.0
            "gemini-2.0-flash-exp",   # EXPERIMENTAL 2.0
            "gemini-1.5-flash",       # STABLE 1.5
            "gemini-1.5-flash-8b",    # LITE 1.5
            "gemini-1.5-pro",         # PRO 1.5
            "gemini-pro",             # LEGACY
        ]
        
        if image_input:
            # 비전 모델이 필요한 경우
            candidate_models = model_candidates + ["gemini-pro-vision"]
        else:
            candidate_models = model_candidates
        
        # 프롬프트 생성
        has_image = image_input is not None
        prompt = get_prompt(country, text_input, has_image)
        
        last_error = ""
        for model_name in candidate_models:
            try:
                model = genai.GenerativeModel(model_name)
                
                # 실행
                if image_input:
                    img = Image.open(image_input)
                    response = model.generate_content([prompt, img])
                else:
                    response = model.generate_content(prompt)
                
                # 응답 처리
                if hasattr(response, 'text') and response.text:
                    return response.text
                
                # 텍스트 응답이 없는 경우 다음 모델 시도
                last_error = "응답 텍스트가 비어 있습니다."
                continue
                
            except Exception as e:
                last_error = str(e)
                # 404 등 모델 관련 에러인 경우 다음 모델 시도
                if "404" in last_error or "not found" in last_error.lower() or "not supported" in last_error.lower():
                    continue
                else:
                    # 기타 치명적인 에러는 즉시 중단
                    break
        
        return f"❌ 모든 모델에서 분석에 실패했습니다. (마지막 오류: {last_error})"
        
    except Exception as e:
        return f"❌ 알 수 없는 오류 발생: {str(e)}"

def is_valid_checklist_item(item):
    """준비물 항목 유효성 검증"""
    if not item or not isinstance(item, str): return False
    cleaned = item.strip()
    if not cleaned or len(cleaned) <= 2: return False
    if re.match(r'^[-—─–\s]+$', cleaned): return False
    invalid_patterns = [r'^없음', r'^없습니다', r'준비물\s*없', r'^[-•]\s*$', r'^\.+$']
    for p in invalid_patterns:
        if re.search(p, cleaned, re.IGNORECASE): return False
    meaningful = re.findall(r'[가-힣a-zA-Z0-9]+', cleaned)
    return len(''.join(meaningful)) >= 3

def parse_analysis_result(result, country):
    """분석 결과 파싱 (다중 이벤트 지원)"""
    # 구분자로 분리
    raw_events = result.split('---EVENT_SEPARATOR---')
    parsed_events = []
    
    for raw_event in raw_events:
        if not raw_event.strip():
            continue
            
        parsed_data = {
            'event_name': '', 'event_date': '', 'event_time': '',
            'country': country, 'checklist_items': [],
            'translation': '', 'cultural_context': '', 'tips': '', 'memo': ''
        }
        
        # 정규표현식으로 각 섹션 추출
        if "📌" in raw_event:
            m = re.search(r'📌\s*\*\*행사명\*\*:?\s*([^\n📅✅🌍💡]+)', raw_event)
            if m: parsed_data['event_name'] = m.group(1).strip()
        
        if "📅" in raw_event:
            m = re.search(r'📅\s*\*\*일시\*\*:?\s*([^\n📌✅🌍💡]+)', raw_event)
            if m:
                date_str = m.group(1).strip()
                # 간단한 날짜 추출 로직
                date_match = re.search(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\d{4}년\s*\d{1,2}월\s*\d{1,2}일', date_str)
                if date_match:
                    extracted = date_match.group(0)
                    if '년' in extracted:
                        parts = re.findall(r'\d+', extracted)
                        if len(parts) >= 3:
                            parsed_data['event_date'] = f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
                    else:
                        parsed_data['event_date'] = extracted
                
                time_match = re.search(r'(\d{1,2}:\d{2}|\d{1,2}시)', date_str)
                if time_match: parsed_data['event_time'] = time_match.group(0)
        
        if "✅" in raw_event:
            m = re.search(r'✅\s*\*\*준비물 체크리스트\*\*:?\s*([^🌍💡📌📅]+)', raw_event, re.DOTALL)
            if m:
                items = re.findall(r'[-•]\s*([^\n]+)', m.group(1))
                parsed_data['checklist_items'] = [i.strip() for i in items if is_valid_checklist_item(i)]
        
        # 나머지 섹션 추출
        for key, marker in [('translation', '🌐'), ('cultural_context', '🌍'), ('tips', '💡')]:
            if marker in raw_event:
                m = re.search(f'\\{marker}[^📌📅✅🌍💡]*([^📌📅✅🌍💡]+)', raw_event, re.DOTALL)
                if m:
                    text = m.group(1).strip()
                    text = re.sub(r'\*\*[^:]+\*\*:?\s*', '', text, flags=re.IGNORECASE).strip()
                    parsed_data[key] = text
        
        # 유의미한 데이터가 있는 경우만 추가
        if parsed_data['event_name'] or parsed_data['event_date'] or parsed_data['checklist_items']:
            parsed_events.append(parsed_data)
            
    return parsed_events
