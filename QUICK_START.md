# ⚡ 5분 배포 가이드

## 🎯 단계별 실행

### 1️⃣ GitHub 저장소 만들기 (1분)

**웹 브라우저에서:**

```
1. https://github.com/new 접속

2. 입력:
   Repository name: lecture-chat-streamlit
   Public ✅
   
3. "Create repository" 클릭

4. 다음 명령어 복사 (아래 화면에 나옴):
   git remote add origin https://github.com/사용자명/lecture-chat-streamlit.git
   git branch -M main
   git push -u origin main
```

---

### 2️⃣ GitHub에 업로드 (1분)

**터미널에서 실행:**

```bash
# 이미 git init, git add, git commit 완료!

# 위에서 복사한 명령어 실행:
git remote add origin https://github.com/사용자명/lecture-chat-streamlit.git
git branch -M main
git push -u origin main
```

**GitHub 사용자명/비밀번호 입력 요청 시:**
- Username: GitHub 사용자명
- Password: Personal Access Token 사용
  (https://github.com/settings/tokens)

---

### 3️⃣ Streamlit Cloud 배포 (3분)

**웹 브라우저에서:**

```
1. https://streamlit.io/cloud 접속

2. "Sign up" 또는 "Log in"
   → "Continue with GitHub" 클릭
   → 권한 승인

3. "New app" 클릭

4. 입력:
   Repository: lecture-chat-streamlit
   Branch: main
   Main file path: app.py
   
   App URL: 원하는이름 (예: my-lecture-chat)

5. "Deploy!" 클릭

6. 1-2분 대기...

7. ✅ 완료!
   https://your-app-name.streamlit.app
```

---

### 4️⃣ Secrets 설정 (1분, 선택)

**Streamlit Cloud에서:**

```
1. 앱 선택 → ⚙️ Settings

2. "Secrets" 탭 클릭

3. 입력:
   APP_URL = "https://your-app-name.streamlit.app"

4. "Save" 클릭
```

---

## 🎉 완성!

**이제 사용 가능:**

```
https://your-app-name.streamlit.app
```

**테스트:**

1. "강사로 시작" 클릭
2. "새 세션 시작" 클릭
3. QR 코드 확인 ✅
4. 스마트폰으로 QR 스캔
5. 채팅 시작! 💬

---

## 🔄 코드 수정 후

```bash
# 파일 수정 후
git add .
git commit -m "수정 내용"
git push

# Streamlit이 자동으로 재배포! ✨
```

---

## 📱 실제 사용

### 강의 전:
```
1. 앱 접속
2. "강사로 시작"
3. QR 코드 화면 공유
```

### 강의 중:
```
학생들 QR 스캔 → 자동 입장
실시간 질문 & 답변
```

### 강의 후:
```
"세션 종료" 클릭
```

---

## 💡 로컬 테스트 (배포 전)

```bash
cd streamlit-app
pip install -r requirements.txt
streamlit run app.py
```

**브라우저:** http://localhost:8501

---

## 🐛 문제 발생 시

### "Git credentials required"

```bash
# Personal Access Token 생성:
https://github.com/settings/tokens
→ Generate new token (classic)
→ 'repo' 권한 선택
→ 토큰 복사

# 터미널에서:
git push
Username: GitHub사용자명
Password: 복사한토큰붙여넣기
```

### "App failed to start"

```
Streamlit Dashboard → Logs 확인
→ 에러 수정 후 git push
```

---

## 🎯 완료 체크리스트

- [ ] GitHub 저장소 생성
- [ ] git push 완료
- [ ] Streamlit Cloud 배포
- [ ] 앱 URL 접속 확인
- [ ] 강사 모드 테스트
- [ ] QR 코드 생성 확인
- [ ] 스마트폰으로 QR 스캔 테스트
- [ ] 채팅 송수신 확인

---

## 🚀 지금 시작!

**GitHub 저장소부터 만들어주세요:**
https://github.com/new

궁금한 점 있으면 물어보세요! 😊

