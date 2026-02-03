import google.generativeai as genai
from PIL import Image
import re
from datetime import datetime

# 국가별 교육 문화 정보 (상세 버전)
COUNTRY_INFO = {
    "네덜란드": {
        "name": "네덜란드",
        "culture": """네덜란드 교육 시스템은 매우 개방적이고 실용적이며, 자유로운 분위기가 특징입니다.

**주요 행사 및 기념일:**
- Studiedag (스투디다흐): 교사 연수일로 아이들이 등교하지 않습니다. 보통 학기 중 2-3회 있습니다.
- Koningsdag (코닝스다흐, 국왕의 날): 4월 27일, 오렌지색으로 치장하고 거리 축제가 열립니다.
- Sinterklaas (신테르클라스): 12월 5일, 성 니콜라스 축제로 아이들에게 선물을 주는 중요한 전통 행사입니다.
- Ouderspreekavond (아우더스프레이크아본트): 학부모 상담일
- Schoolreisje (스훌레이셰): 학교 여행/소풍

**교육 문화 특징:**
- 매우 개방적이고 비공식적인 분위기
- 교사와 학부모 간의 수평적 관계
- 실용적이고 창의적인 교육 접근
- 조기 퇴교가 일반적 (보통 오후 3시 전)
- 생일 파티를 학교에서 자주 합니다 (traktatie 준비 필요)""",
        "context_guidance": "네덜란드의 개방적이고 실용적인 교육 문화, 자유로운 분위기, 그리고 학부모 참여 방식의 특징을 반영하여 설명해주세요."
    },
    "미국": {
        "name": "미국",
        "culture": """미국 학교는 학부모 참여가 매우 활발하고, 다양한 행사와 문화적 기념일이 중요합니다.

**주요 행사 및 기념일:**
- PTA (Parent-Teacher Association) 모임: 학부모 교사 협회 정기 모임
- Field Trip (필드트립): 교육적 현장 학습 여행
- Picture Day (포토데이): 학교 사진 촬영일
- Thanksgiving (추수감사절): 11월 셋째 목요일, 가족 모임이 중요
- Halloween (할로윈): 10월 31일, 코스튬과 사탕이 필수
- Martin Luther King Jr. Day: 1월 셋째 월요일
- Presidents' Day, Memorial Day 등 공휴일

**교육 문화 특징:**
- 학부모 자원봉사가 매우 활발함
- 다양한 문화적 배경의 학생들
- 학교 행사에 적극적인 참여 문화
- Fundraising 이벤트가 많음
- 교사와 학부모 간의 정기적인 소통""",
        "context_guidance": "미국의 활발한 학부모 참여 문화, 다양한 문화적 배경, 그리고 학부모가 알아야 할 행사 준비 방법을 반영하여 설명해주세요."
    },
    "독일": {
        "name": "독일",
        "culture": """독일 교육은 연방제로 인해 지역(Bundesland)별로 차이가 크며, 구조화된 시스템이 특징입니다.

**주요 행사 및 기념일:**
- Schulfest (슐페스트): 학교 축제, 보통 여름에 열립니다
- Wandertag (반데르타크): 등산의 날, 자연 학습과 운동을 결합
- Elternabend (엘테른아벤트): 학부모 상담일
- Einschulung (아인슐룽): 초등학교 입학식, Schultüte(슐튀테) 준비 필요
- 지역별 공휴일과 축제일이 다양함

**교육 문화 특징:**
- 지역별로 교육 시스템이 다름 (예: 바이에른은 가장 엄격)
- 구조화되고 체계적인 교육 접근
- 조기 교육에 대한 강조
- 학부모 참여는 중요하지만 공식적
- 생일 파티는 보통 집에서, 학교에서는 간단히 축하""",
        "context_guidance": "독일의 지역별 차이, 구조화된 교육 시스템, 그리고 학부모가 알아야 할 지역별 특성을 반영하여 설명해주세요."
    },
    "영국": {
        "name": "영국",
        "culture": """영국 학교는 전통적이면서도 현대적인 교육 시스템을 가지고 있으며, 하우스 시스템과 엄격한 규정이 특징입니다.

**주요 행사 및 기념일:**
- Parents' Evening (페런츠 이브닝): 학부모 상담일, 정기적으로 열립니다
- Sports Day (스포츠 데이): 운동회, 하우스별 경쟁이 있습니다
- INSET Day (인셋 데이): 교사 연수일, 학생은 등교하지 않습니다
- Bank Holiday: 영국 공휴일 (5월, 8월 등)
- Harvest Festival (추수 감사절): 가을 행사
- Christmas Nativity: 크리스마스 연극/공연

**교육 문화 특징:**
- 하우스(House) 시스템으로 학생들을 그룹화
- 엄격한 교복 규정
- 전통적인 교육 방식과 현대적 접근의 조화
- 학부모 참여는 중요하지만 공식적
- 학교 규칙과 예의가 중요함""",
        "context_guidance": "영국의 전통적 교육 시스템, 하우스 시스템, 그리고 학부모가 알아야 할 학교 문화와 예의를 반영하여 설명해주세요."
    },
    "기타": {
        "name": "기타 국가",
        "culture": """해당 국가의 고유한 교육 문화, 주요 기념일, 학교 행사 전통을 고려하여 분석하겠습니다.

**일반적인 고려사항:**
- 해당 국가의 교육 시스템 특징
- 주요 공휴일과 문화적 기념일
- 학교 행사 전통과 관습
- 학부모 참여 방식
- 지역별 차이점""",
        "context_guidance": "해당 국가의 교육 문화, 주요 기념일, 학교 행사 전통, 그리고 학부모가 알아야 할 문화적 맥락을 반영하여 설명해주세요."
    }
}

