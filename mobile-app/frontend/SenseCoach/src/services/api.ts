import axios from 'axios';

// 프로덕션 API URL (Render.com)
const API_BASE_URL = 'https://sense-coach-api.onrender.com';

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// 서버 상태 확인
export const checkHealth = async () => {
    const response = await api.get('/api/health');
    return response.data;
};

// 알림장 텍스트 분석
export const analyzeNotice = async (text: string, country: string, userId: string) => {
    const response = await api.post('/api/analyze', {
        text,
        country,
        user_id: userId,
    });
    return response.data;
};

// 이미지 분석 (FormData 사용)
export const analyzeImage = async (
    imageUri: string,
    country: string,
    userId: string,
    text?: string
) => {
    const formData = new FormData();
    formData.append('file', {
        uri: imageUri,
        type: 'image/jpeg',
        name: 'notice.jpg',
    } as any);
    formData.append('country', country);
    formData.append('user_id', userId);
    if (text) {
        formData.append('text', text);
    }

    const response = await api.post('/api/analyze/image', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

// 이벤트 목록 조회
export const getEvents = async (futureOnly: boolean = false) => {
    const response = await api.get('/api/events', {
        params: { future_only: futureOnly },
    });
    return response.data;
};

// 이벤트 저장
export const saveEvent = async (eventData: any) => {
    const response = await api.post('/api/events', eventData);
    return response.data;
};

// 이벤트 삭제
export const deleteEvent = async (eventId: number) => {
    const response = await api.delete(`/api/events/${eventId}`);
    return response.data;
};

// 특정 이벤트 조회
export const getEventById = async (eventId: number) => {
    const response = await api.get(`/api/events/${eventId}`);
    return response.data;
};

// 이벤트 수정
export const updateEvent = async (eventId: number, eventData: any) => {
    const response = await api.put(`/api/events/${eventId}`, eventData);
    return response.data;
};

// 체크리스트 항목 상태 업데이트
export const updateChecklistItem = async (itemId: number, isChecked: boolean) => {
    const response = await api.put(`/api/checklist/${itemId}`, { is_checked: isChecked });
    return response.data;
};

// 체크리스트 항목 추가
export const addChecklistItem = async (eventId: number, itemName: string) => {
    const formData = new FormData();
    formData.append('item_name', itemName);
    const response = await api.post(`/api/events/${eventId}/checklist`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
};

// 체크리스트 항목 삭제
export const deleteChecklistItem = async (itemId: number) => {
    const response = await api.delete(`/api/checklist/${itemId}`);
    return response.data;
};

// 아이 목록 조회
export const getChildren = async () => {
    const response = await api.get('/api/children');
    return response.data;
};

// 아이 추가
export const addChild = async (name: string) => {
    const response = await api.post('/api/children', { name });
    return response.data;
};

// 아이 삭제
export const deleteChild = async (name: string) => {
    const response = await api.delete(`/api/children/${encodeURIComponent(name)}`);
    return response.data;
};

// 멤버십 정보 조회
export const getMembership = async (userId: string) => {
    const response = await api.get(`/api/user/${userId}/membership`);
    return response.data;
};

export default api;

