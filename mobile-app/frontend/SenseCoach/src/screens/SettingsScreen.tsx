import React, { useState, useEffect, useCallback } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    TextInput,
    Alert,
    ActivityIndicator,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { getChildren, addChild, deleteChild } from '../services/api';

interface SettingsScreenProps {
    navigation: any;
}

const SettingsScreen: React.FC<SettingsScreenProps> = ({ navigation }) => {
    const [children, setChildren] = useState<string[]>([]);
    const [newChildName, setNewChildName] = useState('');
    const [loading, setLoading] = useState(true);

    const fetchChildren = async () => {
        try {
            const data = await getChildren();
            setChildren(data.children || []);
        } catch (error) {
            console.error('Failed to fetch children:', error);
        } finally {
            setLoading(false);
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
        try {
            await addChild(newChildName.trim());
            setNewChildName('');
            fetchChildren();
            Alert.alert('성공', `'${newChildName.trim()}'이(가) 추가되었습니다!`);
        } catch (error: any) {
            if (error.response?.status === 400) {
                Alert.alert('알림', '이미 등록된 이름입니다.');
            } else {
                Alert.alert('오류', '아이 추가에 실패했습니다.');
            }
        }
    };

    const handleDeleteChild = (name: string) => {
        Alert.alert(
            '삭제 확인',
            `'${name}'을(를) 삭제하시겠습니까?`,
            [
                { text: '취소', style: 'cancel' },
                {
                    text: '삭제',
                    style: 'destructive',
                    onPress: async () => {
                        try {
                            await deleteChild(name);
                            fetchChildren();
                        } catch (error) {
                            Alert.alert('오류', '삭제에 실패했습니다.');
                        }
                    },
                },
            ]
        );
    };

    return (
        <ScrollView style={styles.container}>
            {/* 아이 관리 섹션 */}
            <View style={styles.section}>
                <Text style={styles.sectionTitle}>👶 아이 관리</Text>
                <Text style={styles.sectionDescription}>
                    등록된 아이를 일정에 태그할 수 있습니다.
                </Text>

                {loading ? (
                    <ActivityIndicator color="#4ECDC4" />
                ) : children.length === 0 ? (
                    <View style={styles.emptyState}>
                        <Text style={styles.emptyText}>등록된 아이가 없습니다.</Text>
                    </View>
                ) : (
                    <View style={styles.childList}>
                        {children.map((child) => (
                            <View key={child} style={styles.childItem}>
                                <Text style={styles.childName}>{child}</Text>
                                <TouchableOpacity
                                    style={styles.deleteChildButton}
                                    onPress={() => handleDeleteChild(child)}
                                >
                                    <Text style={styles.deleteChildText}>🗑️</Text>
                                </TouchableOpacity>
                            </View>
                        ))}
                    </View>
                )}

                {/* 아이 추가 */}
                <View style={styles.addChildRow}>
                    <TextInput
                        style={styles.addChildInput}
                        value={newChildName}
                        onChangeText={setNewChildName}
                        placeholder="아이 이름 입력"
                        autoCorrect={false}
                        returnKeyType="done"
                        onSubmitEditing={handleAddChild}
                    />
                    <TouchableOpacity style={styles.addChildButton} onPress={handleAddChild}>
                        <Text style={styles.addChildButtonText}>+ 추가</Text>
                    </TouchableOpacity>
                </View>
            </View>

            {/* 앱 정보 섹션 */}
            <View style={styles.section}>
                <Text style={styles.sectionTitle}>ℹ️ 앱 정보</Text>
                <View style={styles.infoRow}>
                    <Text style={styles.infoLabel}>버전</Text>
                    <Text style={styles.infoValue}>1.0.0</Text>
                </View>
                <View style={styles.infoRow}>
                    <Text style={styles.infoLabel}>개발자</Text>
                    <Text style={styles.infoValue}>눈치코치 팀</Text>
                </View>
            </View>

            {/* 법적 고지 */}
            <View style={styles.section}>
                <Text style={styles.sectionTitle}>📋 법적 고지</Text>
                <TouchableOpacity style={styles.linkRow}>
                    <Text style={styles.linkText}>개인정보 처리방침</Text>
                    <Text style={styles.linkArrow}>→</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.linkRow}>
                    <Text style={styles.linkText}>이용약관</Text>
                    <Text style={styles.linkArrow}>→</Text>
                </TouchableOpacity>
            </View>

            <View style={{ height: 40 }} />
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F5F7FA',
    },
    section: {
        backgroundColor: '#fff',
        marginHorizontal: 16,
        marginTop: 16,
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
        marginBottom: 8,
    },
    sectionDescription: {
        fontSize: 14,
        color: '#666',
        marginBottom: 16,
    },
    emptyState: {
        padding: 20,
        alignItems: 'center',
    },
    emptyText: {
        color: '#999',
        fontSize: 14,
    },
    childList: {
        marginBottom: 16,
    },
    childItem: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        backgroundColor: '#F8F9FA',
        padding: 12,
        borderRadius: 10,
        marginBottom: 8,
    },
    childName: {
        fontSize: 16,
        color: '#333',
        fontWeight: '500',
    },
    deleteChildButton: {
        padding: 8,
    },
    deleteChildText: {
        fontSize: 18,
    },
    addChildRow: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    addChildInput: {
        flex: 1,
        backgroundColor: '#F8F9FA',
        borderRadius: 10,
        padding: 12,
        fontSize: 15,
        marginRight: 8,
        borderWidth: 1,
        borderColor: '#E0E0E0',
    },
    addChildButton: {
        backgroundColor: '#4ECDC4',
        paddingVertical: 12,
        paddingHorizontal: 16,
        borderRadius: 10,
    },
    addChildButtonText: {
        color: '#fff',
        fontWeight: 'bold',
    },
    infoRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        paddingVertical: 10,
        borderBottomWidth: 1,
        borderBottomColor: '#F0F0F0',
    },
    infoLabel: {
        fontSize: 15,
        color: '#666',
    },
    infoValue: {
        fontSize: 15,
        color: '#333',
        fontWeight: '500',
    },
    linkRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        paddingVertical: 12,
        borderBottomWidth: 1,
        borderBottomColor: '#F0F0F0',
    },
    linkText: {
        fontSize: 15,
        color: '#4ECDC4',
    },
    linkArrow: {
        fontSize: 15,
        color: '#999',
    },
});

export default SettingsScreen;
