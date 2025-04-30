from flask import Blueprint, request, jsonify
from utils.db import get_db_connection

schools_bp = Blueprint('schools', __name__)

@schools_bp.route('/api/schools', methods=['GET'])
def get_schools():
    try:
        conn = get_db_connection()
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
        cursor.close()
        conn.close()

@schools_bp.route('/api/schools/<int:school_id>/faculties', methods=['GET'])
def get_faculties_by_school(school_id):
    try:
        conn = get_db_connection()
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
        cursor.close()
        conn.close()

@schools_bp.route('/api/faculties/<int:faculty_id>/subjects', methods=['GET'])
def get_subjects_by_faculty(faculty_id):
    document_type = request.args.get('type', 'exam')
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT s.id, s.name,
                (SELECT COUNT(*) FROM documents d 
                 WHERE d.subject_id = s.id AND d.document_type = %s) AS count
            FROM subjects s
            WHERE s.faculty_id = %s
            ORDER BY s.name
        """
        cursor.execute(query, (document_type, faculty_id))
        subjects = cursor.fetchall()
        return jsonify(subjects)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@schools_bp.route('/api/get_schools_v2', methods=['GET'])
def get_schools_v2():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, name AS school_name FROM schools"
        cursor.execute(query)
        schools = cursor.fetchall()
        return jsonify(schools)
    finally:
        cursor.close()
        conn.close()

@schools_bp.route('/api/faculties_v2/<int:school_id>', methods=['GET'])
def get_faculties_v2(school_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, name AS faculty_name FROM faculties WHERE school_id = %s"
        cursor.execute(query, (school_id,))
        faculties = cursor.fetchall()
        return jsonify(faculties)
    finally:
        cursor.close()
        conn.close()

@schools_bp.route('/api/subjects_v2/<int:faculty_id>', methods=['GET'])
def get_subjects_v2(faculty_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, name AS subject_name FROM subjects WHERE faculty_id = %s"
        cursor.execute(query, (faculty_id,))
        subjects = cursor.fetchall()
        return jsonify(subjects)
    finally:
        cursor.close()
        conn.close()

@schools_bp.route('/api/add_school_v2', methods=['POST'])
def add_school_v2():
    name = request.form.get("tenTruong")
    if not name:
        return jsonify({"error": "Thiếu tên trường"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO schools (name) VALUES (%s)"
        cursor.execute(query, (name,))
        conn.commit()
        school_id = cursor.lastrowid
        return jsonify({"message": "Thêm trường thành công", "school_id": school_id}), 200
    finally:
        cursor.close()
        conn.close()

@schools_bp.route('/api/add_department_v2', methods=['POST'])
def add_department_v2():
    name = request.form.get("tenKhoa")
    truongKhoa = request.form.get("truongKhoa")
    if not name or not truongKhoa:
        return jsonify({"error": "Thiếu tên khoa hoặc trường"}), 400

    try:
        school_id = int(truongKhoa.split('-')[0])
    except Exception:
        return jsonify({"error": "Giá trị trường không hợp lệ"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO faculties (school_id, name) VALUES (%s, %s)"
        cursor.execute(query, (school_id, name))
        conn.commit()
        faculty_id = cursor.lastrowid
        return jsonify({"message": "Thêm khoa thành công", "faculty_id": faculty_id}), 200
    finally:
        cursor.close()
        conn.close()

@schools_bp.route('/api/add_subject_v2', methods=['POST'])
def add_subject_v2():
    name = request.form.get("tenMon")
    faculty_id = request.form.get("khoaMon")
    
    if not name or not faculty_id:
        return jsonify({"error": "Thiếu tên môn hoặc khoa"}), 400

    try:
        faculty_id = int(faculty_id)
    except ValueError:
        return jsonify({"error": "Giá trị khoa không hợp lệ"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO subjects (faculty_id, name) VALUES (%s, %s)"
        cursor.execute(query, (faculty_id, name))
        conn.commit()
        subject_id = cursor.lastrowid
        return jsonify({"message": "Thêm môn học thành công", "subject_id": subject_id}), 200
    finally:
        cursor.close()
        conn.close()