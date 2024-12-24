from flask import Blueprint, jsonify, render_template, request, make_response
from utils.auth_utils import validate_user, create_session, log_user_activity

loginPage_bp = Blueprint("login", __name__)


@loginPage_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # 클라이언트에서 보낸 폼 데이터 받기
        user_id = request.form.get("user_id")
        password = request.form.get("password")

        # 사용자 인증
        if validate_user(user_id, password):  # 사용자 인증 함수 호출
            # 세션 생성
            session_id = create_session(user_id)

            log_user_activity("로그인", user_id=user_id, success=True)

            # 쿠키에 세션 ID 설정
            response = make_response(jsonify({"result": 1}))  # 로그인 성공
            response.set_cookie("session_id", session_id, httponly=True, secure=True)

            print("로그인 성공: 세션 ID 생성 완료")
            return response
        else:
            log_user_activity("로그인", user_id=user_id, success=False)

            print("로그인 실패: 잘못된 아이디 또는 비밀번호")
            return jsonify({"result": 0})
        
    return render_template("login.html")

