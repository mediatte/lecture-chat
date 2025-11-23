# 🚀 Streamlit Cloud 배포 가이드

완전 무료! 5분이면 배포 완료!

## 🎯 왜 Streamlit Cloud?

**완벽한 선택:**
- ✅ **완전 무료** - 카드 등록 불필요
- ✅ **무제한 사용** - 시간 제한 없음
- ✅ **자동 배포** - GitHub push만 하면 끝
- ✅ **HTTPS 자동** - 보안 걱정 없음
- ✅ **Python 전용** - 최적화됨

**Railway/Render와 비교:**
| 항목 | Streamlit Cloud | Railway | Render |
|------|----------------|---------|--------|
| **무료 시간** | ♾️ 무제한 | 500h | 750h |
| **Python 지원** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **배포 속도** | ⚡ 5분 | 10분 | 10분 |
| **설정 난이도** | ⭐ 쉬움 | ⭐⭐ | ⭐⭐ |

---

## 🚀 5분 배포

### 1단계: GitHub 저장소 만들기 (1분)

**방법 A: 웹사이트 (추천)**

1. **GitHub 접속**
   ```
   https://github.com/new
   ```

2. **저장소 설정**
   ```
   Repository name: lecture-chat-streamlit
   Description: 강의 실시간 채팅 (Streamlit)
   Public ✅
   Create repository
   ```

3. **파일 업로드**
   ```
   "uploading an existing file" 클릭
   
   streamlit-app 폴더의 모든 파일 드래그:
   - app.py
   - requirements.txt
   - .streamlit/config.toml
   - .streamlit/secrets.toml.example
   - README.md
   
   "Commit changes" 클릭
   ```

**방법 B: 터미널**

```bash
cd ~/Library/CloudStorage/OneDrive-고운고등학교/PROJECTS/websocket_sidebar/streamlit-app

git init
git add .
git commit -m "Streamlit 채팅 앱 초기 버전"
git remote add origin https://github.com/사용자명/lecture-chat-streamlit.git
git branch -M main
git push -u origin main
```

### 2단계: Streamlit Cloud 배포 (3분)

1. **Streamlit Cloud 접속**
   ```
   https://streamlit.io/cloud
   ```

2. **Sign Up / Login**
   ```
   "Sign up" 클릭
   → "Continue with GitHub" 선택
   → 권한 승인
   ```

3. **New app 생성**
   ```
   "New app" 클릭 (우측 상단)
   ```

4. **앱 설정**
   ```
   Repository: lecture-chat-streamlit
   Branch: main
   Main file path: app.py
   
   App URL (선택):
   your-app-name.streamlit.app
   ```

5. **Deploy! 클릭**
   ```
   "Deploy!" 버튼 클릭
   자동 배포 시작!
   ```

### 3단계: 배포 완료 대기 (1-2분)

**진행 상황:**
```
Installing dependencies...
Running app...
✅ Your app is live!
```

**URL 확인:**
```
https://your-app-name.streamlit.app
```

### 4단계: Secrets 설정 (선택)

**Streamlit Cloud Dashboard:**
```
앱 선택 → ⚙️ Settings 클릭
→ "Secrets" 탭
→ 다음 입력:

APP_URL = "https://your-app-name.streamlit.app"

"Save" 클릭
```

---

## 🎉 완료!

**이제 사용 가능:**

```
1. https://your-app-name.streamlit.app 접속
2. "강사로 시작" 클릭
3. "새 세션 시작" 클릭
4. QR 코드 공유
5. 학생들 접속!
```

---

## 📱 실제 사용 워크플로우

### 강의 전 (1분)

```
1. 앱 접속: https://your-app-name.streamlit.app
2. "강사로 시작" 클릭
3. "새 세션 시작" 클릭
4. QR 코드 저장 또는 화면 공유
```

### 강의 중

```
1. 학생들 QR 코드 스캔
2. 실시간 질문 확인
3. 답변 입력 및 전송
4. 자동 새로고침 ON
```

### 강의 후

```
"세션 종료" 클릭
(또는 그냥 닫기)
```

---

## 🔄 코드 수정 후 재배포

**자동 배포!**

