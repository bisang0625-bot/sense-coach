import React, { useState } from 'react';
import {
    View,
    Text,
    TextInput,
    TouchableOpacity,
    StyleSheet,
    ScrollView,
    ActivityIndicator,
    Alert,
    KeyboardAvoidingView,
    Platform,
    Image,
} from 'react-native';
import { launchImageLibrary, launchCamera } from 'react-native-image-picker';
import { analyzeNotice, analyzeImage } from '../services/api';

const COUNTRIES = ['네덜란드', '미국', '독일', '영국', '기타'];

interface HomeScreenProps {
    navigation: any;
}

const HomeScreen: React.FC<HomeScreenProps> = ({ navigation }) => {
    const [text, setText] = useState('');
    const [country, setCountry] = useState('네덜란드');
    const [loading, setLoading] = useState(false);
    const [selectedImage, setSelectedImage] = useState<string | null>(null);

    const handleSelectImage = () => {
        Alert.alert(
            '이미지 선택',
            '어디서 이미지를 가져올까요?',
            [
                {
                    text: '📷 카메라',
                    onPress: () => {
                        launchCamera(
                            {
                                mediaType: 'photo',
                                quality: 0.8,
                                maxWidth: 1200,
                                maxHeight: 1200,
                            },
                            (response) => {
                                if (response.assets && response.assets[0]?.uri) {
                                    setSelectedImage(response.assets[0].uri);
                                }
                            }
                        );
                    },
                },
                {
                    text: '🖼️ 갤러리',
                    onPress: () => {
                        launchImageLibrary(
                            {
                                mediaType: 'photo',
                                quality: 0.8,
                                maxWidth: 1200,
                                maxHeight: 1200,
                            },
                            (response) => {
                                if (response.assets && response.assets[0]?.uri) {
                                    setSelectedImage(response.assets[0].uri);
                                }
                            }
                        );
                    },
                },
                { text: '취소', style: 'cancel' },
            ]
        );
    };

    const handleClearImage = () => {
        setSelectedImage(null);
    };

    const handleAnalyze = async () => {
        if (!text.trim() && !selectedImage) {
            Alert.alert('알림', '분석할 내용을 입력하거나 이미지를 선택해주세요.');
            return;
        }

        setLoading(true);
        try {
            const userId = 'temp-user-001';
            let result;

            if (selectedImage) {
                // 이미지 분석 (텍스트가 있으면 함께 전송)
                result = await analyzeImage(selectedImage, country, userId, text);
            } else {
                // 텍스트만 분석
                result = await analyzeNotice(text, country, userId);
            }

            navigation.navigate('Result', {
                result: result,
                country: country,
            });
        } catch (error: any) {
            console.error(error);
            Alert.alert('오류', error.response?.data?.detail || '분석 중 오류가 발생했습니다.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <KeyboardAvoidingView
            style={styles.container}
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        >
            <ScrollView contentContainerStyle={styles.scrollContent}>
                <View style={styles.header}>
                    <Text style={styles.title}>🎒 알림장 분석</Text>
                    <Text style={styles.subtitle}>학교 알림장을 붙여넣거나 사진을 찍어주세요</Text>
                </View>

                {/* 국가 선택 */}
                <View style={styles.countryContainer}>
                    <Text style={styles.label}>거주 국가</Text>
                    <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                        {COUNTRIES.map((c) => (
                            <TouchableOpacity
                                key={c}
                                style={[
                                    styles.countryChip,
                                    country === c && styles.countryChipSelected,
                                ]}
                                onPress={() => setCountry(c)}
                            >
                                <Text style={[
                                    styles.countryChipText,
                                    country === c && styles.countryChipTextSelected,
                                ]}>
                                    {c}
                                </Text>
                            </TouchableOpacity>
                        ))}
                    </ScrollView>
                </View>

                {/* 이미지 업로드 */}
                <View style={styles.imageSection}>
                    <Text style={styles.label}>📷 이미지로 분석 (선택)</Text>

                    {selectedImage ? (
                        <View style={styles.imagePreviewContainer}>
                            <Image source={{ uri: selectedImage }} style={styles.imagePreview} />
                            <TouchableOpacity style={styles.removeImageButton} onPress={handleClearImage}>
                                <Text style={styles.removeImageText}>✕</Text>
                            </TouchableOpacity>
                        </View>
                    ) : (
                        <TouchableOpacity style={styles.imageUploadButton} onPress={handleSelectImage}>
                            <Text style={styles.imageUploadIcon}>📷</Text>
                            <Text style={styles.imageUploadText}>알림장 사진 추가</Text>
                            <Text style={styles.imageUploadHint}>카메라로 찍거나 갤러리에서 선택</Text>
                        </TouchableOpacity>
                    )}
                </View>

                {/* 텍스트 입력 */}
                <View style={styles.inputContainer}>
                    <Text style={styles.label}>✏️ 알림장 내용 (선택)</Text>
                    <TextInput
                        style={styles.textInput}
                        multiline
                        numberOfLines={6}
                        placeholder="학교에서 받은 알림장 내용을 여기에 붙여넣으세요..."
                        placeholderTextColor="#999"
                        value={text}
                        onChangeText={setText}
                        textAlignVertical="top"
                        autoCorrect={false}
                        autoCapitalize="none"
                    />
                </View>

                {/* 분석 버튼 */}
                <TouchableOpacity
                    style={[styles.analyzeButton, loading && styles.analyzeButtonDisabled]}
                    onPress={handleAnalyze}
                    disabled={loading}
                >
                    {loading ? (
                        <ActivityIndicator color="#fff" />
                    ) : (
                        <Text style={styles.analyzeButtonText}>✨ AI 분석하기</Text>
                    )}
                </TouchableOpacity>

                {/* 하단 네비게이션 */}
                <View style={styles.bottomLinks}>
                    <TouchableOpacity
                        style={styles.bottomLink}
                        onPress={() => navigation.navigate('Dashboard')}
                    >
                        <Text style={styles.bottomLinkText}>📅 저장된 일정</Text>
                    </TouchableOpacity>

                    <TouchableOpacity
                        style={styles.bottomLink}
                        onPress={() => navigation.navigate('Settings')}
                    >
                        <Text style={styles.bottomLinkText}>⚙️ 설정</Text>
                    </TouchableOpacity>
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F5F7FA',
    },
    scrollContent: {
        padding: 20,
    },
    header: {
        marginBottom: 24,
        alignItems: 'center',
    },
    title: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#1a1a2e',
        marginBottom: 8,
    },
    subtitle: {
        fontSize: 15,
        color: '#666',
        textAlign: 'center',
    },
    label: {
        fontSize: 14,
        fontWeight: '600',
        color: '#333',
        marginBottom: 8,
    },
    countryContainer: {
        marginBottom: 20,
    },
    countryChip: {
        paddingHorizontal: 16,
        paddingVertical: 8,
        borderRadius: 20,
        backgroundColor: '#fff',
        marginRight: 8,
        borderWidth: 1,
        borderColor: '#ddd',
    },
    countryChipSelected: {
        backgroundColor: '#4ECDC4',
        borderColor: '#4ECDC4',
    },
    countryChipText: {
        color: '#666',
        fontWeight: '500',
    },
    countryChipTextSelected: {
        color: '#fff',
    },
    imageSection: {
        marginBottom: 20,
    },
    imageUploadButton: {
        backgroundColor: '#fff',
        borderRadius: 12,
        padding: 24,
        alignItems: 'center',
        borderWidth: 2,
        borderColor: '#ddd',
        borderStyle: 'dashed',
    },
    imageUploadIcon: {
        fontSize: 36,
        marginBottom: 8,
    },
    imageUploadText: {
        fontSize: 16,
        fontWeight: '600',
        color: '#333',
        marginBottom: 4,
    },
    imageUploadHint: {
        fontSize: 13,
        color: '#888',
    },
    imagePreviewContainer: {
        position: 'relative',
    },
    imagePreview: {
        width: '100%',
        height: 200,
        borderRadius: 12,
        backgroundColor: '#eee',
    },
    removeImageButton: {
        position: 'absolute',
        top: 8,
        right: 8,
        backgroundColor: 'rgba(0,0,0,0.6)',
        width: 28,
        height: 28,
        borderRadius: 14,
        alignItems: 'center',
        justifyContent: 'center',
    },
    removeImageText: {
        color: '#fff',
        fontSize: 16,
        fontWeight: 'bold',
    },
    inputContainer: {
        marginBottom: 20,
    },
    textInput: {
        backgroundColor: '#fff',
        borderRadius: 12,
        padding: 16,
        fontSize: 16,
        minHeight: 140,
        borderWidth: 1,
        borderColor: '#e0e0e0',
        color: '#333',
    },
    analyzeButton: {
        backgroundColor: '#4ECDC4',
        paddingVertical: 16,
        borderRadius: 12,
        alignItems: 'center',
        shadowColor: '#4ECDC4',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
        elevation: 4,
    },
    analyzeButtonDisabled: {
        opacity: 0.7,
    },
    analyzeButtonText: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
    },
    dashboardLink: {
        marginTop: 20,
        alignItems: 'center',
        padding: 12,
    },
    dashboardLinkText: {
        color: '#4ECDC4',
        fontSize: 16,
        fontWeight: '500',
    },
    bottomLinks: {
        flexDirection: 'row',
        justifyContent: 'center',
        marginTop: 20,
        gap: 16,
    },
    bottomLink: {
        padding: 12,
    },
    bottomLinkText: {
        color: '#4ECDC4',
        fontSize: 16,
        fontWeight: '500',
    },
});

export default HomeScreen;
