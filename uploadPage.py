import datetime
import json
import os
from flask import Blueprint, jsonify, request, render_template, current_app

from utils.imageFile_utils import allowed_file

from AI.classificationAI_test import running_AI

uploadPage_bp = Blueprint("upload", __name__)
UPLOAD_FOLDER = 'images'  # 서버에 이미지가 저장될 폴더


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

            # 클라이언트 쿠키에서 session_id 가져오기
            session_id = request.cookies.get('session_id')

            # 서버에 저장된 sessions.json 파일에서 사용자 ID 조회
            sessions_file = os.path.join(current_app.root_path, 'sessions.json')

            with open(sessions_file, 'r') as f:
                sessions = json.load(f)
            session_data = sessions.get(session_id)

            if session_data:
                user_id = session_data.get('user_id')
            else: 
                return jsonify({"result": 4})

            # 저장 파일명 생성 (저장 시각 + user_id)
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{user_id}.jpg"
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            # AI 모델 실행
            result = list(running_AI(file))  # set을 list로 변환

            return jsonify({"result": 2, "confidence": result[0], "artist": result[1]})
        else:
            return jsonify({"result": 3})

    # GET 요청일 경우 업로드 페이지 렌더링
    return render_template('upload.html')


