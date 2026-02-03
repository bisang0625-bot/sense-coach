import React, { useState, useEffect, useCallback } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    TextInput,
    Alert,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { getChildren, addChild, deleteChild } from '../services/api';

interface SettingsScreenProps {
    navigation: any;
}

const SettingsScreen: React.FC<SettingsScreenProps> = ({ navigation }) => {
    const [children, setChildren] = useState<string[]>([]);
    const [newChildName, setNewChildName] = useState('');
    const [loading, setLoading] = useState(false);

    const fetchChildren = async () => {
        try {
            const data = await getChildren();
            setChildren(data.children || []);
        } catch (error) {
            console.error('Failed to fetch children:', error);
        }
    };

    useFocusEffect(
        useCallback(() => {
            fetchChildren();
        }, [])
    );

    const handleAddChild = async () => {
        if (!newChildName.trim()) {
            Alert.alert('알림', '아이 이름을 입력해주세요.');
            return;
        }

        setLoading(true);
        try {
            await addChild(newChildName.trim());
            setNewChildName('');
            fetchChildren();
            Alert.alert('성공', `'${newChildName.trim()}'이(가) 추가되었습니다!`);
        } catch (error: any) {
            Alert.alert('오류', error.response?.data?.detail || '추가 중 오류가 발생했습니다.');
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteChild = (childName: string) => {
        Alert.alert(
            '삭제 확인',
            `'${childName}'을(를) 삭제하시겠습니까?`,
            [
                { text: '취소', style: 'cancel' },
                {
                    text: '삭제',
                    style: 'destructive',
                    onPress: async () => {
                        try {
                            await deleteChild(childName);
                            fetchChildren();
                        } catch (error) {
                            Alert.alert('오류', '삭제 중 오류가 발생했습니다.');
                        }
                    },
                },
            ]
        );
    };

    return (
        <ScrollView style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>⚙️ 설정</Text>
            </View>

            {/* 아이 관리 섹션 */}
            <View style={styles.section}>
                <Text style={styles.sectionTitle}>👶 아이 관리</Text>
                <Text style={styles.sectionDesc}>
                    아이를 등록하면 일정에 아이별 태그를 붙일 수 있습니다.
                </Text>

                {/* 아이 목록 */}
                {children.length > 0 ? (
                    <View style={styles.childList}>
                        {children.map((child, index) => (
                            <View key={index} style={styles.childItem}>
                                <Text style={styles.childName}>{child}</Text>
                                <TouchableOpacity
                                    style={styles.deleteButton}
                                    onPress={() => handleDeleteChild(child)}
                                >
                                    <Text style={styles.deleteButtonText}>🗑️</Text>
                                </TouchableOpacity>
                            </View>
                        ))}
                    </View>
                ) : (
                    <Text style={styles.emptyText}>등록된 아이가 없습니다.</Text>
                )}

                {/* 아이 추가 */}
                <View style={styles.addChildContainer}>
                    <TextInput
                        style={styles.input}
                        placeholder="아이 이름 (예: 첫째, 민수)"
                        placeholderTextColor="#999"
                        value={newChildName}
                        onChangeText={setNewChildName}
                        autoCorrect={false}
                        autoCapitalize="none"
                    />
                    <TouchableOpacity
                        style={[styles.addButton, loading && styles.addButtonDisabled]}
                        onPress={handleAddChild}
                        disabled={loading}
                    >
                        <Text style={styles.addButtonText}>➕ 추가</Text>
                    </TouchableOpacity>
                </View>
            </View>

            {/* 데이터 관리 섹션 */}
            <View style={styles.section}>
                <Text style={styles.sectionTitle}>⚠️ 데이터 관리</Text>
                <TouchableOpacity
                    style={styles.dangerButton}
                    onPress={() => {
                        Alert.alert(
                            '경고',
                            '모든 일정과 아이 정보가 영구적으로 삭제됩니다. 계속하시겠습니까?',
                            [
                                { text: '취소', style: 'cancel' },
                                {
                                    text: '초기화',
                                    style: 'destructive',
                                    onPress: async () => {
                                        // TODO: 데이터 초기화 API 호출
                                        Alert.alert('알림', '데이터 초기화 기능은 곧 추가됩니다.');
                                    },
                                },
                            ]
                        );
                    }}
                >
                    <Text style={styles.dangerButtonText}>🚨 모든 데이터 초기화</Text>
                </TouchableOpacity>
            </View>

            {/* 앱 정보 */}
            <View style={styles.footer}>
                <Text style={styles.footerText}>© 2026 눈치코치 알림장 (Sense Coach)</Text>
                <Text style={styles.footerText}>문의: vennaper@gmail.com</Text>
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F5F7FA',
    },
    header: {
        padding: 20,
        paddingBottom: 10,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#1a1a2e',
    },
    section: {
        backgroundColor: '#fff',
        margin: 16,
        borderRadius: 12,
        padding: 16,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 2,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: '600',
        color: '#333',
        marginBottom: 8,
    },
    sectionDesc: {
        fontSize: 14,
        color: '#666',
        marginBottom: 16,
    },
    childList: {
        marginBottom: 16,
    },
    childItem: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        backgroundColor: '#f8f9fa',
        padding: 12,
        borderRadius: 8,
        marginBottom: 8,
    },
    childName: {
        fontSize: 16,
        fontWeight: '500',
        color: '#333',
    },
    deleteButton: {
        padding: 4,
    },
    deleteButtonText: {
        fontSize: 18,
    },
    emptyText: {
        color: '#999',
        textAlign: 'center',
        marginVertical: 16,
    },
    addChildContainer: {
        flexDirection: 'row',
        gap: 8,
    },
    input: {
        flex: 1,
        backgroundColor: '#f8f9fa',
        borderRadius: 8,
        padding: 12,
        fontSize: 16,
        borderWidth: 1,
        borderColor: '#e0e0e0',
    },
    addButton: {
        backgroundColor: '#4ECDC4',
        paddingHorizontal: 16,
        borderRadius: 8,
        justifyContent: 'center',
    },
    addButtonDisabled: {
        opacity: 0.6,
    },
    addButtonText: {
        color: '#fff',
        fontWeight: 'bold',
    },
    dangerButton: {
        backgroundColor: '#fff3f3',
        padding: 14,
        borderRadius: 8,
        borderWidth: 1,
        borderColor: '#ffcccc',
        alignItems: 'center',
    },
    dangerButtonText: {
        color: '#cc0000',
        fontWeight: '500',
    },
    footer: {
        padding: 20,
        alignItems: 'center',
    },
    footerText: {
        fontSize: 12,
        color: '#999',
        marginBottom: 4,
    },
});

export default SettingsScreen;
