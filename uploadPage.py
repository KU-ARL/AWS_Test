import os
from flask import Blueprint, flash, jsonify, redirect, request, render_template, current_app, url_for

from utils.auth_utils import validate_session
from utils.imageFile_utils import allowed_file


uploadPage_bp = Blueprint("upload", __name__)
UPLOAD_FOLDER = 'images'  # 서버에 이미지가 저장될 폴더


@uploadPage_bp.before_request
def load_session():
    print("load_session 실행")
    session_id = request.cookies.get("session_id")
    session_valid, result = validate_session(session_id)

    if result == 0:
        return jsonify({"result": 0})  # 세션 없음

    if result == 2:
        return jsonify({"result": 2}) # 세션 만료

    if session_valid:
        return  # 세션이 유효할 경우 계속 진행



# 이미지 업로드 페이지
@uploadPage_bp.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # 파일이 요청에 포함되어 있는지 확인
        if 'image' not in request.files:
            return jsonify({"result": 0})

        file = request.files['image']

        # 파일명이 없는 경우 처리
        if file.filename == '':
            return jsonify({"result": 1})

        # 파일 유효성 검사
        if file and allowed_file(file.filename):
            # Flask 설정에서 업로드 폴더 경로 가져오기
            upload_folder = current_app.config['UPLOAD_FOLDER']

            # 폴더가 없다면 생성
            os.makedirs(upload_folder, exist_ok=True)

            # 파일 저장
            filepath = os.path.join(upload_folder, file.filename)
            file.save(filepath)

            # AI 모델 실행
            result = ["SMC","99.99%"]  # set을 list로 변환

            return jsonify({"result": 2, "confidence": result[0], "artist": result[1]})
        else:
            return jsonify({"result": 3})

    # GET 요청일 경우 업로드 페이지 렌더링
    return render_template('upload.html')


