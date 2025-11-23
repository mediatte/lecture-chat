# 📚 강의 실시간 채팅 - Streamlit 앱

Python Streamlit 기반 실시간 채팅 앱

---

## 📁 파일 구성

- `app.py` - 기본 버전 (로컬 JSON 저장)
- `app_api.py` - 로컬 API 서버 연동 버전 ⭐ 추천
- `requirements.txt` - Python 의존성
- `.streamlit/` - Streamlit 설정

---

## 🚀 사용 방법

### 로컬 테스트

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Streamlit Cloud 배포

```bash
# GitHub 업로드
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/mediatte/lecture-chat.git
git push -u origin main

# Streamlit Cloud에서:
# 1. https://streamlit.io/cloud 접속
# 2. New app 클릭
# 3. Repository 선택
# 4. Main file: app.py
# 5. Deploy!
```

---

## ⚙️ API 서버 연동 (추천)

**1. app_api.py 사용:**
```bash
cp app_api.py app.py
echo "requests>=2.31.0" >> requirements.txt
```

**2. Streamlit Secrets 설정:**
```toml
API_SERVER = "https://your-tunnel-url"
APP_URL = "https://your-app.streamlit.app"
```

**3. 로컬 API 서버 실행:**
```bash
cd ../api-server
python server.py

# 외부 접속 (새 터미널)
lt --port 5000
```

---

## 📝 기능

- ✅ 강사/학생 모드 분리
- ✅ 세션 생성 및 관리
- ✅ QR 코드 자동 생성
- ✅ 익명 참여 기능
- ✅ 실시간 채팅 (자동 새로고침)
- ✅ 참여자 수 표시

---

**상세 가이드는 상위 폴더 README.md 참고**
