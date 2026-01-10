# 개인정보 처리방침 (Privacy Policy)

**최종 수정일**: 2026년 1월 10일  
**시행일**: 2026년 1월 10일

---

## 1. 총칙

눈치코치(Sense Coach, 이하 "본 앱")는 사용자의 개인정보를 중요하게 생각하며, 개인정보 보호법, 정보통신망 이용촉진 및 정보보호 등에 관한 법률 등 관련 법령을 준수하고 있습니다.

본 개인정보 처리방침은 본 앱이 제공하는 서비스 이용 과정에서 수집·이용·제공되는 개인정보의 처리와 보호에 대해 안내합니다.

---

## 2. 수집하는 개인정보의 항목

### 2.1 필수 수집 항목
본 앱은 서비스 제공을 위해 다음과 같은 정보를 수집합니다:

#### 자동 수집 정보
- 기기 정보: OS 버전, 기기 모델명, 기기 식별자
- 로그 데이터: 접속 시간, 서비스 이용 기록, 오류 로그
- 쿠키 및 세션 정보

#### 사용자 입력 정보
- 학교 알림장 텍스트 (분석 요청 시)
- 업로드한 이미지 (분석 요청 시)
- 저장한 일정 정보 (행사명, 날짜, 준비물, 메모)
- 자녀 이름 (일정 관리를 위한 태그)
- 선택한 국가 정보

### 2.2 선택 수집 항목
- 없음

---

## 3. 개인정보의 수집 및 이용 목적

본 앱은 수집한 개인정보를 다음의 목적으로 이용합니다:

### 3.1 서비스 제공
- 학교 알림장 텍스트 및 이미지 분석
- AI 기반 번역 및 요약 제공
- 일정 및 준비물 체크리스트 생성
- 현지 문화 맥락 설명 제공

### 3.2 서비스 개선
- 서비스 품질 향상을 위한 통계 분석
- 오류 및 버그 수정
- 신규 기능 개발

### 3.3 사용자 지원
- 문의사항 응대
- 공지사항 전달

---

## 4. 개인정보의 보유 및 이용 기간

### 4.1 일반 원칙
본 앱은 개인정보의 수집 및 이용 목적이 달성된 후에는 해당 정보를 지체 없이 파기합니다.

### 4.2 구체적 보유 기간

#### 로컬 저장 데이터
- **저장된 일정 정보**: 사용자가 직접 삭제할 때까지
- **설정 정보** (선택 국가, 자녀 이름): 앱 삭제 시까지
- **저장 위치**: 사용자 기기 내 SQLite 데이터베이스

#### API 처리 데이터
- **분석 요청 데이터**: Google Gemini API로 전송 후 즉시 삭제
- **API 응답 데이터**: 화면 표시 후 세션 종료 시 삭제

#### 로그 데이터
- **오류 로그**: 90일 보관 후 자동 삭제
- **접속 로그**: 수집하지 않음

---

## 5. 개인정보의 제3자 제공

### 5.1 제공하는 정보
본 앱은 사용자의 개인정보를 다음과 같이 제3자에게 제공합니다:

| 제공받는 자 | 제공 목적 | 제공 항목 | 보유 및 이용 기간 |
|------------|----------|----------|-----------------|
| Google LLC | AI 분석 서비스 제공 (Gemini API) | 학교 알림장 텍스트, 업로드한 이미지 | 처리 즉시 삭제 (Google 정책에 따름) |

