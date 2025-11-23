# 🚀 GitHub + Streamlit Cloud 배포 가이드

## 🎯 전체 흐름 (5분!)

```
로컬 코드 → GitHub 업로드 → Streamlit Cloud 배포 → 완성! ✨
```

---

## 📋 1단계: GitHub 저장소 만들기 (1분)

### 방법 1: 웹사이트에서 (더 쉬움! 추천 ⭐)

1. **GitHub 접속**
   ```
   https://github.com/new
   ```

2. **저장소 설정**
   ```
   Repository name: lecture-chat-streamlit
   Description: 강의 실시간 채팅 시스템 (Python + Streamlit)
   
   ✅ Public (반드시 Public으로!)
   ❌ Add a README file (체크 해제)
   ❌ Add .gitignore (체크 해제)
   
   "Create repository" 클릭
   ```

3. **명령어 복사**
   ```
   생성 후 나오는 명령어 중에서:
   "…or push an existing repository from the command line"
   밑에 있는 3줄 복사해두기
   
   예시:
   git remote add origin https://github.com/사용자명/lecture-chat-streamlit.git
   git branch -M main
   git push -u origin main
   ```

---

## 💻 2단계: 터미널에서 업로드 (2분)

### 현재 디렉토리 확인

```bash
cd ~/Library/CloudStorage/OneDrive-고운고등학교/PROJECTS/websocket_sidebar/streamlit-app
pwd
```

### Git 설정 (처음만)

```bash
# 이름과 이메일 설정 (한 번만 하면 됨)
git config --global user.name "내이름"
git config --global user.email "내이메일@example.com"
```

### 파일 추가 및 커밋

```bash
# 모든 파일 추가
git add .

# 커밋
git commit -m "강의 실시간 채팅 시스템 초기 버전"

# GitHub 저장소 연결 (위에서 복사한 URL 사용)
git remote add origin https://github.com/사용자명/lecture-chat-streamlit.git

# 브랜치 이름 변경
git branch -M main

# 업로드!
git push -u origin main
```

### 완료 확인

```
브라우저에서 저장소 확인:
https://github.com/사용자명/lecture-chat-streamlit

파일들이 보이면 성공! ✅
```

---

## ☁️ 3단계: Streamlit Cloud 배포 (2분)

### 1. Streamlit Cloud 접속

```
https://streamlit.io/cloud
```

### 2. 로그인

```
"Sign up" 또는 "Log in" 클릭
→ "Continue with GitHub" 선택 ✅
→ GitHub 계정으로 로그인
→ 권한 승인 (Authorize Streamlit)
```

### 3. 새 앱 생성

```
대시보드에서 "New app" 클릭 (우측 상단)
```

### 4. 앱 설정

```
Repository: lecture-chat-streamlit 선택
Branch: main
Main file path: app.py

App URL (선택사항):
your-app-name (원하는 이름 입력)
→ https://your-app-name.streamlit.app

Advanced settings (선택사항):
Python version: 3.11 (기본값 사용)
```

### 5. Deploy! 클릭

```
파란색 "Deploy!" 버튼 클릭
```

### 6. 배포 진행 확인

```
화면에 로그가 실시간으로 표시됨:

📦 Installing dependencies...
   ✅ streamlit
   ✅ qrcode
   ✅ Pillow
   ✅ firebase-admin
   ✅ python-dotenv

🚀 Starting app...

✅ Your app is live at:
   https://your-app-name.streamlit.app
```

---

## 🎉 4단계: 완료 및 테스트

### 앱 접속

```
https://your-app-name.streamlit.app
```

### 테스트

1. **강사 모드**
   ```
   "강사로 시작" 클릭
   → "새 세션 시작" 클릭
   → QR 코드 확인
   ```

2. **학생 모드 (스마트폰)**
   ```
   QR 코드 스캔
   → 이름 입력
   → 채팅 참여
   ```

3. **메시지 테스트**
   ```
   학생: "테스트 질문입니다"
   강사: "답변 드립니다"
   ```

---

## 🔄 코드 수정 후 재배포

### 자동 배포! (GitHub push만 하면 됨)

```bash
# 1. 파일 수정 (app.py, requirements.txt 등)

# 2. Git 커밋 및 푸시
git add .
git commit -m "기능 개선"
git push

# 3. Streamlit Cloud가 자동으로 재배포!
# (1-2분 소요)
```

### 수동 재시작

```
Streamlit Cloud Dashboard
→ 앱 선택
→ ⋮ (메뉴) 클릭
→ "Reboot app" 선택
```

---

## ⚙️ Secrets 설정 (선택사항)