def get_prompt(country, text_input=None, has_image=False):
    """국가별 프롬프트 생성"""
    country_info = COUNTRY_INFO.get(country, COUNTRY_INFO["기타"])
    context_guidance = country_info.get('context_guidance', '해당 국가의 교육 문화와 전통을 반영하여 설명해주세요.')
    
    prompt = f"""당신은 {country_info['name']}에서 거주하는 한인 학부모를 위한 교육 문화 전문가입니다.
당신의 목표는 {country_info['name']}의 교육 시스템, 문화, 전통을 깊이 이해하고 이를 바탕으로 학교 알림장을 분석하는 것입니다.

**{country_info['name']} 교육 문화 배경 정보:**
{country_info['culture']}

**중요한 분석 원칙:**
1. 반드시 {country_info['name']}의 교육 문화와 전통을 고려하여 분석해야 합니다.
2. 행사명, 날짜, 준비물을 추출할 때 {country_info['name']}의 관습을 반영해야 합니다.
3. Cultural Context는 반드시 {country_info['name']}의 맥락에서 설명해야 합니다.
4. 실용적인 팁도 {country_info['name']}에서 실제로 유용한 정보여야 합니다.

사용자가 제공한 학교 알림장을 분석하여, 포함된 **모든 일정**을 찾아서 분석해주세요.
알림장에 여러 개의 행사나 일정이 포함되어 있다면, 반드시 **각 일정별로 구분**하여 아래 형식을 반복해서 작성해주세요.
각 일정 사이에는 `---EVENT_SEPARATOR---` 라는 구분선을 반드시 넣어주세요.

**출력 형식:**

🌐 **원문 번역 (한국어)**:
[해당 일정과 관련된 원문 부분만 한국어로 번역]

📌 **행사명**: [행사 이름]
📅 **일시**: [날짜와 시간] (YYYY-MM-DD HH:MM 형식 권장)
✅ **준비물 체크리스트**:
- [준비물 1]
- [준비물 2]
...

🌍 **Cultural Context (문화적 배경)**:
[이 행사가 {country_info['name']}에서 가지는 의미와 중요성, 교육 시스템에서의 진행 방식, 학부모가 알아야 할 문화적 배경을 2-3문장으로 설명]

💡 **실용적인 팁**:
[{country_info['name']}의 관습에 맞는 준비 방법, 주의사항, 흔히 하는 실수 등을 구체적으로 제안 (2-3문장)]

---EVENT_SEPARATOR---

(다음 일정이 있으면 위 형식을 반복, 없으면 종료)

**중요한 작성 지침:**
- 일정이 하나라도, 형식을 정확히 지켜주세요.
- 일정이 여러 개라면 `---EVENT_SEPARATOR---`로 명확히 구분해주세요.
- **Cultural Context는 반드시 {country_info['name']}의 교육 문화와 전통을 반영해야 합니다.** {context_guidance}
- **실용적인 팁도 {country_info['name']}에서 실제로 적용 가능한 구체적인 조언이어야 합니다.**
- 행사명을 추출할 때 {country_info['name']}의 용어와 관습을 고려해주세요.
- 날짜 형식도 {country_info['name']}의 관습을 반영해주세요.
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
        
    # 정규표현식으로 각 섹션 추출 (이모지 선택적 허용, 키워드 중심)
        
        # 1. 행사명
        m_name = re.search(r'(?:📌|:)\s*\**행사명\**[:\s]*([^\n📅✅🌍💡🌐]+)', raw_event)
        if m_name: parsed_data['event_name'] = m_name.group(1).strip()
        
        # 2. 일시
        m_date = re.search(r'(?:📅|:)\s*\**일시\**[:\s]*([^\n📌✅🌍💡🌐]+)', raw_event)
        if m_date:
            date_str = m_date.group(1).strip()
            # 날짜 추출
            date_match = re.search(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\d{4}년\s*\d{1,2}월\s*\d{1,2}일', date_str)
            if date_match:
                extracted = date_match.group(0)
                if '년' in extracted:
                    parts = re.findall(r'\d+', extracted)
                    if len(parts) >= 3:
                        parsed_data['event_date'] = f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
                else:
                    parsed_data['event_date'] = extracted
            
            # 시간 추출
            time_match = re.search(r'(\d{1,2}:\d{2}|\d{1,2}시)', date_str)
            if time_match: parsed_data['event_time'] = time_match.group(0)
            
        # 3. 준비물 체크리스트
        m_check = re.search(r'(?:✅|:)\s*\**준비물(?: 체크리스트)?\**[:\s]*([^🌍💡🌐📌📅]+)', raw_event, re.DOTALL)
        if m_check:
            items = re.findall(r'[-•]\s*([^\n]+)', m_check.group(1))
            parsed_data['checklist_items'] = [i.strip() for i in items if is_valid_checklist_item(i)]
            
        # 4. 번역 (🌐 또는 '원문 번역' 키워드)
        # 헤더를 찾고, 다음 헤더(행사명, 일시, 준비물, 문화, 팁)가 나오기 전까지 추출
        m_trans = re.search(r'(?:🌐|:)\s*\**원문\s*번역(?: \(한국어\))?\**[:\s]*(.*?)(?=(?:📌|📅|✅|🌍|💡|:?\s*\**행사명|:?\s*\**일시|:?\s*\**준비물|:?\s*\**Cultural|:?\s*\**문화|:?\s*\**실용적인|:?\s*\**팁)|$)', raw_event, re.DOTALL)
        if m_trans:
            text = m_trans.group(1).strip()
            if text: parsed_data['translation'] = text

        # 5. Cultural Context (🌍 또는 'Cultural'/'문화' 키워드)
        m_context = re.search(r'(?:🌍|:)\s*\**(?:Cultural Context|문화적 배경)\**[:\s]*(.*?)(?=(?:📌|📅|✅|💡|:?\s*\**행사명|:?\s*\**일시|:?\s*\**준비물|:?\s*\**실용적인|:?\s*\**팁)|$)', raw_event, re.DOTALL)
        if m_context:
            text = m_context.group(1).strip()
            if text: parsed_data['cultural_context'] = text
            
        # 6. 실용적인 팁 (💡 또는 '팁' 키워드)
        m_tips = re.search(r'(?:💡|:)\s*\**(?:실용적인 팁|팁)\**[:\s]*(.*?)(?=(?:📌|📅|✅|🌍|:?\s*\**행사명|:?\s*\**일시|:?\s*\**준비물|:?\s*\**Cultural|:?\s*\**문화)|$)', raw_event, re.DOTALL)
        if m_tips:
            text = m_tips.group(1).strip()
            if text: parsed_data['tips'] = text
        
        # 유의미한 데이터가 있는 경우만 추가
        if parsed_data['event_name'] or parsed_data['event_date'] or parsed_data['checklist_items'] or parsed_data['translation']:
            parsed_events.append(parsed_data)
            
    return parsed_events
