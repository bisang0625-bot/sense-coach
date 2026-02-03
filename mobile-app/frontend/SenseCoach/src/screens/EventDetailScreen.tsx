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
import {
    getEventById,
    updateEvent,
    updateChecklistItem,
    getChildren,
    addChecklistItem,
    deleteChecklistItem
} from '../services/api';

interface EventDetailScreenProps {
    route: any;
    navigation: any;
}

const EventDetailScreen: React.FC<EventDetailScreenProps> = ({ route, navigation }) => {
    const { eventId } = route.params || {};
    const [event, setEvent] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);
    const [children, setChildren] = useState<string[]>([]);
    const [newItemName, setNewItemName] = useState('');

    // 편집용 상태
    const [editedName, setEditedName] = useState('');
    const [editedDate, setEditedDate] = useState('');
    const [editedTime, setEditedTime] = useState('');
    const [editedChild, setEditedChild] = useState('');
    const [editedMemo, setEditedMemo] = useState('');

    // DateTimePicker 상태
    const [showDatePicker, setShowDatePicker] = useState(false);
    const [showTimePicker, setShowTimePicker] = useState(false);

    useEffect(() => {
        fetchData();
    }, [eventId]);

    const fetchData = async () => {
        setLoading(true);
        try {
            const eventData = await getEventById(eventId);
            const childData = await getChildren();

            const e = eventData.event;
            setEvent(e);
            setChildren(childData.children || []);

            // 편집 상태 초기화
            setEditedName(e.event_name);
            setEditedDate(e.event_date);
            setEditedTime(e.event_time);
            setEditedChild(e.child_tag);
            setEditedMemo(e.memo);

            navigation.setOptions({ title: e.event_name });
        } catch (error) {
            console.error(error);
            Alert.alert('오류', '데이터를 불러오지 못했습니다.');
        } finally {
            setLoading(false);
        }
    };

    const handleToggleItem = async (itemId: number, currentStatus: boolean) => {
        try {
            await updateChecklistItem(itemId, !currentStatus);
            // 로컬 상태 업데이트
            setEvent({
                ...event,
                checklist_with_status: event.checklist_with_status.map((item: any) =>
                    item.id === itemId ? { ...item, is_checked: !currentStatus } : item
                ),
            });
        } catch (error) {
            Alert.alert('오류', '상태 변경에 실패했습니다.');
        }
    };

    const handleAddItem = async () => {
        if (!newItemName.trim()) return;
        try {
            await addChecklistItem(eventId, newItemName.trim());
            setNewItemName('');
            fetchData(); // 전체 다시 불러오기
        } catch (error) {
            Alert.alert('오류', '항목 추가에 실패했습니다.');
        }
    };

    const handleDeleteItem = async (itemId: number) => {
        try {
            await deleteChecklistItem(itemId);
            fetchData();
        } catch (error) {
            Alert.alert('오류', '항목 삭제에 실패했습니다.');
        }
    };

    const handleSave = async () => {
        try {
            setLoading(true);
            await updateEvent(eventId, {
                event_name: editedName,
                event_date: editedDate,
                event_time: editedTime,
                child_tag: editedChild,
                memo: editedMemo,
            });
            setIsEditing(false);
            fetchData();
            Alert.alert('성공', '일정이 수정되었습니다.');
        } catch (error) {
            Alert.alert('오류', '수정에 실패했습니다.');
        } finally {
            setLoading(false);
        }
    };

    // 날짜 선택 핸들러
    const handleDateChange = (event: any, selectedDate?: Date) => {
        setShowDatePicker(Platform.OS === 'ios');
        if (selectedDate) {
            const dateStr = selectedDate.toISOString().split('T')[0];
            setEditedDate(dateStr);
        }
        if (Platform.OS === 'android') {
            setShowDatePicker(false);
        }
    };

    // 시간 선택 핸들러
    const handleTimeChange = (event: any, selectedTime?: Date) => {
        setShowTimePicker(Platform.OS === 'ios');
        if (selectedTime) {
            const hours = selectedTime.getHours().toString().padStart(2, '0');
            const minutes = selectedTime.getMinutes().toString().padStart(2, '0');
            setEditedTime(`${hours}:${minutes}`);
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

    if (loading && !event) {
        return (
            <View style={styles.center}>
                <ActivityIndicator size="large" color="#4ECDC4" />
            </View>
        );
    }

    if (!event) return null;

    return (
        <ScrollView style={styles.container}>
            {/* 헤더 섹션 */}
            <View style={styles.headerCard}>
                {isEditing ? (
                    <View style={styles.editSection}>
                        <Text style={styles.label}>📌 행사명</Text>
                        <TextInput
                            style={styles.input}
                            value={editedName}
                            onChangeText={setEditedName}
                            autoCorrect={false}
                            autoCapitalize="none"
                        />
                        <View style={styles.row}>
                            <View style={{ flex: 1, marginRight: 8 }}>
                                <Text style={styles.label}>📅 날짜</Text>
                                <TouchableOpacity
                                    style={styles.datePickerButton}
                                    onPress={() => setShowDatePicker(true)}
                                >
                                    <Text style={styles.datePickerText}>
                                        {editedDate || '📅 날짜 선택'}
                                    </Text>
                                </TouchableOpacity>
                            </View>
                            <View style={{ flex: 1, marginLeft: 8 }}>
                                <Text style={styles.label}>⏰ 시간</Text>
                                <TouchableOpacity
                                    style={styles.datePickerButton}
                                    onPress={() => setShowTimePicker(true)}
                                >
                                    <Text style={styles.datePickerText}>
                                        {editedTime || '⏰ 시간 선택'}
                                    </Text>
                                </TouchableOpacity>
                            </View>
                        </View>
                        <Text style={styles.label}>👶 아이 선택</Text>
                        <View style={styles.childChips}>
                            <TouchableOpacity
                                style={[styles.childChip, editedChild === '없음' && styles.childChipSelected]}
                                onPress={() => setEditedChild('없음')}
                            >
                                <Text style={[styles.childChipText, editedChild === '없음' && styles.childChipTextSelected]}>없음</Text>
                            </TouchableOpacity>
                            {children.map(c => (
                                <TouchableOpacity
                                    key={c}
                                    style={[styles.childChip, editedChild === c && styles.childChipSelected]}
                                    onPress={() => setEditedChild(c)}
                                >
                                    <Text style={[styles.childChipText, editedChild === c && styles.childChipTextSelected]}>{c}</Text>
                                </TouchableOpacity>
                            ))}
                        </View>
                    </View>
                ) : (
                    <View>
                        <View style={styles.titleRow}>
                            <Text style={styles.title}>{event.event_name}</Text>
                            {event.child_tag !== '없음' && (
                                <View style={styles.tagBadge}>
                                    <Text style={styles.tagBadgeText}>{event.child_tag}</Text>
                                </View>
                            )}
                        </View>
                        <Text style={styles.dateTime}>📅 {event.event_date} {event.event_time}</Text>
                    </View>
                )}

                <TouchableOpacity
                    style={[styles.editToggleButton, isEditing && styles.saveButton]}
                    onPress={isEditing ? handleSave : () => setIsEditing(true)}
                >
                    <Text style={styles.editToggleText}>{isEditing ? '💾 저장하기' : '✏️ 편집하기'}</Text>
                </TouchableOpacity>
                {isEditing && (
                    <TouchableOpacity style={styles.cancelButton} onPress={() => setIsEditing(false)}>
                        <Text style={styles.cancelButtonText}>취소</Text>
                    </TouchableOpacity>
                )}
            </View>

            {/* 체크리스트 섹션 */}
            <View style={styles.section}>
                <Text style={styles.sectionTitle}>✅ 준비물 체크리스트</Text>
                {event.checklist_with_status.map((item: any) => (
                    <View key={item.id} style={styles.checklistItem}>
                        <TouchableOpacity
                            style={styles.checkboxArea}
                            onPress={() => handleToggleItem(item.id, item.is_checked)}
                        >
                            <View style={[styles.checkbox, item.is_checked && styles.checkboxChecked]}>
                                {item.is_checked && <Text style={styles.checkIcon}>✓</Text>}
                            </View>
                            <Text style={[styles.itemText, item.is_checked && styles.itemTextChecked]}>
                                {item.name}
                            </Text>
                        </TouchableOpacity>
                        <TouchableOpacity onPress={() => handleDeleteItem(item.id)}>
                            <Text style={styles.deleteItem}>✕</Text>
                        </TouchableOpacity>
                    </View>
                ))}

                <View style={styles.addItemRow}>
                    <TextInput
                        style={styles.addItemInput}
                        placeholder="항목 추가..."
                        value={newItemName}
                        onChangeText={setNewItemName}
                    />
                    <TouchableOpacity style={styles.addItemButton} onPress={handleAddItem}>
                        <Text style={styles.addItemButtonText}>+</Text>
                    </TouchableOpacity>
                </View>
            </View>

            {/* 분석 정보 (보기 전용) */}
            {!isEditing && (
                <>
                    {event.cultural_context && (
                        <View style={styles.section}>
                            <Text style={styles.sectionTitle}>🌍 문화적 배경</Text>
                            <Text style={styles.content}>{event.cultural_context}</Text>
                        </View>
                    )}
                    {event.tips && (
                        <View style={styles.section}>
                            <Text style={styles.sectionTitle}>💡 팁</Text>
                            <Text style={styles.content}>{event.tips}</Text>
                        </View>
                    )}
                </>
            )}

            {/* 메모 섹션 */}
            <View style={styles.section}>
                <Text style={styles.sectionTitle}>📝 나의 메모</Text>
                {isEditing ? (
                    <TextInput
                        style={[styles.input, styles.textArea]}
                        multiline
                        value={editedMemo}
                        onChangeText={setEditedMemo}
                        placeholder="메모를 입력하세요..."
                    />
                ) : (
                    <Text style={styles.content}>{event.memo || '입력된 메모가 없습니다.'}</Text>
                )}
            </View>

            <View style={{ height: 40 }} />

            {/* DateTimePicker 레이어 */}
            {showDatePicker && (
                <DateTimePicker
                    value={getDateFromString(editedDate)}
                    mode="date"
                    display={Platform.OS === 'ios' ? 'spinner' : 'default'}
                    onChange={handleDateChange}
                />
            )}
            {showTimePicker && (
                <DateTimePicker
                    value={getTimeFromString(editedTime)}
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
    },
    headerCard: {
        backgroundColor: '#fff',
        padding: 20,
        borderBottomLeftRadius: 24,
        borderBottomRightRadius: 24,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 10,
        elevation: 5,
        marginBottom: 16,
    },
    titleRow: {
        flexDirection: 'row',
        alignItems: 'center',
        flexWrap: 'wrap',
        marginBottom: 8,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#1a1a2e',
        marginRight: 10,
    },
    tagBadge: {
        backgroundColor: '#4ECDC4',
        paddingHorizontal: 8,
        paddingVertical: 2,
        borderRadius: 6,
    },
    tagBadgeText: {
        color: '#fff',
        fontSize: 12,
        fontWeight: 'bold',
    },
    dateTime: {
        fontSize: 16,
        color: '#666',
        marginBottom: 20,
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
    section: {
        backgroundColor: '#fff',
        marginHorizontal: 16,
        marginBottom: 16,
        borderRadius: 16,
        padding: 16,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.05,
        shadowRadius: 5,
        elevation: 2,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: '700',
        color: '#333',
        marginBottom: 12,
    },
    content: {
        fontSize: 15,
        color: '#555',
        lineHeight: 22,
    },
    checklistItem: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingVertical: 10,
        borderBottomWidth: 1,
        borderBottomColor: '#f0f0f0',
    },
    checkboxArea: {
        flexDirection: 'row',
        alignItems: 'center',
        flex: 1,
    },
    checkbox: {
        width: 24,
        height: 24,
        borderRadius: 6,
        borderWidth: 2,
        borderColor: '#4ECDC4',
        marginRight: 12,
        alignItems: 'center',
        justifyContent: 'center',
    },
    checkboxChecked: {
        backgroundColor: '#4ECDC4',
    },
    checkIcon: {
        color: '#fff',
        fontWeight: 'bold',
    },
    itemText: {
        fontSize: 16,
        color: '#333',
    },
    itemTextChecked: {
        textDecorationLine: 'line-through',
        color: '#999',
    },
    deleteItem: {
        color: '#ccc',
        fontSize: 18,
        padding: 5,
    },
    addItemRow: {
        flexDirection: 'row',
        marginTop: 15,
    },
    addItemInput: {
        flex: 1,
        backgroundColor: '#f8f9fa',
        borderRadius: 8,
        padding: 10,
        marginRight: 10,
        borderWidth: 1,
        borderColor: '#eee',
    },
    addItemButton: {
        width: 44,
        height: 44,
        backgroundColor: '#1a1a2e',
        borderRadius: 8,
        alignItems: 'center',
        justifyContent: 'center',
    },
    addItemButtonText: {
        color: '#fff',
        fontSize: 24,
        fontWeight: '300',
    },
    editSection: {
        marginBottom: 15,
    },
    label: {
        fontSize: 13,
        fontWeight: '600',
        color: '#888',
        marginBottom: 5,
        marginTop: 10,
    },
    input: {
        backgroundColor: '#f8f9fa',
        borderRadius: 8,
        padding: 12,
        fontSize: 16,
        borderWidth: 1,
        borderColor: '#e0e0e0',
        color: '#333',
    },
    row: {
        flexDirection: 'row',
    },
    textArea: {
        minHeight: 100,
        textAlignVertical: 'top',
    },
    childChips: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: 8,
        marginTop: 5,
    },
    childChip: {
        paddingHorizontal: 12,
        paddingVertical: 6,
        borderRadius: 15,
        backgroundColor: '#eee',
    },
    childChipSelected: {
        backgroundColor: '#1a1a2e',
    },
    childChipText: {
        fontSize: 13,
        color: '#666',
    },
    childChipTextSelected: {
        color: '#fff',
        fontWeight: 'bold',
    },
    editToggleButton: {
        backgroundColor: '#f0f0f0',
        paddingVertical: 12,
        borderRadius: 12,
        alignItems: 'center',
        marginTop: 10,
    },
    saveButton: {
        backgroundColor: '#4ECDC4',
    },
    editToggleText: {
        fontWeight: 'bold',
        fontSize: 16,
        color: '#333',
    },
    cancelButton: {
        alignItems: 'center',
        marginTop: 8,
    },
    cancelButtonText: {
        color: '#eb4d4b',
        fontSize: 14,
    },
});

export default EventDetailScreen;