### APP_URL 설정

1. **Streamlit Cloud Dashboard**
   ```
   앱 선택 → ⚙️ Settings 클릭
   ```

2. **Secrets 탭**
   ```
   "Secrets" 클릭
   ```

3. **입력**
   ```toml
   APP_URL = "https://your-app-name.streamlit.app"
   ```

4. **Save**
   ```
   "Save" 버튼 클릭
   앱 자동 재시작
   ```

---

## 📱 실제 사용 예시

### 강의 시작

```
1. 스마트폰으로 앱 접속
   https://your-app-name.streamlit.app

2. "강사로 시작" 클릭

3. "새 세션 시작" 클릭

4. QR 코드 화면 공유 또는 저장

5. 학생들 스캔 → 자동 입장!
```

### 실시간 소통

```
학생: "선생님, 이 부분 이해가 안 돼요"
강사: "좋은 질문이에요! ..."

학생: "슬라이드 넘기기 너무 빨라요"
강사: "알겠습니다, 천천히 할게요"
```

---

## 🐛 문제 해결

### "Could not find a version that satisfies..."

**원인:** requirements.txt 버전 문제

**해결:**
```bash
# requirements.txt 수정
streamlit>=1.29.0
qrcode>=7.4.2
Pillow>=10.1.0

# 푸시
git add requirements.txt
git commit -m "의존성 버전 수정"
git push
```

### "App failed to start"

**원인:** app.py 오류

**해결:**
```
Streamlit Cloud Dashboard
→ Logs 탭 확인
→ 에러 메시지 확인
→ 수정 후 푸시
```

### "Session state cleared"

**원인:** 앱 재시작

**해결:** 정상 동작 (데이터는 JSON 파일에 저장됨)

### QR 코드에 localhost 나옴

**원인:** Secrets 미설정

**해결:** 위의 "Secrets 설정" 단계 진행

---

## 📊 모니터링

### Streamlit Cloud Dashboard

```
https://streamlit.io/cloud
→ 앱 선택
```

**확인 가능:**
- 📈 앱 사용 통계
- 🔧 리소스 사용량 (CPU, RAM)
- 🐛 에러 로그
- 👥 동시 접속자 수
- 📝 배포 히스토리

---

## 💡 팁

### 1. 커스텀 URL

```
배포 시 "App URL" 설정:
lecture-chat (짧고 기억하기 쉽게)
→ https://lecture-chat.streamlit.app
```

### 2. 여러 버전 관리

```bash
# 개발 브랜치
git checkout -b dev
git push -u origin dev

# Streamlit에서 dev 브랜치도 배포 가능
# (별도 앱으로 만들기)
```

### 3. 로컬 테스트 먼저

```bash
# 로컬에서 테스트
streamlit run app.py

# 문제 없으면 푸시
git push
```

---

## 🎯 체크리스트

### 배포 전:

- [ ] GitHub 계정 있음
- [ ] Git 설치됨
- [ ] app.py 완성
- [ ] requirements.txt 확인
- [ ] 로컬 테스트 완료

### GitHub 업로드:

- [ ] 저장소 생성 (Public)
- [ ] git init
- [ ] git add .
- [ ] git commit
- [ ] git remote add origin
- [ ] git push
- [ ] 웹에서 파일 확인

### Streamlit Cloud:

- [ ] 계정 가입/로그인
- [ ] New app 생성
- [ ] 저장소 선택
- [ ] app.py 지정
- [ ] Deploy 클릭
- [ ] 배포 완료 확인
- [ ] URL 접속 테스트

---

## 🌟 완료!

**이제 전 세계 어디서나 접속 가능:**

```
https://your-app-name.streamlit.app
```

**특징:**
- ✅ 완전 무료
- ✅ HTTPS 자동
- ✅ 24/7 온라인
- ✅ 모바일 최적화
- ✅ 자동 재배포

**사용:**
```
1. 앱 접속
2. 강사로 시작
3. QR 코드 공유
4. 학생들 참여
5. 실시간 채팅!
```

---

## 📚 추가 자료

**Streamlit 문서:**
```
https://docs.streamlit.io/
```

**Streamlit Cloud 가이드:**
```
https://docs.streamlit.io/streamlit-community-cloud
```

**GitHub 도움말:**
```
https://docs.github.com/ko
```

---

## 🚀 지금 바로 시작!

```bash
cd streamlit-app
git init
git add .
git commit -m "Initial commit"
# GitHub에서 저장소 생성 후
git remote add origin https://github.com/사용자명/저장소.git
git push -u origin main
```

궁금한 점 있으면 언제든 물어보세요! 😊

