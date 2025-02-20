import os
import sys
import logging
from flask import Flask, request, jsonify, session, render_template, redirect, url_for, abort, send_from_directory
import mysql.connector
from mysql.connector import pooling
from werkzeug.security import generate_password_hash
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Cấu hình logging
logging.basicConfig(
    filename="debug.log",  # Ghi log vào file
    level=logging.DEBUG,    # Mức độ ghi log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.debug("Chương trình bắt đầu chạy")

import bcrypt
import requests
from flask_cors import CORS
from flask import Flask, request, jsonify
from mysql.connector import pooling, Error
from datetime import datetime

CORS(app)
from flask import send_from_directory
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Đặt secret key cho Flask
# Ghi log toàn bộ request
@app.before_request
def log_request():
    logging.info(f"Request: {request.method} {request.url}")
    logging.info(f"Headers: {request.headers}")
    logging.info(f"Body: {request.get_data()}")

@app.route('/static/image/<filename>')
def serve_image(filename):
    return send_from_directory('static/image', filename)
# Route để phục vụ các file HTML từ thư mục html
# Cấu hình đường dẫn tới thư mục html
@app.route('/html/<path:filename>')
def send_html(filename):
    return send_from_directory('html', filename)

# Trang chủ
@app.route('/')
def index():
    if 'Mozilla' not in request.headers.get('User-Agent', ''):
        abort(403)  # Trả về lỗi 403 Forbidden

    return render_template('index.html')  # Flask sẽ tìm tệp trong thư mục "html" nếu không có cấu hình template_folder

# Tạo kết nối pool đến cơ sở dữ liệu
pool = pooling.MySQLConnectionPool(
    # pool_name="mypool",
    # pool_size=7,  # Kích thước pool
    host='localhost',
    user='mmddllg_huehub',
    password='Ngoctruong123@',
    database='mmddllg_huehub'
)
def get_db_connection():
    # Lấy kết nối từ pool
    return pool.get_connection()
# Thiết lập secret key cho session
app.secret_key = 'your_secret_key'


@app.route('/api/schools', methods=['GET'])
def get_schools():
    conn = None
    cursor = None
    try:
        conn = pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
          SELECT s.id, s.name,
            (SELECT COUNT(*) FROM faculties f WHERE f.school_id = s.id) AS count
          FROM schools s
          ORDER BY s.name
        """)
        schools = cursor.fetchall()
        return jsonify(schools)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/schools/<int:school_id>/faculties', methods=['GET'])
def get_faculties_by_school(school_id):
    conn = None
    cursor = None
    try:
        conn = pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
          SELECT f.id, f.name,
            (SELECT COUNT(*) FROM subjects s WHERE s.faculty_id = f.id) AS count
          FROM faculties f
          WHERE f.school_id = %s
          ORDER BY f.name
        """, (school_id,))
        faculties = cursor.fetchall()
        return jsonify(faculties)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/faculties/<int:faculty_id>/subjects', methods=['GET'])
def get_subjects_by_faculty(faculty_id):
    conn = None
    cursor = None
    try:
        conn = pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
          SELECT s.id, s.name,
            (SELECT COUNT(*) FROM documents d WHERE d.subject_id = s.id) AS count
          FROM subjects s
          WHERE s.faculty_id = %s
          ORDER BY s.name
        """, (faculty_id,))
        subjects = cursor.fetchall()
        return jsonify(subjects)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/subjects/<int:subject_id>/documents_by_year', methods=['GET'])
def get_documents_by_subject_grouped(subject_id):
    conn = None
    cursor = None
    try:
        conn = pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        # Lấy tài liệu của môn học có type = 'exam' và sắp xếp theo năm giảm dần
        cursor.execute("SELECT * FROM documents WHERE subject_id = %s AND document_type	 = 'exam' ORDER BY year DESC", (subject_id,))
        documents = cursor.fetchall()
        grouped = {}
        for doc in documents:
            year = doc['year']
            if year not in grouped:
                grouped[year] = []
            grouped[year].append(doc)
        return jsonify(grouped)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/subjects/<int:subject_id>/documents/<int:year>', methods=['GET'])
def get_documents_by_subject_and_year(subject_id, year):
    conn = None
    cursor = None
    try:
        conn = pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
          SELECT * FROM documents
          WHERE subject_id = %s AND year = %s
        """, (subject_id, year))
        documents = cursor.fetchall()
        return jsonify(documents)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/search/subjects', methods=['GET'])
def search_subjects():
    term = request.args.get('term', '')
    conn = None
    cursor = None
    try:
        conn = pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        # Tìm kiếm môn học theo tên (LIKE %term%)
        cursor.execute("""
            SELECT s.id, s.name, f.id AS faculty_id, f.name AS faculty_name,
                   sc.id AS school_id, sc.name AS school_name
            FROM subjects s
            JOIN faculties f ON s.faculty_id = f.id
            JOIN schools sc ON f.school_id = sc.id
            WHERE s.name LIKE %s
            ORDER BY s.name
        """, ('%' + term + '%',))
        subjects = cursor.fetchall()
        return jsonify(subjects)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/search/documents', methods=['GET'])
def search_documents():
    term = request.args.get('term', '')
    document_type = request.args.get('type', '')  # "exam" hoặc "syllabus"
    conn = None
    cursor = None
    try:
        conn = pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        if document_type:
            query = """
                SELECT * FROM documents
                WHERE file_name LIKE %s AND document_type = %s
                ORDER BY file_name
            """
            cursor.execute(query, ('%' + term + '%', document_type))
        else:
            query = """
                SELECT * FROM documents
                WHERE file_name LIKE %s
                ORDER BY file_name
            """
            cursor.execute(query, ('%' + term + '%',))
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':

    app.run(port=8080, debug=True)