### 5.2 Google Gemini API 개인정보 처리
- Google Gemini API는 사용자가 입력한 텍스트와 이미지를 분석합니다
- Google은 API 요청 데이터를 모델 학습에 사용하지 않습니다 (Google Cloud API 정책)
- 자세한 내용: [Google Privacy Policy](https://policies.google.com/privacy)

### 5.3 기타 제3자 제공
위에 명시된 경우를 제외하고, 본 앱은 사용자의 동의 없이 개인정보를 제3자에게 제공하지 않습니다.

---

## 6. 개인정보의 처리 위탁

본 앱은 서비스 제공을 위해 다음과 같이 개인정보 처리를 위탁하고 있습니다:

| 수탁업체 | 위탁 업무 내용 | 위탁 기간 |
|---------|--------------|----------|
| Streamlit Cloud (Snowflake Inc.) | 앱 호스팅 및 서버 운영 | 서비스 제공 기간 동안 |
| Google Cloud Platform | API 서비스 제공 | 서비스 제공 기간 동안 |

위탁업체가 변경될 경우, 본 개인정보 처리방침을 통해 공지하겠습니다.

---

## 7. 정보주체의 권리·의무 및 행사 방법

사용자는 다음과 같은 권리를 행사할 수 있습니다:

### 7.1 개인정보 열람 요구
- 앱 내에서 저장된 일정 확인 가능

### 7.2 개인정보 정정·삭제 요구
- 앱 내에서 일정 수정 및 삭제 가능
- 자녀 이름 수정 및 삭제 가능

### 7.3 개인정보 처리 정지 요구
- 앱 사용 중지 시 데이터 처리 정지

### 7.4 개인정보 파기 요구
- 앱 삭제 시 모든 로컬 데이터 자동 삭제

### 7.5 권리 행사 방법
- 앱 내 설정 메뉴에서 직접 수정/삭제
- 이메일 문의: [support@sensecoach.app] (실제 이메일로 변경 필요)

---

## 8. 개인정보의 파기 절차 및 방법

### 8.1 파기 절차
- 사용자가 삭제 요청한 데이터는 즉시 파기
- 목적 달성 후 보유 기간이 경과한 데이터는 자동 파기

### 8.2 파기 방법
- **전자파일**: 복구 불가능한 방법으로 영구 삭제
- **로컬 데이터베이스**: SQLite 데이터베이스에서 레코드 삭제
- **로그 파일**: 90일 경과 후 자동 삭제

---

## 9. 개인정보 보호를 위한 기술적·관리적 대책

### 9.1 기술적 대책
- **데이터 암호화**: HTTPS를 통한 통신 암호화
- **로컬 저장**: 민감 정보는 사용자 기기에만 저장
- **API 보안**: API 키는 환경 변수로 관리, 코드에 노출하지 않음
- **세션 관리**: 세션 타임아웃 적용

### 9.2 관리적 대책
- **최소 수집 원칙**: 서비스 제공에 필요한 최소한의 정보만 수집
- **접근 권한 관리**: 개발자 계정 접근 권한 제한
- **정기 점검**: 보안 취약점 정기 점검 및 업데이트

---

## 10. 개인정보 보호책임자 및 담당자

본 앱의 개인정보 처리에 관한 문의는 아래로 연락주시기 바랍니다:

### 개인정보 보호책임자
- **이름**: [책임자 이름]
- **직책**: [직책]
- **이메일**: [support@sensecoach.app] (실제 이메일로 변경 필요)

### 개인정보 보호담당자
- **이름**: [담당자 이름]
- **이메일**: [privacy@sensecoach.app] (실제 이메일로 변경 필요)

---

## 11. 개인정보 처리방침의 변경

본 개인정보 처리방침은 법령, 정책 또는 서비스의 변경에 따라 변경될 수 있으며, 변경 시 앱 내 공지사항을 통해 고지합니다.

### 공고 일자
- **최초 공고일**: 2026년 1월 10일
- **최종 수정일**: 2026년 1월 10일
- **시행일**: 2026년 1월 10일

---

## 12. 아동의 개인정보 보호

본 앱은 만 14세 미만 아동의 개인정보를 수집하지 않습니다. 서비스는 학부모(성인)를 대상으로 제공됩니다.

---

## 13. 추가 정보

### 13.1 쿠키 사용
본 앱은 세션 유지를 위해 쿠키를 사용할 수 있습니다. 사용자는 웹 브라우저 설정을 통해 쿠키를 차단할 수 있으나, 일부 기능이 제한될 수 있습니다.

### 13.2 링크된 웹사이트
본 앱은 외부 웹사이트로의 링크를 포함할 수 있으며, 해당 웹사이트의 개인정보 보호정책은 본 정책과 무관합니다.

### 13.3 분쟁 해결
개인정보 침해에 대한 신고나 상담이 필요하신 경우:
- 개인정보 침해신고센터: (국번 없이) 118
- 개인정보 분쟁조정위원회: 1833-6972
- 대검찰청 사이버수사과: (국번 없이) 1301
- 경찰청 사이버안전국: (국번 없이) 182

---

## 14. 언어
본 개인정보 처리방침은 한국어를 정본으로 합니다.

---

**연락처**  
이메일: [support@sensecoach.app]  
웹사이트: [https://sensecoach.app]

---

# Privacy Policy (English)

**Last Updated**: January 10, 2026  
**Effective Date**: January 10, 2026

---

## 1. Overview

Sense Coach ("the App") values your privacy and complies with relevant laws including the Personal Information Protection Act and the Act on Promotion of Information and Communications Network Utilization and Information Protection.

This Privacy Policy describes how we collect, use, and protect your personal information when you use our services.

---

## 2. Information We Collect

### 2.1 Required Information

#### Automatically Collected
- Device information: OS version, device model, device identifiers
- Log data: access time, service usage records, error logs
- Cookies and session information

#### User-Provided Information
- School notice text (when requesting analysis)
- Uploaded images (when requesting analysis)
- Saved schedule information (event name, date, items, notes)
- Children's names (for schedule tags)
- Selected country information

### 2.2 Optional Information
- None

---

## 3. Purpose of Collection and Use

We use collected information for the following purposes:

### 3.1 Service Provision
- Analysis of school notice text and images
- AI-based translation and summary
- Schedule and checklist creation
- Local cultural context explanation

### 3.2 Service Improvement
- Statistical analysis for quality improvement
- Error and bug fixes
- New feature development

### 3.3 User Support
- Customer inquiry response
- Announcement delivery

---

## 4. Retention and Use Period

### 4.1 General Principle
We delete personal information promptly after achieving the purpose of collection and use.

### 4.2 Specific Retention Periods

#### Locally Stored Data
- **Saved schedules**: Until user deletes
- **Settings** (selected country, children's names): Until app deletion
- **Storage location**: SQLite database on user's device

#### API Processing Data
- **Analysis request data**: Deleted immediately after sending to Google Gemini API
- **API response data**: Deleted when session ends after display

#### Log Data
- **Error logs**: Automatically deleted after 90 days
- **Access logs**: Not collected

---

## 5. Third-Party Data Sharing

### 5.1 Shared Information

| Recipient | Purpose | Information Shared | Retention Period |
|-----------|---------|-------------------|-----------------|
| Google LLC | AI analysis service (Gemini API) | School notice text, uploaded images | Deleted immediately after processing (per Google policy) |

### 5.2 Google Gemini API Privacy
- Google Gemini API analyzes user-provided text and images
- Google does not use API request data for model training (Google Cloud API policy)
- Details: [Google Privacy Policy](https://policies.google.com/privacy)

### 5.3 Other Third-Party Sharing
Except as specified above, we do not share your personal information with third parties without your consent.

---

## 6. Data Processing Outsourcing

We outsource personal information processing as follows:

| Contractor | Outsourced Tasks | Duration |
|------------|------------------|----------|
| Streamlit Cloud (Snowflake Inc.) | App hosting and server operation | During service provision |
| Google Cloud Platform | API service provision | During service provision |

We will notify through this Privacy Policy if contractors change.

---

## 7. Your Rights and How to Exercise Them

You can exercise the following rights:

### 7.1 Request to View Personal Information
- View saved schedules within the app

### 7.2 Request to Correct/Delete Personal Information
- Edit and delete schedules within the app
- Edit and delete children's names

### 7.3 Request to Stop Personal Information Processing
- Data processing stops when you stop using the app

### 7.4 Request to Destroy Personal Information
- All local data automatically deleted when app is uninstalled

### 7.5 How to Exercise Rights
- Directly edit/delete in app settings menu
- Email inquiry: [support@sensecoach.app] (please update with actual email)

---

## 8. Data Destruction Procedures and Methods

### 8.1 Destruction Procedures
- Data requested for deletion by users is destroyed immediately
- Data past retention period after purpose achievement is automatically destroyed

### 8.2 Destruction Methods
- **Electronic files**: Permanently deleted in an unrecoverable manner
- **Local database**: Records deleted from SQLite database
- **Log files**: Automatically deleted after 90 days

---

## 9. Technical and Administrative Security Measures

### 9.1 Technical Measures
- **Data encryption**: Communication encryption via HTTPS
- **Local storage**: Sensitive information stored only on user's device
- **API security**: API keys managed as environment variables, not exposed in code
- **Session management**: Session timeout applied

### 9.2 Administrative Measures
- **Minimum collection principle**: Collect only minimum information necessary for service provision
- **Access control**: Restricted developer account access
- **Regular inspections**: Regular security vulnerability checks and updates

---

## 10. Privacy Officer and Contact

For inquiries about personal information processing:

### Privacy Officer
- **Name**: [Officer Name]
- **Title**: [Title]
- **Email**: [support@sensecoach.app] (please update with actual email)

### Privacy Manager
- **Name**: [Manager Name]
- **Email**: [privacy@sensecoach.app] (please update with actual email)

---

## 11. Changes to Privacy Policy

This Privacy Policy may change according to laws, policies, or service changes. Changes will be announced through in-app notifications.

### Announcement Dates
- **Initial announcement**: January 10, 2026
- **Last updated**: January 10, 2026
- **Effective date**: January 10, 2026

---

## 12. Children's Privacy

This app does not collect personal information from children under 14 years old. The service is provided for parents (adults).

---

## 13. Additional Information

### 13.1 Cookie Use
The app may use cookies for session maintenance. Users can block cookies through web browser settings, but some features may be limited.

### 13.2 Linked Websites
The app may contain links to external websites. Their privacy policies are independent of this policy.

### 13.3 Dispute Resolution
For reports or consultations regarding personal information violations:
- Personal Information Infringement Report Center: 118 (Korea)
- Personal Information Dispute Mediation Committee: 1833-6972 (Korea)
- Supreme Prosecutors' Office Cyber Investigation Division: 1301 (Korea)
- National Police Agency Cyber Safety Bureau: 182 (Korea)

---

## 14. Language
The Korean version of this Privacy Policy is the authoritative text.

---

**Contact**  
Email: [support@sensecoach.app]  
Website: [https://sensecoach.app]
