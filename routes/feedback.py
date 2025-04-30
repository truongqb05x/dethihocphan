from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from utils.db import get_db_connection
from utils.helpers import allowed_file
from config.config import FEEDBACK_UPLOAD_FOLDER
import os, time

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/api/feedback-types', methods=['GET'])
def get_feedback_types():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, type_name FROM feedback_types WHERE is_active = TRUE")
        types = cursor.fetchall()
        return jsonify(types)
    finally:
        cursor.close()
        conn.close()

@feedback_bp.route('/api/feedback-statuses', methods=['GET'])
def get_feedback_statuses():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, status_name, status_color FROM feedback_statuses WHERE is_active = TRUE")
        statuses = cursor.fetchall()
        return jsonify(statuses)
    finally:
        cursor.close()
        conn.close()

@feedback_bp.route('/api/feedbacks', methods=['GET'])
def get_feedbacks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT f.*, ft.type_name, fs.status_name, fs.status_color
            FROM feedbacks f
            JOIN feedback_types ft ON f.type_id = ft.id
            JOIN feedback_statuses fs ON f.status_id = fs.id
            ORDER BY f.created_at DESC
        """
        cursor.execute(query)
        feedbacks = cursor.fetchall()
        
        for feedback in feedbacks:
            cursor.execute("SELECT * FROM feedback_attachments WHERE feedback_id = %s", (feedback['id'],))
            feedback['attachments'] = cursor.fetchall()
            
            cursor.execute("""
                SELECT fr.*, u.full_name as admin_name 
                FROM feedback_responses fr
                LEFT JOIN users u ON fr.admin_id = u.id
                WHERE fr.feedback_id = %s
                ORDER BY fr.created_at DESC
            """, (feedback['id'],))
            feedback['responses'] = cursor.fetchall()
        
        return jsonify(feedbacks)
    finally:
        cursor.close()
        conn.close()

@feedback_bp.route('/api/feedbacks/<int:feedback_id>', methods=['GET'])
def get_feedback_by_id(feedback_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT f.*, ft.type_name, fs.status_name
            FROM feedbacks f
            JOIN feedback_types ft ON f.type_id = ft.id
            JOIN feedback_statuses fs ON f.status_id = fs.id
            WHERE f.id = %s
        """, (feedback_id,))
        feedback = cursor.fetchone()
        if feedback:
            return jsonify(feedback)
        return jsonify({'error': 'Feedback not found'}), 404
    finally:
        cursor.close()
        conn.close()

@feedback_bp.route('/api/feedbacks/<int:feedback_id>/attachments', methods=['GET'])
def get_feedback_attachments(feedback_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM feedback_attachments WHERE feedback_id = %s", (feedback_id,))
        attachments = cursor.fetchall()
        return jsonify(attachments)
    finally:
        cursor.close()
        conn.close()

@feedback_bp.route('/api/feedbacks', methods=['POST'])
def create_feedback():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Vui lòng đăng nhập trước khi gửi phản hồi."}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        type_id = request.form.get('type_id')
        title = request.form.get('title')
        content = request.form.get('content')

        cursor.execute(
            """
            INSERT INTO feedbacks
              (user_id, type_id, title, content, ip_address, user_agent)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, type_id, title, content, request.remote_addr, request.headers.get('User-Agent'))
        )
        feedback_id = cursor.lastrowid

        files = request.files.getlist('attachments')
        for file in files:
            if file.filename == '':
                continue
            filename = secure_filename(file.filename)
            data = file.read()
            file.seek(0)
            timestamp = int(time.time())
            filepath = f"uploads/feedbacks/{feedback_id}_{timestamp}_{filename}"
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)

            cursor.execute(
                """
                INSERT INTO feedback_attachments
                  (feedback_id, file_name, file_path, file_size, file_type)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (feedback_id, filename, filepath, len(data), file.content_type)
            )

        conn.commit()
        return jsonify({"message": "Feedback created", "id": feedback_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": "Có lỗi xảy ra khi lưu phản hồi"}), 500
    finally:
        cursor.close()
        conn.close()