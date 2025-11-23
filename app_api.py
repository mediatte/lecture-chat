"""
강의 실시간 채팅 시스템 - Streamlit + 로컬 API 서버 버전
로컬 Flask API를 통한 세션 데이터 관리
"""

import streamlit as st
import qrcode
from io import BytesIO
from datetime import datetime
import time
import requests

# 페이지 설정
st.set_page_config(
    page_title="강의 실시간 채팅",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 8px;
        font-weight: 600;
    }
    .chat-message {
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
        animation: slideIn 0.3s ease;
    }
    .instructor-message {
        background: #f0f4ff;
        border-left: 3px solid #667eea;
    }
    .student-message {
        background: #ecfdf5;
        border-left: 3px solid #10b981;
    }
    .system-message {
        background: #fef3c7;
        border: 1px solid #fcd34d;
        text-align: center;
        color: #92400e;
        font-size: 13px;
    }
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .header-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# API 서버 URL (Streamlit secrets 또는 기본값)
if hasattr(st, 'secrets') and 'API_SERVER' in st.secrets:
    API_SERVER = st.secrets['API_SERVER']
else:
    API_SERVER = "http://localhost:5000"

def check_api_server():
    """API 서버 연결 확인"""
    try:
        response = requests.get(f"{API_SERVER}/", timeout=3)
        return response.status_code == 200
    except:
        return False

def create_session():
    """새 세션 생성"""
    try:
        response = requests.post(f"{API_SERVER}/api/session", timeout=5)
        data = response.json()
        if data.get('success'):
            return data['session_id']
        return None
    except Exception as e:
        st.error(f"세션 생성 실패: {e}")
        return None

def get_session(session_id):
    """세션 정보 가져오기"""
    try:
        response = requests.get(f"{API_SERVER}/api/session/{session_id}", timeout=5)
        data = response.json()
        if data.get('success'):
            return data['session']
        return None
    except:
        return None

def add_message(session_id, username, message, msg_type='student'):
    """메시지 추가"""
    try:
        response = requests.post(
            f"{API_SERVER}/api/session/{session_id}/message",
            json={
                'username': username,
                'message': message,
                'type': msg_type
            },
            timeout=5
        )
        data = response.json()
        return data.get('success', False)
    except Exception as e:
        st.error(f"메시지 전송 실패: {e}")
        return False

def add_participant(session_id, username):
    """참여자 추가"""
    try:
        response = requests.post(
            f"{API_SERVER}/api/session/{session_id}/participant",
            json={'username': username},
            timeout=5
        )
        data = response.json()
        return data.get('success', False)
    except Exception as e:
        st.error(f"참여자 추가 실패: {e}")
        return False

def get_messages(session_id):
    """메시지 목록 가져오기"""
    try:
        response = requests.get(f"{API_SERVER}/api/session/{session_id}/messages", timeout=5)
        data = response.json()
        if data.get('success'):
            return data['messages']
        return []
    except:
        return []

def generate_qr_code(data):
    """QR 코드 생성"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

# 메인 앱
def main():
    # API 서버 연결 확인
    if not check_api_server():
        st.error(f"""
        ⚠️ **API 서버 연결 실패**
        
        API 서버가 실행 중인지 확인하세요:
        
        **로컬 서버 주소:** `{API_SERVER}`
        
        **서버 실행 방법:**
        ```bash
        cd api-server
        pip install -r requirements.txt
        python server.py
        ```
        
        **외부 접속을 위해 다른 터미널에서:**
        ```bash
        ngrok http 5000
        # 또는
        lt --port 5000
        ```
        
        그 후 Streamlit Secrets에 API 서버 URL 설정:
        ```toml
        API_SERVER = "https://your-tunnel-url"
        ```
        """)
        return
    
    # URL 파라미터로 모드 결정
    try:
        query_params = st.query_params
    except AttributeError:
        query_params = st.experimental_get_query_params()
    
    # 세션 상태 초기화
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'session_id' not in st.session_state:
        st.session_state.session_id = None
    
    # URL에 session_id가 있으면 학생 모드
    if 'session' in query_params and not st.session_state.user_type:
        st.session_state.user_type = 'student'
        session_value = query_params.get('session', query_params.get('session', [None]))
        if isinstance(session_value, list):
            st.session_state.session_id = session_value[0] if session_value else None
        else:
            st.session_state.session_id = session_value
    
    # 모드 선택 또는 실행
    if not st.session_state.user_type:
        show_mode_selection()
    elif st.session_state.user_type == 'instructor':
        show_instructor_interface()
    elif st.session_state.user_type == 'student':
        show_student_interface()

def show_mode_selection():
    """모드 선택 화면"""
    st.markdown("""
    <div class="header-gradient">
        <h1>📚 강의 실시간 채팅</h1>
        <p>로컬 API 서버 연결 🚀</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success(f"✅ API 서버 연결됨: {API_SERVER}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👨‍🏫 강사")
        st.write("세션을 생성하고 학생들의 질문을 받으세요")
        if st.button("강사로 시작", key="instructor"):
            st.session_state.user_type = 'instructor'
            st.session_state.username = '강사'
            st.rerun()
    
    with col2:
        st.markdown("### 🎓 학생")
        st.write("QR 코드를 스캔하거나 세션 ID를 입력하세요")
        session_input = st.text_input("세션 ID", key="student_session_id")
        if st.button("학생으로 참여", key="student") and session_input:
            session = get_session(session_input)
            if session:
                st.session_state.user_type = 'student'
                st.session_state.session_id = session_input
                st.rerun()
            else:
                st.error("유효하지 않은 세션 ID입니다")

