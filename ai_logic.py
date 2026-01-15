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
 
사용자가 제공한 학교 알림장을 분석하여 다음 형식으로 정확하게 응답해주세요:
 
🌐 **원문 번역 (한국어)**:
[학교 알림장의 원문을 한국어로 정확하고 자연스럽게 번역해주세요. 전문 용어나 현지 특유의 표현이 있으면 주석을 달아주세요.]
 
📌 **행사명**: [행사 이름을 명확하게]
📅 **일시**: [날짜와 시간을 구체적으로]
✅ **준비물 체크리스트**:
- [준비물 1] (현지 용어가 있으면 함께 표기)
- [준비물 2]
- [준비물 3]
...
 
🌍 **Cultural Context (문화적 배경)**:
[해당 행사나 준비물과 관련된 {country_info['name']}의 교육 문화, 현지 관습, 중요한 맥락을 간결하게 설명해주세요. 불릿포인트 형식으로 핵심 사항을 나열하되, 각 포인트에 대한 설명은 최대 2-3문장으로 간략하게 작성해주세요. 특히 한인 부모가 놓치기 쉬운 부분, 현지에서 특별히 중요한 점, 해당 국가만의 특징적인 교육 관습을 핵심만 간결하게 강조해주세요.]
 
💡 **실용적인 팁**:
[실제로 준비할 때 유용한 팁, 주의사항, 추가로 알아두면 좋은 정보를 불릿포인트 형식으로 제공해주세요. 각 팁은 최대 2-3문장으로 간결하게 작성하고, 핵심만 전달해주세요.]
 
**중요한 작성 지침:**
- 🌍 Cultural Context (문화적 배경): 불릿포인트로 핵심 사항 나열, 각 포인트 설명은 2-3문장 이내로 간결하게
- 💡 실용적인 팁: 불릿포인트로 제시, 각 팁은 2-3문장 이내로 간결하게
- 두 섹션 모두 불필요한 부연 설명, 반복, 장황한 설명은 피하고 핵심만 전달해주세요
- 전체 설명 분량은 현재 수준의 약 60% 정도로 작성해주세요
 
응답은 한국어로 작성하고, 친근하고 따뜻한 톤으로 작성해주세요. 원문 번역은 자세하게, Cultural Context와 실용적인 팁은 간결하게 작성해주세요."""
 
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
        
        # 사용할 모델 결정
        if image_input:
            try_models = [
                "models/gemini-1.5-flash-latest",
                "models/gemini-1.5-pro-latest",
                "models/gemini-pro-vision",
            ]
        else:
            try_models = [
                "models/gemini-1.5-flash-latest",
                "models/gemini-1.5-pro-latest",
                "models/gemini-pro",
            ]
        
        model = None
        for test_model in try_models:
            try:
                model = genai.GenerativeModel(test_model)
                break
            except:
                continue
        
        if model is None:
            raise Exception("사용 가능한 모델을 찾을 수 없습니다.")
        
        # 프롬프트 생성
        has_image = image_input is not None
        prompt = get_prompt(country, text_input, has_image)
        
        # 실행
        if image_input:
            img = Image.open(image_input)
            response = model.generate_content([prompt, img])
        else:
            response = model.generate_content(prompt)
        
        # 응답 처리
        if hasattr(response, 'text') and response.text:
            return response.text
        return "❌ 응답을 생성할 수 없습니다."
        
    except Exception as e:
        return f"❌ 오류 발생: {str(e)}"

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
    """분석 결과 파싱"""
    parsed_data = {
        'event_name': '', 'event_date': '', 'event_time': '',
        'country': country, 'checklist_items': [],
        'translation': '', 'cultural_context': '', 'tips': '', 'memo': ''
    }
    
    # 정규표현식으로 각 섹션 추출 (app.py의 로직과 동일)
    if "📌" in result:
        m = re.search(r'📌\s*\*\*행사명\*\*:?\s*([^\n📅✅🌍💡]+)', result)
        if m: parsed_data['event_name'] = m.group(1).strip()
    
    if "📅" in result:
        m = re.search(r'📅\s*\*\*일시\*\*:?\s*([^\n📌✅🌍💡]+)', result)
        if m:
            date_str = m.group(1).strip()
            # 간단한 날짜 추출 로직 (app.py 참고)
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

    if "✅" in result:
        m = re.search(r'✅\s*\*\*준비물 체크리스트\*\*:?\s*([^🌍💡📌📅]+)', result, re.DOTALL)
        if m:
            items = re.findall(r'[-•]\s*([^\n]+)', m.group(1))
            parsed_data['checklist_items'] = [i.strip() for i in items if is_valid_checklist_item(i)]

    # 나머지 섹션 추출 (생략 가능하나 일단 유지)
    for key, marker in [('translation', '🌐'), ('cultural_context', '🌍'), ('tips', '💡')]:
        if marker in result:
            m = re.search(f'\\{marker}[^📌📅✅🌍💡]*([^📌📅✅🌍💡]+)', result, re.DOTALL)
            if m:
                text = m.group(1).strip()
                # 서두 제거
                text = re.sub(r'\*\*[^:]+\*\*:?\s*', '', text, flags=re.IGNORECASE).strip()
                parsed_data[key] = text

    return parsed_data
