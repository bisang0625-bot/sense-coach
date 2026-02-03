import React, { useState, useEffect } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    TextInput,
    Alert,
    ActivityIndicator,
    Platform,
} from 'react-native';
import DateTimePicker from '@react-native-community/datetimepicker';
import { saveEvent, getChildren } from '../services/api';

interface ResultScreenProps {
    route: any;
    navigation: any;
}

const ResultScreen: React.FC<ResultScreenProps> = ({ route, navigation }) => {
    const { result, country } = route.params || {};
    const [saving, setSaving] = useState(false);
    const [children, setChildren] = useState<string[]>([]);
    const [expandedTranslation, setExpandedTranslation] = useState<number | null>(null);

    // DateTimePicker 상태
    const [showDatePicker, setShowDatePicker] = useState(false);
    const [showTimePicker, setShowTimePicker] = useState(false);
    const [pickerEventIndex, setPickerEventIndex] = useState<number | null>(null);

    // 분석 결과를 로컬 상태로 관리하여 편집 가능하게 함
    const [events, setEvents] = useState<any[]>([]);

    useEffect(() => {
        if (result && result.parsed_events) {
            setEvents(result.parsed_events.map((e: any) => ({
                ...e,
                child_tags: [] as string[],
                is_saved: false
            })));
        }
        fetchChildren();
    }, [result]);

    const fetchChildren = async () => {
        try {
            const data = await getChildren();
            if (data && data.children) {
                setChildren(data.children);
            }
        } catch (error) {
            console.error('Failed to fetch children:', error);
        }
    };

    const updateEventField = (index: number, field: string, value: any) => {
        setEvents(prevEvents => {
            const newEvents = [...prevEvents];
            if (newEvents[index]) {
                newEvents[index] = { ...newEvents[index], [field]: value };
            }
            return newEvents;
        });
    };

    // 날짜 선택 핸들러
    const handleDateChange = (event: any, selectedDate?: Date) => {
        setShowDatePicker(Platform.OS === 'ios');
        if (selectedDate && pickerEventIndex !== null) {
            const dateStr = selectedDate.toISOString().split('T')[0]; // YYYY-MM-DD
            updateEventField(pickerEventIndex, 'event_date', dateStr);
        }
        if (Platform.OS === 'android') {
            setShowDatePicker(false);
        }
    };

    // 시간 선택 핸들러
    const handleTimeChange = (event: any, selectedTime?: Date) => {
        setShowTimePicker(Platform.OS === 'ios');
        if (selectedTime && pickerEventIndex !== null) {
            const hours = selectedTime.getHours().toString().padStart(2, '0');
            const minutes = selectedTime.getMinutes().toString().padStart(2, '0');
            updateEventField(pickerEventIndex, 'event_time', `${hours}:${minutes}`);
        }
        if (Platform.OS === 'android') {
            setShowTimePicker(false);
        }
    };

    // 현재 날짜를 Date 객체로 변환
    const getDateFromString = (dateStr: string): Date => {
        if (dateStr && /^\d{4}-\d{2}-\d{2}$/.test(dateStr)) {
            return new Date(dateStr + 'T00:00:00');
        }
        return new Date();
    };

    // 현재 시간을 Date 객체로 변환
    const getTimeFromString = (timeStr: string): Date => {
        const now = new Date();
        if (timeStr && /^\d{1,2}:\d{2}$/.test(timeStr)) {
            const [hours, minutes] = timeStr.split(':').map(Number);
            now.setHours(hours, minutes, 0, 0);
        }
        return now;
    };

    const toggleChildTag = (index: number, childName: string) => {
        setEvents(prevEvents => {
            const newEvents = [...prevEvents];
            if (newEvents[index]) {
                const currentTags = newEvents[index].child_tags || [];
                if (currentTags.includes(childName)) {
                    newEvents[index].child_tags = currentTags.filter((t: string) => t !== childName);
                } else {
                    newEvents[index].child_tags = [...currentTags, childName];
                }
            }
            return newEvents;
        });
    };

    const handleSaveEvent = async (event: any, index: number) => {
        if (!event) return;
        setSaving(true);
        try {
            const tags = event.child_tags || [];
            await saveEvent({
                event_name: event.event_name,
                event_date: event.event_date,
                event_time: event.event_time || '',
                country: country || '네덜란드',
                child_tag: tags.length > 0 ? tags.join(', ') : '없음',
                translation: event.translation || '',
                cultural_context: event.cultural_context || '',
                tips: event.tips || '',
                checklist_items: event.checklist_items || [],
                memo: '',
            });

            setEvents(prevEvents => {
                const newEvents = [...prevEvents];
                if (newEvents[index]) {
                    newEvents[index].is_saved = true;
                }
                return newEvents;
            });
            Alert.alert('성공', '일정이 저장되었습니다!');
        } catch (error: any) {
            Alert.alert('오류', error.response?.data?.detail || '저장 중 오류가 발생했습니다.');
        } finally {
            setSaving(false);
        }
    };

    if (!result) {
        return (
            <View style={styles.center}>
                <Text>분석 결과 데이터를 찾을 수 없습니다.</Text>
                <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
                    <Text>뒤로 가기</Text>
                </TouchableOpacity>
            </View>
        );
    }

    return (
        <ScrollView style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>✨ AI 분석 결과</Text>
                <Text style={styles.subtitle}>
                    {country || '네덜란드'}의 교육 문화 맥락에서 분석했습니다
                </Text>
            </View>

            {events.length === 0 ? (
                <View style={styles.emptyState}>
                    <Text style={styles.emptyText}>분석된 일정이 없습니다.</Text>
                </View>
            ) : (
                events.map((event, index) => (
                    <View key={index} style={[styles.eventCard, event.is_saved && styles.eventCardSaved]}>

                        {/* 번역 섹션 - 접을 수 있는 UI */}
                        {/* 🌐 번역 섹션 - 항상 펼쳐보이게 수정 */}
                        {event.translation ? (
                            <View style={styles.translationBox}>
                                <View style={styles.sectionHeaderRow}>
                                    <Text style={styles.collapsibleTitle}>🌐 원문 번역</Text>
                                </View>
                                <Text style={styles.translationText}>{event.translation}</Text>
                            </View>
                        ) : null}

                        {/* 📌 행사 기본 정보 */}
                        <View style={styles.infoSection}>
                            <Text style={styles.sectionTitle}>📋 행사 정보</Text>

                            <View style={styles.infoRow}>
                                <Text style={styles.infoLabel}>📌 행사명</Text>
                                <TextInput
                                    style={styles.inlineInput}
                                    value={event.event_name || ''}
                                    onChangeText={(val) => updateEventField(index, 'event_name', val)}
                                    editable={!event.is_saved}
                                    autoCorrect={false}
                                    autoCapitalize="none"
                                />
                            </View>

                            <View style={styles.infoRow}>
                                <Text style={styles.infoLabel}>📅 일시</Text>
                                <View style={styles.dateTimeRow}>
                                    <TouchableOpacity
                                        style={[styles.datePickerButton, { flex: 1, marginRight: 8 }]}
                                        onPress={() => {
                                            if (!event.is_saved) {
                                                setPickerEventIndex(index);
                                                setShowDatePicker(true);
                                            }
                                        }}
                                        disabled={event.is_saved}
                                    >
                                        <Text style={styles.datePickerText}>
                                            {event.event_date || '📅 날짜 선택'}
                                        </Text>
                                    </TouchableOpacity>
                                    <TouchableOpacity
                                        style={[styles.datePickerButton, { flex: 0.6 }]}
                                        onPress={() => {
                                            if (!event.is_saved) {
                                                setPickerEventIndex(index);
                                                setShowTimePicker(true);
                                            }
                                        }}
                                        disabled={event.is_saved}
                                    >
                                        <Text style={styles.datePickerText}>
                                            {event.event_time || '⏰ 시간'}
                                        </Text>
                                    </TouchableOpacity>
                                </View>
                            </View>

                            {children.length > 0 && (
                                <View style={styles.childSection}>
                                    <Text style={styles.infoLabel}>👶 아이 선택 (복수 가능)</Text>
                                    <View style={styles.childChips}>
                                        {children.map(c => (
                                            <TouchableOpacity
                                                key={c}
                                                disabled={event.is_saved}
                                                style={[
                                                    styles.childChip,
                                                    (event.child_tags || []).includes(c) && styles.childChipSelected
                                                ]}
                                                onPress={() => toggleChildTag(index, c)}
                                            >
                                                <Text style={[
                                                    styles.childChipText,
                                                    (event.child_tags || []).includes(c) && styles.childChipTextSelected
                                                ]}>{c}</Text>
                                            </TouchableOpacity>
                                        ))}
                                    </View>
                                </View>
                            )}
                        </View>

                        {/* ✅ 준비물 체크리스트 */}
                        {event.checklist_items && event.checklist_items.length > 0 && (
                            <View style={styles.checklistSection}>
                                <Text style={styles.sectionTitle}>✅ 준비물 체크리스트</Text>
                                {event.checklist_items.map((item: string, i: number) => (
                                    <View key={i} style={styles.checklistItem}>
                                        <Text style={styles.checklistBullet}>•</Text>
                                        <Text style={styles.checklistText}>{item}</Text>
                                    </View>
                                ))}
                            </View>
                        )}

                        {/* 🌍 Cultural Context - 핵심 기능! */}
                        {event.cultural_context ? (
                            <View style={styles.culturalContextBox}>
                                <Text style={styles.culturalTitle}>🌍 Cultural Context (문화적 배경)</Text>
                                <Text style={styles.culturalText}>{event.cultural_context}</Text>
                            </View>
                        ) : null}

                        {/* 💡 실용적인 팁 - 핵심 기능! */}
                        {event.tips ? (
                            <View style={styles.tipsBox}>
                                <Text style={styles.tipsTitle}>💡 실용적인 팁</Text>
                                <Text style={styles.tipsText}>{event.tips}</Text>
                            </View>
                        ) : null}

                        {/* 저장 버튼 */}
                        <TouchableOpacity
                            style={[styles.saveButton, (saving || event.is_saved) && styles.saveButtonDisabled]}
                            onPress={() => handleSaveEvent(event, index)}
                            disabled={saving || event.is_saved}
                        >
                            {saving ? (
                                <ActivityIndicator color="#fff" />
                            ) : (
                                <Text style={styles.saveButtonText}>
                                    {event.is_saved ? '✅ 일정 저장 완료' : '💾 일정으로 저장하기'}
                                </Text>
                            )}
                        </TouchableOpacity>
                    </View>
                ))
            )}

            <View style={styles.buttonRow}>
                <TouchableOpacity
                    style={styles.backButton}
                    onPress={() => navigation.goBack()}
                >
                    <Text style={styles.backButtonText}>← 다시 분석하기</Text>
                </TouchableOpacity>

                <TouchableOpacity
                    style={styles.dashboardButton}
                    onPress={() => navigation.navigate('Dashboard')}
                >
                    <Text style={styles.dashboardButtonText}>📅 일정 보기</Text>
                </TouchableOpacity>
            </View>
            <View style={{ height: 40 }} />

            {/* DateTimePicker 레이어 */}
            {showDatePicker && pickerEventIndex !== null && (
                <DateTimePicker
                    value={getDateFromString(events[pickerEventIndex]?.event_date || '')}
                    mode="date"
                    display={Platform.OS === 'ios' ? 'spinner' : 'default'}
                    onChange={handleDateChange}
                />
            )}
            {showTimePicker && pickerEventIndex !== null && (
                <DateTimePicker
                    value={getTimeFromString(events[pickerEventIndex]?.event_time || '')}
                    mode="time"
                    is24Hour={true}
                    display={Platform.OS === 'ios' ? 'spinner' : 'default'}
                    onChange={handleTimeChange}
                />
            )}
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F5F7FA',
    },
    center: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
    },
    header: {
        padding: 20,
        alignItems: 'center',
        backgroundColor: '#fff',
        borderBottomLeftRadius: 24,
        borderBottomRightRadius: 24,
        marginBottom: 16,
    },
    title: {
        fontSize: 26,
        fontWeight: 'bold',
        color: '#1a1a2e',
        marginBottom: 6,
    },
    subtitle: {
        fontSize: 14,
        color: '#666',
        textAlign: 'center',
    },
    emptyState: {
        padding: 40,
        alignItems: 'center',
    },
    emptyText: {
        fontSize: 16,
        color: '#999',
    },
    eventCard: {
        backgroundColor: '#fff',
        marginHorizontal: 16,
        marginBottom: 20,
        borderRadius: 20,
        padding: 0,
        overflow: 'hidden',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.1,
        shadowRadius: 12,
        elevation: 5,
    },
    eventCardSaved: {
        opacity: 0.85,
        borderColor: '#4ECDC4',
        borderWidth: 2,
    },

    // 번역 섹션
    sectionHeaderRow: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 8,
    },
    collapsibleHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: 16,
        backgroundColor: '#f0f8f0',
        borderBottomWidth: 1,
        borderBottomColor: '#e0e0e0',
    },
    collapsibleTitle: {
        fontSize: 15,
        fontWeight: '600',
        color: '#2E7D32',
    },
    expandIcon: {
        fontSize: 12,
        color: '#2E7D32',
    },
    translationBox: {
        backgroundColor: '#f8fdf8',
        padding: 16,
        borderBottomWidth: 1,
        borderBottomColor: '#e0e0e0',
    },
    translationText: {
        fontSize: 14,
        color: '#333',
        lineHeight: 22,
    },

    // 행사 정보 섹션
    infoSection: {
        padding: 16,
        borderBottomWidth: 1,
        borderBottomColor: '#f0f0f0',
    },
    sectionTitle: {
        fontSize: 16,
        fontWeight: '700',
        color: '#333',
        marginBottom: 12,
    },
    infoRow: {
        marginBottom: 12,
    },
    infoLabel: {
        fontSize: 13,
        fontWeight: '600',
        color: '#888',
        marginBottom: 4,
    },
    inlineInput: {
        backgroundColor: '#f8f9fa',
        borderRadius: 8,
        padding: 10,
        fontSize: 15,
        borderWidth: 1,
        borderColor: '#e0e0e0',
        color: '#333',
    },
    dateTimeRow: {
        flexDirection: 'row',
    },
    datePickerButton: {
        backgroundColor: '#f8f9fa',
        borderRadius: 8,
        padding: 12,
        borderWidth: 1,
        borderColor: '#4ECDC4',
        justifyContent: 'center',
        alignItems: 'center',
    },
    datePickerText: {
        fontSize: 15,
        color: '#333',
        fontWeight: '500',
    },
    childSection: {
        marginTop: 4,
    },
    childChips: {
        flexDirection: 'row',
        flexWrap: 'wrap',
    },
    childChip: {
        paddingHorizontal: 12,
        paddingVertical: 6,
        borderRadius: 15,
        backgroundColor: '#eee',
        marginRight: 8,
        marginBottom: 8,
    },
    childChipSelected: {
        backgroundColor: '#4ECDC4',
    },
    childChipText: {
        fontSize: 13,
        color: '#666',
    },
    childChipTextSelected: {
        color: '#fff',
        fontWeight: 'bold',
    },

    // 준비물 체크리스트
    checklistSection: {
        padding: 16,
        backgroundColor: '#fafafa',
        borderBottomWidth: 1,
        borderBottomColor: '#f0f0f0',
    },
    checklistItem: {
        flexDirection: 'row',
        alignItems: 'flex-start',
        marginBottom: 6,
    },
    checklistBullet: {
        fontSize: 16,
        color: '#4ECDC4',
        marginRight: 8,
        fontWeight: 'bold',
    },
    checklistText: {
        fontSize: 14,
        color: '#444',
        flex: 1,
        lineHeight: 20,
    },

    // 🌍 Cultural Context 박스 - 핵심!
    culturalContextBox: {
        margin: 16,
        marginBottom: 12,
        padding: 16,
        backgroundColor: '#FFF8E1',
        borderRadius: 12,
        borderLeftWidth: 4,
        borderLeftColor: '#FFA000',
    },
    culturalTitle: {
        fontSize: 15,
        fontWeight: '700',
        color: '#E65100',
        marginBottom: 10,
    },
    culturalText: {
        fontSize: 14,
        color: '#5D4037',
        lineHeight: 22,
    },

    // 💡 실용적인 팁 박스 - 핵심!
    tipsBox: {
        margin: 16,
        marginTop: 0,
        marginBottom: 16,
        padding: 16,
        backgroundColor: '#E3F2FD',
        borderRadius: 12,
        borderLeftWidth: 4,
        borderLeftColor: '#1976D2',
    },
    tipsTitle: {
        fontSize: 15,
        fontWeight: '700',
        color: '#0D47A1',
        marginBottom: 10,
    },
    tipsText: {
        fontSize: 14,
        color: '#1565C0',
        lineHeight: 22,
    },

    // 저장 버튼
    saveButton: {
        backgroundColor: '#4ECDC4',
        paddingVertical: 14,
        margin: 16,
        marginTop: 8,
        borderRadius: 12,
        alignItems: 'center',
    },
    saveButtonDisabled: {
        backgroundColor: '#bbb',
    },
    saveButtonText: {
        color: '#fff',
        fontSize: 16,
        fontWeight: 'bold',
    },

    // 하단 버튼
    buttonRow: {
        flexDirection: 'row',
        padding: 16,
    },
    backButton: {
        flex: 1,
        marginRight: 8,
        padding: 15,
        borderRadius: 12,
        backgroundColor: '#fff',
        alignItems: 'center',
        borderWidth: 1,
        borderColor: '#ddd',
    },
    backButtonText: {
        color: '#666',
        fontWeight: '600',
    },
    dashboardButton: {
        flex: 1,
        marginLeft: 8,
        padding: 15,
        borderRadius: 12,
        backgroundColor: '#1a1a2e',
        alignItems: 'center',
    },
    dashboardButtonText: {
        color: '#fff',
        fontWeight: '600',
    },
});

export default ResultScreen;
