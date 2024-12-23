from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, g
from utils.auth_utils import validate_user, create_session, validate_session, delete_session

loginPage_bp = Blueprint("login", __name__)


@loginPage_bp.before_request
def load_session():
    # 클라이언트 쿠키에서 세션 ID를 가져와 g 객체에 저장
    session_id = request.cookies.get("session_id")

    # 'logout'접근시 load_session 실행 X
    if request.endpoint == "login.logout" or request.endpoint == "/":
        return  # 특정 라우트에서는 메시지 플래시 및 처리 생략


    session_valid, response = validate_session(session_id)

    if response:
        flash("세션이 만료되었습니다.", "danger")
        print("response 1")
        return

    if session_valid:
        flash("정상적으로 로그인중!", "success")
        print("response 2")
        # return redirect(url_for("login.login"))
        return

    print("response 3")
    flash("로그인 후 사용해주세요")


@loginPage_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")

        # 사용자 인증
        if validate_user(user_id, password):
            # 세션 생성
            session_id = create_session(user_id)

            # 쿠키에 세션 ID 설정
            response = make_response(redirect(url_for("upload.upload_image")))
            response.set_cookie("session_id", session_id, httponly=True, secure=False)

            flash("로그인 성공!", "success")
            return response
        else:
            flash("아이디 또는 비밀번호가 올바르지 않습니다.", "danger")

    return render_template("login.html")


@loginPage_bp.route("/logout", methods=["GET"])
def logout():
    # 클라이언트 쿠키에서 세션 ID 가져오기
    session_id = request.cookies.get("session_id")

    if session_id:
        if validate_session(session_id):
            # 세션 삭제
            delete_session(session_id)

            # 쿠키에서 세션 ID 삭제
            response = make_response(redirect(url_for("login.login")))
            response.delete_cookie("session_id")

            flash("로그아웃 완료!", "logout")
            return response
        else:  # 사실 어차피 일어날 수 없는 상황
            flash("세션에는 넌 이미 없는 존재란다", "danger")
    else:
        flash("쿠키가 비었는데 어떻게 들어와있니?", "danger")

    # 로그아웃 후 로그인 페이지로 리다이렉트
    return redirect(url_for("login.login"))