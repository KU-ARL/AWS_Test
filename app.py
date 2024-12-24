import json
import os
from flask import Flask, current_app, jsonify, make_response, render_template, request

from loginPage import loginPage_bp
from registerPage import registerPage_bp
from uploadPage import uploadPage_bp

from utils.auth_utils import delete_session, validate_session, log_user_activity


app = Flask(__name__)

UPLOAD_FOLDER = 'images'
app.secret_key = 'gyuchul_company'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 블루프린트 등록
app.register_blueprint(loginPage_bp)
app.register_blueprint(registerPage_bp)
app.register_blueprint(uploadPage_bp)


@app.route("/validation", methods=["GET"])
def load_session():
    session_id = request.cookies.get("session_id")

    session_valid, result = validate_session(session_id)
    if result == 0:
        response = make_response(jsonify({"result": 0}))
        response.set_cookie("session_id", "", expires=0)  # 쿠키 만료

        return response  # 세션 없음

    if result == 2:
        response = make_response(jsonify({"result": 2}))
        response.set_cookie("session_id", "", expires=0)  # 쿠키 만료

        return response  # 세션 만료

    if session_valid:
        return jsonify({"result": 1}) # 세션이 유효할 경우 계속 진행


@app.route("/logout", methods=["GET"])
def logout():
    # 클라이언트 쿠키에서 세션 ID 가져오기
    session_id = request.cookies.get("session_id")

    if session_id:
        # 세션 유효성 확인
        if validate_session(session_id):
            # 사용자 ID 조회
            sessions_file = os.path.join(current_app.root_path, 'sessions.json')

            with open(sessions_file, 'r') as f:
                sessions = json.load(f)
            session_data = sessions.get(session_id)

            if session_data:
                # user_id 추출
                user_id = session_data.get('user_id')
                delete_session(session_id)

                # 로그아웃 성공 로그 기록
                log_user_activity("로그아웃", user_id=user_id, success=True)

            # 쿠키 제거
            response = make_response(jsonify({"result": 0}))
            response.set_cookie("session_id", "", expires=0)  # 쿠키 만료

            return response
        else:
            # 세션이 유효하지 않은 경우 valideate에서 이미 세션 만료로 로그 처리

            return jsonify({"result": 1})  # 쿠키는 있지만 세션이 없음
    else:
        # 쿠키가 없는 경우 로그아웃 실패
        log_user_activity("로그아웃", user_id="Unknown", success=False)

        return jsonify({"result": 2})  # 쿠키도 없음



@app.route("/")
def home():
    return render_template("index.html")


# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