```bash
# 1. 로컬에서 파일 수정

# 2. GitHub에 push
git add .
git commit -m "기능 추가"
git push

# 3. Streamlit Cloud가 자동으로 재배포!
# (1-2분 소요)
```

**확인:**
```
Streamlit Cloud Dashboard
→ 앱 선택
→ "Reboot" 표시 확인
→ 자동 재시작
```

---

## 💡 고급 설정

### 커스텀 도메인 (Pro 플랜)

```
Settings → Custom domain
→ chat.yourschool.com
→ DNS 설정
```

### 리소스 업그레이드 (Pro)

**무료 플랜:**
- 1GB RAM
- 1 CPU
- 무제한 사용

**Pro 플랜 ($20/월):**
- 8GB RAM
- 2 CPU
- 커스텀 도메인
- 우선 지원

---

## 🎨 UI 커스터마이징

### 색상 변경

`.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### 로고 추가

`app.py`:
```python
st.logo("logo.png")
```

---

## 📊 모니터링

### Streamlit Cloud Dashboard

**확인 가능:**
- 📈 앱 사용 통계
- 🔧 리소스 사용량
- 🐛 에러 로그
- 👥 동시 접속자 수

**접근:**
```
https://streamlit.io/cloud
→ 앱 선택
→ "Metrics" 탭
```

---

## 🐛 문제 해결

### "App is sleeping"

**원인:** 미사용 시 자동 슬립

**해결:** 접속하면 자동으로 깨어남 (10초)

### "데이터가 사라짐"

**원인:** 앱 재시작 시 데이터 초기화

**해결:** 
- Firebase 사용 (영구 저장)
- 또는 강의 중에만 사용 (일회성)

### "ModuleNotFoundError"

**원인:** requirements.txt 오류

**해결:**
```
requirements.txt 확인
→ GitHub에 push
→ 자동 재배포
```

### "Port already in use"

**발생 안 함:** Streamlit Cloud가 자동 관리

---

## 🎯 Node.js → Streamlit 마이그레이션

### 장점

1. ✅ **Python** - JavaScript 불필요
2. ✅ **완전 무료** - 시간 제한 없음
3. ✅ **쉬운 배포** - 5분이면 끝
4. ✅ **자동 관리** - 서버 관리 불필요
5. ✅ **빠른 개발** - 코드 300줄

### 단점

1. ⚠️ **폴링 방식** - 3-5초 지연 (WebSocket보다 느림)
2. ⚠️ **리소스 제한** - 1GB RAM (충분하지만)
3. ⚠️ **공유 리소스** - 가끔 느릴 수 있음

### 결론

**추천:**
- 소규모 강의 (30명 이하) → Streamlit ⭐⭐⭐⭐⭐
- 대규모 강의 (100명+) → Node.js + Railway
- 완전 무료 원함 → Streamlit ⭐⭐⭐⭐⭐

---

## 📋 체크리스트

### 배포 전:

- [ ] GitHub 계정 있음
- [ ] 저장소 생성
- [ ] 파일 업로드
- [ ] requirements.txt 확인
- [ ] app.py 확인

### 배포 후:

- [ ] Streamlit Cloud 가입
- [ ] 앱 생성
- [ ] 배포 완료
- [ ] URL 확인
- [ ] 테스트 (강사 모드)
- [ ] 테스트 (학생 모드)
- [ ] QR 코드 생성 확인

---

## 🎉 최종 정리

**Streamlit Cloud 배포 = 최고의 선택!**

**이유:**
1. ✅ 완전 무료
2. ✅ 무제한 사용
3. ✅ 5분 배포
4. ✅ Python 친화적
5. ✅ 자동 관리

**사용:**
```
1. https://your-app.streamlit.app
2. 강사로 시작
3. QR 코드 공유
4. 끝!
```

---

## 🚀 지금 바로 시작

```bash
# 1. 로컬 테스트
cd streamlit-app
pip install -r requirements.txt
streamlit run app.py

# 2. GitHub 업로드
git init
git add .
git commit -m "Initial commit"
git push

# 3. Streamlit Cloud 배포
https://streamlit.io/cloud
→ New app
→ 저장소 선택
→ Deploy!
```

**5분이면 완성!** 🎯

궁금한 점 있으면 물어보세요! 😊

