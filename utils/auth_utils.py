import json
import os
import time
import uuid

from flask import make_response, redirect, url_for

# 회원가입 파일 경로
USERS_FILE_PATH = "users.json"
# 세션 관리 파일 경로
SESSIONS_FILE_PATH = "sessions.json"
# 세션 만료 시간 (5분)
# SESSION_EXPIRY = 5 * 60  # 초 단위
# 세션 만료 시간 (20초)
SESSION_EXPIRY = 5*60  # 초 단위

# JSON 파일 초기화
def initialize_json(file_path, default_data):
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump(default_data, file)


# 회원가입 시 사용자 추가 함수
def add_user(user_id, username, password):
    initialize_json(USERS_FILE_PATH, {})
    with open(USERS_FILE_PATH, "r") as file:
        data = json.load(file)

    if user_id in data:
        return False  # 아이디 중복

    # 새 사용자 추가
    data[user_id] = {"username": username, "password": password}
    with open(USERS_FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)
    return True


# 로그인 확인 함수
def validate_user(user_id, password):
    initialize_json(USERS_FILE_PATH, {})
    with open(USERS_FILE_PATH, "r") as file:
        data = json.load(file)

    return user_id in data and data[user_id]["password"] == password


# 세션 추가 함수
def create_session(user_id):
    initialize_json(SESSIONS_FILE_PATH, {})
    with open(SESSIONS_FILE_PATH, "r") as file:
        sessions = json.load(file)

    # 고유 세션 ID 생성
    session_id = str(uuid.uuid4())
    expiry_time = time.time() + SESSION_EXPIRY

    # 세션 추가
    sessions[session_id] = {"user_id": user_id, "expiry": expiry_time}
    with open(SESSIONS_FILE_PATH, "w") as file:
        json.dump(sessions, file, indent=4)
    return session_id


# 세션 삭제 함수 (로그아웃)
def delete_session(session_id):
    initialize_json(SESSIONS_FILE_PATH, {})
    with open(SESSIONS_FILE_PATH, "r") as file:
        sessions = json.load(file)

    if session_id in sessions:
        del sessions[session_id]
        with open(SESSIONS_FILE_PATH, "w") as file:
            json.dump(sessions, file, indent=4)
        return True
    return False


def validate_session(session_id):
    """
    세션 유효성 검사 및 만료 처리.
    - session_id가 비어 있으면 False와 result 0 반환.
    - 세션 파일에서 만료된 세션을 삭제.
    - session_id가 유효하면 True와 result 1 반환.
    """
    print("validate 함수 실행")
    # 세션 파일 초기화
    initialize_json(SESSIONS_FILE_PATH, {})

    # 세션 데이터 로드
    with open(SESSIONS_FILE_PATH, "r") as file:
        sessions = json.load(file)

    # 세션 ID가 없으면 바로 반환
    if not session_id:
        print("no session id 실행")
        return False, 0

    # 현재 시간
    current_time = time.time()

    # 만료된 세션 제거 및 업데이트
    valid_sessions = {}
    session_valid = False  # 세션 유효성 플래그
    result = 0  # 기본 결과 값

    for sid, details in sessions.items():
        if current_time < details["expiry"]:
            valid_sessions[sid] = details
        else:
            # 만료된 세션 삭제
            if sid == session_id:
                result = 2  # 세션 만료

    # 유효한 세션만 다시 저장
    with open(SESSIONS_FILE_PATH, "w") as file:
        json.dump(valid_sessions, file, indent=4)

    # 세션 ID가 유효한지 확인
    if session_id in valid_sessions:
        session_valid = True
        result = 1  # 세션 유효

    return session_valid, result
