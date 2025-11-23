"""
강의 실시간 채팅 시스템 - Streamlit 버전
Firebase Firestore를 사용한 실시간 채팅
"""

import streamlit as st
import qrcode
from io import BytesIO
from datetime import datetime
import time
import uuid
import json
from pathlib import Path

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

# 데이터 저장 (간단한 JSON 파일 사용)
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def load_sessions():
    """세션 데이터 로드"""
    sessions_file = DATA_DIR / "sessions.json"
    if sessions_file.exists():
        with open(sessions_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_sessions(sessions):
    """세션 데이터 저장"""
    sessions_file = DATA_DIR / "sessions.json"
    with open(sessions_file, 'w', encoding='utf-8') as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)

def create_session():
    """새 세션 생성"""
    session_id = f"session-{int(time.time())}-{uuid.uuid4().hex[:6]}"
    sessions = load_sessions()
    sessions[session_id] = {
        'id': session_id,
        'created_at': datetime.now().isoformat(),
        'messages': [],
        'participants': {}
    }
    save_sessions(sessions)
    return session_id

def add_message(session_id, username, message, user_type='student'):
    """메시지 추가"""
    sessions = load_sessions()
    if session_id in sessions:
        msg = {
            'id': f"msg-{int(time.time())}-{uuid.uuid4().hex[:6]}",
            'username': username,
            'message': message,
            'type': user_type,
            'timestamp': datetime.now().isoformat()
        }
        sessions[session_id]['messages'].append(msg)
        save_sessions(sessions)
        return True
    return False

def add_participant(session_id, username):
    """참여자 추가"""
    sessions = load_sessions()
    if session_id in sessions:
        sessions[session_id]['participants'][username] = {
            'joined_at': datetime.now().isoformat()
        }
        save_sessions(sessions)
        # 시스템 메시지 추가
        add_system_message(session_id, f"{username}님이 입장했습니다")
        return True
    return False

def add_system_message(session_id, text):
    """시스템 메시지 추가"""
    sessions = load_sessions()
    if session_id in sessions:
        msg = {
            'id': f"sys-{int(time.time())}-{uuid.uuid4().hex[:6]}",
            'text': text,
            'type': 'system',
            'timestamp': datetime.now().isoformat()
        }
        sessions[session_id]['messages'].append(msg)
        save_sessions(sessions)

def get_session(session_id):
    """세션 정보 가져오기"""
    sessions = load_sessions()
    return sessions.get(session_id)

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
    
    # BytesIO로 변환
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

