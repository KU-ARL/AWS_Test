from flask import Blueprint, jsonify, request, render_template
from utils.auth_utils import add_user

registerPage_bp = Blueprint("register", __name__)

@registerPage_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        user_id = request.json.get("user_id")
        username = request.json.get("username")
        password = request.json.get("password")

        if not user_id or not username or not password:
            return jsonify({"result": 0})  # 입력값 부족

        if add_user(user_id, username, password):
            return jsonify({"result": 1})  # 회원가입 성공
        else:
            return jsonify({"result": 2})  # 아이디 중복
        
    return render_template("register.html")