def show_instructor_interface():
    """강사 인터페이스"""
    st.markdown("""
    <div class="header-gradient">
        <h1>👨‍🏫 강사 패널</h1>
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### 📊 세션 관리")
        
        if not st.session_state.session_id:
            if st.button("🎯 새 세션 시작", use_container_width=True):
                session_id = create_session()
                if session_id:
                    st.session_state.session_id = session_id
                    st.success("✅ 세션 생성 완료!")
                    st.rerun()
                else:
                    st.error("❌ 세션 생성 실패")
        else:
            session = get_session(st.session_state.session_id)
            if session:
                st.success("🟢 세션 활성")
                st.info(f"**세션 ID**\n{st.session_state.session_id}")
                
                participant_count = len(session.get('participants', {}))
                st.metric("참여자", f"{participant_count}명")
                
                st.markdown("### 📱 QR 코드")
                app_url = st.secrets.get("APP_URL", "https://your-app.streamlit.app") if hasattr(st, 'secrets') else "https://mediatte-lecture-chat.streamlit.app"
                session_url = f"{app_url}?session={st.session_state.session_id}"
                
                qr_img = generate_qr_code(session_url)
                st.image(qr_img, caption="학생들이 스캔", use_column_width=True)
                
                st.code(session_url, language=None)
                
                st.download_button(
                    label="💾 QR 코드 저장",
                    data=qr_img,
                    file_name=f"qr-{st.session_state.session_id}.png",
                    mime="image/png",
                    use_container_width=True
                )
                
                if st.button("🚪 세션 종료", use_container_width=True):
                    st.session_state.session_id = None
                    st.session_state.user_type = None
                    st.rerun()
    
    if st.session_state.session_id:
        session = get_session(st.session_state.session_id)
        
        if session:
            st.markdown("### 💬 실시간 채팅")
            
            messages = session.get('messages', [])
            
            messages_container = st.container()
            
            with messages_container:
                if not messages:
                    st.info("💡 학생들의 질문과 의견이 여기에 표시됩니다")
                else:
                    for msg in messages:
                        if msg.get('type') == 'system':
                            st.markdown(f"""
                            <div class="chat-message system-message">
                                {msg.get('text', '')}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            msg_time = msg.get('timestamp', '')
                            if msg_time:
                                try:
                                    dt = datetime.fromisoformat(msg_time)
                                    msg_time_str = dt.strftime('%H:%M')
                                except:
                                    msg_time_str = datetime.now().strftime('%H:%M')
                            else:
                                msg_time_str = datetime.now().strftime('%H:%M')
                            
                            msg_class = 'instructor-message' if msg.get('type') == 'instructor' else 'student-message'
                            st.markdown(f"""
                            <div class="chat-message {msg_class}">
                                <strong>{msg.get('username', '익명')}</strong> 
                                <span style="color: #999; font-size: 12px;">{msg_time_str}</span>
                                <div style="margin-top: 4px;">{msg.get('message', '')}</div>
                            </div>
                            """, unsafe_allow_html=True)
            
            st.markdown("---")
            col1, col2 = st.columns([5, 1])
            
            with col1:
                message_input = st.text_input(
                    "메시지 입력",
                    key="instructor_message",
                    placeholder="학생들에게 답변하세요...",
                    label_visibility="collapsed"
                )
            
            with col2:
                send_clicked = st.button("📤 전송", use_container_width=True)
            
            if send_clicked and message_input:
                if add_message(st.session_state.session_id, st.session_state.username, message_input, 'instructor'):
                    st.rerun()
            
            st.markdown("---")
            if st.checkbox("🔄 자동 새로고침 (3초)", value=True):
                time.sleep(3)
                st.rerun()
            else:
                if st.button("🔄 수동 새로고침"):
                    st.rerun()
    else:
        st.info("👈 사이드바에서 '새 세션 시작'을 클릭하세요")

def show_student_interface():
    """학생 인터페이스"""
    if not st.session_state.username:
        st.markdown("""
        <div class="header-gradient">
            <h1>🎓 채팅 참여하기</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 참여 방법을 선택하세요")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📝 이름으로 참여")
            username = st.text_input("이름 (닉네임)", placeholder="이름을 입력하세요", key="username_input")
            
            if st.button("💬 이름으로 참여", use_container_width=True, type="primary") and username:
                st.session_state.username = username
                if add_participant(st.session_state.session_id, username):
                    st.rerun()
        
        with col2:
            st.markdown("#### 🎭 익명으로 참여")
            st.info("익명으로 빠르게 참여할 수 있습니다")
            
            if st.button("🎭 익명 참여", use_container_width=True):
                import random
                adjectives = ['활발한', '조용한', '열정적인', '호기심많은', '친절한', '밝은', '성실한', '똑똑한']
                animals = ['토끼', '고양이', '강아지', '판다', '코알라', '펭귄', '다람쥐', '햄스터']
                anonymous_name = f"{random.choice(adjectives)} {random.choice(animals)}{random.randint(1, 99)}"
                
                st.session_state.username = anonymous_name
                if add_participant(st.session_state.session_id, anonymous_name):
                    st.rerun()
        
        st.markdown("---")
        st.markdown("💡 **팁:** 익명 참여를 선택하면 랜덤 닉네임이 자동으로 생성됩니다")
        
        return
    
    st.markdown("""
    <div class="header-gradient">
        <h1>💬 강의 채팅</h1>
        <p>실시간으로 질문하고 소통하세요</p>
    </div>
    """, unsafe_allow_html=True)
    
    session = get_session(st.session_state.session_id)
    
    if not session:
        st.error("세션을 찾을 수 없습니다")
        if st.button("처음으로"):
            st.session_state.clear()
            st.rerun()
        return
    
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        st.success("🟢 연결됨")
        
        participant_count = len(session.get('participants', {}))
        st.metric("참여자", f"{participant_count}명")
        
        if st.button("🚪 나가기", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    messages = session.get('messages', [])
    
    messages_container = st.container()
    
    with messages_container:
        for msg in messages:
            if msg.get('type') == 'system':
                st.markdown(f"""
                <div class="chat-message system-message">
                    {msg.get('text', '')}
                </div>
                """, unsafe_allow_html=True)
            else:
                msg_time = msg.get('timestamp', '')
                if msg_time:
                    try:
                        dt = datetime.fromisoformat(msg_time)
                        msg_time_str = dt.strftime('%H:%M')
                    except:
                        msg_time_str = datetime.now().strftime('%H:%M')
                else:
                    msg_time_str = datetime.now().strftime('%H:%M')
                
                is_mine = msg.get('username') == st.session_state.username
                msg_class = 'instructor-message' if msg.get('type') == 'instructor' else 'student-message'
                display_name = '나' if is_mine else msg.get('username', '익명')
                
                st.markdown(f"""
                <div class="chat-message {msg_class}">
                    <strong>{display_name}</strong> 
                    <span style="color: #999; font-size: 12px;">{msg_time_str}</span>
                    <div style="margin-top: 4px;">{msg.get('message', '')}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2 = st.columns([5, 1])
    
    with col1:
        message_input = st.text_input(
            "메시지 입력",
            key="student_message",
            placeholder="질문이나 의견을 입력하세요...",
            label_visibility="collapsed"
        )
    
    with col2:
        send_clicked = st.button("📤", use_container_width=True)
    
    if send_clicked and message_input:
        if add_message(st.session_state.session_id, st.session_state.username, message_input, 'student'):
            st.rerun()
    
    st.markdown("---")
    if st.checkbox("🔄 자동 새로고침 (2초)", value=True):
        time.sleep(2)
        st.rerun()
    else:
        if st.button("🔄 수동 새로고침"):
            st.rerun()

if __name__ == "__main__":
    main()

