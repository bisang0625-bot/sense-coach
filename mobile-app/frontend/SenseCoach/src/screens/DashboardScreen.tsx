import React, { useEffect, useState, useCallback } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    RefreshControl,
    Alert,
} from 'react-native';
import { getEvents, deleteEvent } from '../services/api';
import { useFocusEffect } from '@react-navigation/native';

interface DashboardScreenProps {
    navigation: any;
}

const DashboardScreen: React.FC<DashboardScreenProps> = ({ navigation }) => {
    const [events, setEvents] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);

    const fetchEvents = async () => {
        try {
            const data = await getEvents(false); // 모든 일정 보기 (디버깅용)
            setEvents(data.events || []);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    useFocusEffect(
        useCallback(() => {
            fetchEvents();
        }, [])
    );

    const onRefresh = () => {
        setRefreshing(true);
        fetchEvents();
    };

    const handleDeleteEvent = async (eventId: number) => {
        Alert.alert(
            '삭제 확인',
            '이 일정을 삭제하시겠습니까?',
            [
                { text: '취소', style: 'cancel' },
                {
                    text: '삭제',
                    style: 'destructive',
                    onPress: async () => {
                        try {
                            await deleteEvent(eventId);
                            fetchEvents();
                        } catch (error) {
                            Alert.alert('오류', '삭제 중 오류가 발생했습니다.');
                        }
                    },
                },
            ]
        );
    };

    const formatDate = (dateStr: string) => {
        if (!dateStr) return '날짜 미정';
        const date = new Date(dateStr);
        return `${date.getMonth() + 1}월 ${date.getDate()}일`;
    };

    const getDaysUntil = (dateStr: string) => {
        if (!dateStr) return null;
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const eventDate = new Date(dateStr);
        eventDate.setHours(0, 0, 0, 0);
        const diffTime = eventDate.getTime() - today.getTime();
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return diffDays;
    };

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>📅 다가오는 일정</Text>
                <Text style={styles.subtitle}>{events.length}개의 일정</Text>
            </View>

            <ScrollView
                style={styles.eventList}
                refreshControl={
                    <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
                }
            >
                {loading ? (
                    <Text style={styles.loadingText}>로딩 중...</Text>
                ) : events.length === 0 ? (
                    <View style={styles.emptyState}>
                        <Text style={styles.emptyIcon}>📭</Text>
                        <Text style={styles.emptyText}>저장된 일정이 없습니다</Text>
                        <TouchableOpacity
                            style={styles.addButton}
                            onPress={() => navigation.navigate('Home')}
                        >
                            <Text style={styles.addButtonText}>+ 알림장 분석하기</Text>
                        </TouchableOpacity>
                    </View>
                ) : (
                    events.map((event: any) => {
                        const daysUntil = getDaysUntil(event.event_date);
                        return (
                            <TouchableOpacity
                                key={event.id}
                                style={styles.eventCard}
                                onPress={() => navigation.navigate('Details', { eventId: event.id })}
                            >
                                <View style={styles.eventLeft}>
                                    {daysUntil !== null && (
                                        <View style={[
                                            styles.daysChip,
                                            daysUntil <= 3 && styles.daysChipUrgent,
                                        ]}>
                                            <Text style={[
                                                styles.daysText,
                                                daysUntil <= 3 && styles.daysTextUrgent,
                                            ]}>
                                                {daysUntil === 0 ? 'D-Day' : daysUntil > 0 ? `D-${daysUntil}` : `D+${Math.abs(daysUntil)}`}
                                            </Text>
                                        </View>
                                    )}
                                </View>
                                <View style={styles.eventContent}>
                                    <Text style={styles.eventName}>{event.event_name}</Text>
                                    <Text style={styles.eventDate}>
                                        {formatDate(event.event_date)} {event.event_time || ''}
                                    </Text>
                                    {event.child_tag && event.child_tag !== '없음' && (
                                        <View style={styles.childBadge}>
                                            <Text style={styles.childBadgeText}>👶 {event.child_tag}</Text>
                                        </View>
                                    )}
                                    {event.checklist_with_status && event.checklist_with_status.length > 0 && (
                                        <View style={styles.progressRow}>
                                            <View style={styles.progressBarBg}>
                                                <View
                                                    style={[
                                                        styles.progressBarFill,
                                                        {
                                                            width: `${(event.checklist_with_status.filter((i: any) => i.is_checked).length / event.checklist_with_status.length) * 100}%`,
                                                            backgroundColor: event.checklist_with_status.filter((i: any) => i.is_checked).length === event.checklist_with_status.length ? '#10B981' : '#F59E0B'
                                                        }
                                                    ]}
                                                />
                                            </View>
                                            <Text style={styles.progressText}>
                                                {event.checklist_with_status.filter((i: any) => i.is_checked).length}/{event.checklist_with_status.length}
                                            </Text>
                                        </View>
                                    )}
                                </View>
                                <TouchableOpacity
                                    style={styles.deleteButton}
                                    onPress={(e) => {
                                        e.stopPropagation();
                                        handleDeleteEvent(event.id);
                                    }}
                                >
                                    <Text style={styles.deleteButtonText}>🗑️</Text>
                                </TouchableOpacity>
                            </TouchableOpacity>
                        );
                    })
                )}
            </ScrollView>

            <TouchableOpacity
                style={styles.fab}
                onPress={() => navigation.navigate('Home')}
            >
                <Text style={styles.fabText}>+</Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F5F7FA',
    },
    header: {
        padding: 20,
        backgroundColor: '#fff',
        borderBottomWidth: 1,
        borderBottomColor: '#eee',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#1a1a2e',
    },
    subtitle: {
        fontSize: 14,
        color: '#666',
        marginTop: 4,
    },
    eventList: {
        flex: 1,
        padding: 16,
    },
    loadingText: {
        textAlign: 'center',
        color: '#666',
        marginTop: 40,
    },
    emptyState: {
        alignItems: 'center',
        marginTop: 60,
    },
    emptyIcon: {
        fontSize: 48,
        marginBottom: 16,
    },
    emptyText: {
        fontSize: 16,
        color: '#999',
        marginBottom: 20,
    },
    addButton: {
        backgroundColor: '#4ECDC4',
        paddingVertical: 12,
        paddingHorizontal: 24,
        borderRadius: 24,
    },
    addButtonText: {
        color: '#fff',
        fontWeight: 'bold',
    },
    eventCard: {
        backgroundColor: '#fff',
        borderRadius: 12,
        padding: 16,
        marginBottom: 12,
        flexDirection: 'row',
        alignItems: 'center',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 2,
    },
    eventLeft: {
        marginRight: 12,
    },
    daysChip: {
        backgroundColor: '#E8F6F3',
        paddingVertical: 6,
        paddingHorizontal: 10,
        borderRadius: 6,
    },
    daysChipUrgent: {
        backgroundColor: '#FFE8E8',
    },
    daysText: {
        fontSize: 12,
        fontWeight: 'bold',
        color: '#4ECDC4',
    },
    daysTextUrgent: {
        color: '#FF6B6B',
    },
    eventContent: {
        flex: 1,
    },
    eventName: {
        fontSize: 16,
        fontWeight: '600',
        color: '#333',
        marginBottom: 4,
    },
    eventDate: {
        fontSize: 14,
        color: '#666',
    },
    checklistCount: {
        fontSize: 12,
        color: '#4ECDC4',
        marginTop: 4,
    },
    childBadge: {
        backgroundColor: '#E8F0FE',
        paddingHorizontal: 8,
        paddingVertical: 2,
        borderRadius: 10,
        alignSelf: 'flex-start',
        marginTop: 4,
    },
    childBadgeText: {
        fontSize: 11,
        color: '#1967D2',
    },
    progressRow: {
        flexDirection: 'row',
        alignItems: 'center',
        marginTop: 6,
    },
    progressBarBg: {
        flex: 1,
        height: 6,
        backgroundColor: '#E5E7EB',
        borderRadius: 3,
        marginRight: 8,
    },
    progressBarFill: {
        height: 6,
        borderRadius: 3,
    },
    progressText: {
        fontSize: 11,
        color: '#6B7280',
        fontWeight: '600',
    },
    deleteButton: {
        padding: 8,
        marginLeft: 8,
    },
    deleteButtonText: {
        fontSize: 18,
    },
    fab: {
        position: 'absolute',
        bottom: 24,
        right: 24,
        width: 56,
        height: 56,
        borderRadius: 28,
        backgroundColor: '#4ECDC4',
        alignItems: 'center',
        justifyContent: 'center',
        shadowColor: '#4ECDC4',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.4,
        shadowRadius: 8,
        elevation: 6,
    },
    fabText: {
        fontSize: 28,
        color: '#fff',
        fontWeight: '300',
    },
});

export default DashboardScreen;