# 메인 앱
def main():
    # URL 파라미터로 모드 결정
    query_params = st.query_params
    
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
        st.session_state.session_id = query_params['session']
    
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
        <p>실시간으로 소통하는 스마트한 강의</p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # 사이드바
    with st.sidebar:
        st.markdown("### 📊 세션 관리")
        
        if not st.session_state.session_id:
            if st.button("🎯 새 세션 시작", use_container_width=True):
                session_id = create_session()
                st.session_state.session_id = session_id
                add_system_message(session_id, "세션이 시작되었습니다")
                st.rerun()
        else:
            session = get_session(st.session_state.session_id)
            if session:
                st.success("🟢 세션 활성")
                st.info(f"**세션 ID**\n{st.session_state.session_id}")
                
                # 참여자 수
                participant_count = len(session['participants'])
                st.metric("참여자", f"{participant_count}명")
                
                # QR 코드 생성
                st.markdown("### 📱 QR 코드")
                app_url = st.secrets.get("APP_URL", "https://your-app.streamlit.app")
                session_url = f"{app_url}?session={st.session_state.session_id}"
                
                qr_img = generate_qr_code(session_url)
                st.image(qr_img, caption="학생들이 스캔", use_column_width=True)
                
                st.code(session_url, language=None)
                
                # QR 코드 다운로드
                st.download_button(
                    label="💾 QR 코드 저장",
                    data=qr_img,
                    file_name=f"qr-{st.session_state.session_id}.png",
                    mime="image/png",
                    use_container_width=True
                )
                
                # 세션 종료
                if st.button("🚪 세션 종료", use_container_width=True):
                    st.session_state.session_id = None
                    st.session_state.user_type = None
                    st.rerun()
    
    # 메인 채팅 영역
    if st.session_state.session_id:
        session = get_session(st.session_state.session_id)
        
        if session:
            # 채팅 메시지 표시
            st.markdown("### 💬 실시간 채팅")
            
            # 메시지 컨테이너
            messages_container = st.container()
            
            with messages_container:
                if not session['messages']:
                    st.info("💡 학생들의 질문과 의견이 여기에 표시됩니다")
                else:
                    for msg in session['messages']:
                        if msg['type'] == 'system':
                            st.markdown(f"""
                            <div class="chat-message system-message">
                                {msg['text']}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            msg_time = datetime.fromisoformat(msg['timestamp']).strftime('%H:%M')
                            msg_class = 'instructor-message' if msg['type'] == 'instructor' else 'student-message'
                            st.markdown(f"""
                            <div class="chat-message {msg_class}">
                                <strong>{msg['username']}</strong> 
                                <span style="color: #999; font-size: 12px;">{msg_time}</span>
                                <div style="margin-top: 4px;">{msg['message']}</div>
                            </div>
                            """, unsafe_allow_html=True)
            
            # 메시지 입력
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
                add_message(
                    st.session_state.session_id,
                    st.session_state.username,
                    message_input,
                    'instructor'
                )
                st.rerun()
            
            # 자동 새로고침 (5초마다)
            st.markdown("---")
            if st.checkbox("🔄 자동 새로고침 (5초)", value=True):
                time.sleep(5)
                st.rerun()
            else:
                if st.button("🔄 수동 새로고침"):
                    st.rerun()
    else:
        st.info("👈 사이드바에서 '새 세션 시작'을 클릭하세요")

def show_student_interface():
    """학생 인터페이스"""
    # 이름 입력
    if not st.session_state.username:
        st.markdown("""
        <div class="header-gradient">
            <h1>🎓 채팅 참여하기</h1>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("이름 (닉네임)", placeholder="이름을 입력하세요")
        
        if st.button("💬 채팅 참여", use_container_width=True) and username:
            st.session_state.username = username
            add_participant(st.session_state.session_id, username)
            st.rerun()
        
        return
    
    # 채팅 화면
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
    
    # 사이드바
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        st.success("🟢 연결됨")
        
        participant_count = len(session['participants'])
        st.metric("참여자", f"{participant_count}명")
        
        if st.button("🚪 나가기", use_container_width=True):
            add_system_message(
                st.session_state.session_id,
                f"{st.session_state.username}님이 퇴장했습니다"
            )
            st.session_state.clear()
            st.rerun()
    
    # 메시지 표시
    messages_container = st.container()
    
    with messages_container:
        for msg in session['messages']:
            if msg['type'] == 'system':
                st.markdown(f"""
                <div class="chat-message system-message">
                    {msg['text']}
                </div>
                """, unsafe_allow_html=True)
            else:
                msg_time = datetime.fromisoformat(msg['timestamp']).strftime('%H:%M')
                is_mine = msg.get('username') == st.session_state.username
                msg_class = 'instructor-message' if msg['type'] == 'instructor' else 'student-message'
                display_name = '나' if is_mine else msg['username']
                
                st.markdown(f"""
                <div class="chat-message {msg_class}">
                    <strong>{display_name}</strong> 
                    <span style="color: #999; font-size: 12px;">{msg_time}</span>
                    <div style="margin-top: 4px;">{msg['message']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # 메시지 입력
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
        add_message(
            st.session_state.session_id,
            st.session_state.username,
            message_input,
            'student'
        )
        st.rerun()
    
    # 자동 새로고침
    st.markdown("---")
    if st.checkbox("🔄 자동 새로고침 (3초)", value=True):
        time.sleep(3)
        st.rerun()
    else:
        if st.button("🔄 수동 새로고침"):
            st.rerun()

if __name__ == "__main__":
    main()

