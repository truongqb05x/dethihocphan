from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from utils.db import get_db_connection
from utils.helpers import allowed_file
from config.config import UPLOAD_FOLDER, EXAM_UPLOAD_DIR
import os
from datetime import datetime
documents_bp = Blueprint('documents', __name__)
from app import app  # nếu file chính tên là app.py

@documents_bp.route('/api/subjects/<int:subject_id>/documents_by_year', methods=['GET'])
def get_documents_by_subject_grouped(subject_id):
    document_type = request.args.get('type', 'exam')
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM documents 
            WHERE subject_id = %s AND document_type = %s 
            ORDER BY year DESC
        """, (subject_id, document_type))
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
        cursor.close()
        conn.close()

@documents_bp.route('/api/subjects/<int:subject_id>/documents/<int:year>', methods=['GET'])
def get_documents_by_subject_and_year(subject_id, year):
    document_type = request.args.get('type', 'exam')
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                d.id, d.file_name, d.file_path, d.file_info, d.document_type, 
                d.year, d.subject_id, d.created_at, d.updated_at,
                COUNT(fol.id) AS view_count
            FROM documents d
            LEFT JOIN file_open_logs fol ON d.id = fol.document_id
            WHERE d.subject_id = %s 
                AND d.year = %s 
                AND d.document_type = %s
            GROUP BY d.id
            ORDER BY d.file_name
        """, (subject_id, year, document_type))
        documents = cursor.fetchall()
        return jsonify(documents if documents else []), 200
    except Exception as e:
        return jsonify({'error': 'Không thể lấy danh sách tài liệu', 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@documents_bp.route('/api/search/subjects', methods=['GET'])
def search_subjects():
    term = request.args.get('term', '')
    school_id = request.args.get('school_id', type=int)
    faculty_id = request.args.get('faculty_id', type=int)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT s.id, s.name,
                f.id AS faculty_id, f.name AS faculty_name,
                sc.id AS school_id, sc.name AS school_name
            FROM subjects s
            JOIN faculties f ON s.faculty_id = f.id
            JOIN schools sc ON f.school_id = sc.id
            WHERE s.name LIKE %s
        """
        params = ['%' + term + '%']
        if school_id and school_id > 0:
            query += " AND sc.id = %s"
            params.append(school_id)
        if faculty_id and faculty_id > 0:
            query += " AND f.id = %s"
            params.append(faculty_id)
        query += " ORDER BY s.name"
        
        cursor.execute(query, params)
        subjects = cursor.fetchall()
        return jsonify(subjects)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@documents_bp.route('/api/search/documents', methods=['GET'])
def search_documents():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized: User not logged in'}), 401

    term = request.args.get('term', '')
    document_type = request.args.get('type', '')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT university FROM users WHERE id = %s", (user_id,))
        user_school = cursor.fetchone()
        if not user_school:
            return jsonify({'error': 'User not found'}), 404
        school_id = user_school['university']

        query = """
            SELECT d.*
            FROM documents d
            JOIN subjects s ON d.subject_id = s.id
            JOIN faculties f ON s.faculty_id = f.id
            WHERE d.file_name LIKE %s AND f.school_id = %s
        """
        params = ['%' + term + '%', school_id]
        if document_type:
            query += " AND d.document_type = %s"
            params.append(document_type)
        
        query += " ORDER BY d.file_name"
        cursor.execute(query, params)
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@documents_bp.route('/api/upload_document_v2', methods=['POST'])
def upload_document_v2():
    if 'fileInput' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['fileInput']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_save_path)

        subject_id = request.form.get("mon", type=int)
        year = request.form.get("nam")
        if not year:
            return jsonify({"error": "Thiếu năm"}), 400

        document_name = request.form.get("tenDeThi") or filename
        file_info = request.form.get("infoTitle") or ""
        loai = request.form.get("loai")
        document_type = "exam" if loai == "deThi" else "syllabus" if loai == "taiLieu" else "exam"

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO documents (subject_id, year, file_name, file_info, document_type, file_path)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (subject_id, year, document_name, file_info, document_type, file_save_path))
            conn.commit()
            inserted_id = cursor.lastrowid
            return jsonify({"message": "Upload successful", "document_id": inserted_id}), 200
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "File type not allowed"}), 400

@documents_bp.route('/api/upload_exam', methods=['POST'])
def upload_exam():
    school_id = request.form.get('field')
    if not school_id:
        return jsonify({'error': 'Chưa chọn trường'}), 400

    if 'examFile[]' not in request.files:
        return jsonify({'error': 'Không có file upload'}), 400

    files = request.files.getlist('examFile[]')
    if not files:
        return jsonify({'error': 'Không có file nào được gửi'}), 400

    saved_files = []
    for file in files:
        if file.filename == '':
            continue
        filename = secure_filename(file.filename)
        file_path = os.path.join(EXAM_UPLOAD_DIR, filename)
        file.save(file_path)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO exam_donggop (school_id, filename, filepath) VALUES (%s, %s, %s)"
            cursor.execute(query, (school_id, filename, file_path))
            conn.commit()
            saved_files.append({'filename': filename, 'filepath': file_path})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    return jsonify({'message': 'Upload thành công', 'files': saved_files})

@documents_bp.route('/upload_v2', methods=['POST'])
def upload_file_v2():
    if 'file' not in request.files:
        return jsonify({"error": "Không tìm thấy file upload"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Không có file nào được chọn"}), 400

    try:
        import requests
        import base64
        from config.config import API_URL
        file_data = file.read()
        image_data = base64.b64encode(file_data).decode("utf-8")

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": image_data
                            }
                        },
                        {
                            "text": (
                                "Ảnh này có thỏa mãn một trong hai điều kiện sau không: "
                                "1. Là đoạn hội thoại có chia sẻ link trang web 'dethihocphan.com', hoặc "
                                "2. Là hình ảnh của đề thi học phần (ví dụ đề kiểm tra, đề thi cuối kỳ)? "
                                "Chỉ trả lời true hoặc false. Không giải thích gì thêm."
                            )
                        }
                    ]
                }
            ]
        }

        response = requests.post(API_URL, json=payload)
        if response.status_code != 200:
            return jsonify({"error": f"Lỗi khi kiểm tra hình ảnh: {response.text}"}), 500

        result = response.json()
        is_valid = result["candidates"][0]["content"]["parts"][0]["text"].strip().lower() == "true"

        if not is_valid:
            return jsonify({"error": "Ảnh không phù hợp vui lòng tuân thủ quy tắc chung!"}), 403

        filename = secure_filename(file.filename)
        file_type = request.form.get('type', '')
        if file_type:
            filename = f"{file_type}_{filename}"
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER_V2'], filename)
        file.seek(0)
        file.save(file_path)
        
        relative_path = f"/static/xacthuctaikhoan/{filename}"

        user_id = session.get('user_id')
        if user_id:
            try:
                conn = get_db_connection()
                cursor = conn.cursor(buffered=True)
                query = "INSERT INTO user_images (user_id, image_path) VALUES (%s, %s)"
                cursor.execute(query, (user_id, relative_path))
                conn.commit()
            finally:
                cursor.close()
                conn.close()

        return jsonify({
            "message": "Upload thành công",
            "filepath": relative_path
        }), 200
    except Exception as e:
        return jsonify({"error": f"Lỗi khi xử lý file: {str(e)}"}), 500

@documents_bp.route('/api/log-file-open', methods=['POST'])
def log_file_open():
    data = request.get_json()
    if not data or 'documentId' not in data:
        return jsonify({"error": "documentId is required"}), 400

    document_id = data['documentId']
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO file_open_logs (document_id) VALUES (%s)"
        cursor.execute(sql, (document_id,))
        conn.commit()
        return jsonify({"message": "Log recorded successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@documents_bp.route('/api/log-view-exam', methods=['POST'])
def log_view_exam():
    data = request.get_json()
    document_id = data.get('documentId')
    if not document_id:
        return jsonify({"error": "documentId không được để trống"}), 400

    if 'user_id' not in session:
        return jsonify({"error": "Người dùng chưa đăng nhập"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO user_activity_logs (user_id, activity_type, document_id, ip_address)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (session['user_id'], 'view_exam', document_id, request.remote_addr))
        conn.commit()
        return jsonify({"message": "Log view exam thành công"}), 200
    except Exception as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        cursor.close()
        conn.close()

@documents_bp.route('/api/log-view-exam-v2', methods=['POST'])
def log_view_exam_v2():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401
    user_id = session['user_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = (
            "SELECT COUNT(*) AS views_last_24h FROM user_activity_logs "
            "WHERE activity_type = 'view_exam' AND user_id = %s "
            "AND activity_time >= NOW() - INTERVAL 24 HOUR"
        )
        cursor.execute(query, (user_id,))
        views_last_24h = cursor.fetchone()[0]
        
        if views_last_24h >= 10:
            return jsonify({'error': 'Bạn đã đạt đến giới hạn hôm nay'}), 403
        
        data = request.get_json()
        document_id = data.get('documentId')
        
        insert_query = (
            "INSERT INTO user_activity_logs (user_id, activity_type, document_id) "
            "VALUES (%s, 'view_exam', %s)"
        )
        cursor.execute(insert_query, (user_id, document_id))
        conn.commit()
        
        return jsonify({'success': True})
    finally:
        cursor.close()
        conn.close()

@documents_bp.route('/api/check-file-open-timer', methods=['GET'])
def check_file_open_timer():
    if 'user_id' not in session:
        return jsonify({"error": "User chưa đăng nhập"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)
        query = """
            SELECT MAX(activity_time) AS last_open
            FROM user_activity_logs
            WHERE user_id = %s AND activity_type = 'view_exam'
        """
        cursor.execute(query, (session['user_id'],))
        result = cursor.fetchone()
        if result and result['last_open']:
            last_open = result['last_open']
            now = datetime.now(last_open.tzinfo) if last_open.tzinfo else datetime.now()
            diff = (now - last_open).total_seconds()
            if diff >= 15:
                return jsonify({"can_open": True})
            else:
                return jsonify({"can_open": False, "seconds_left": 15 - diff})
        else:
            return jsonify({"can_open": True})
    except Exception as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        cursor.close()
        conn.close()

@documents_bp.route('/report', methods=['POST'])
def report_document():
    try:
        data = request.json
        user_id = data.get('user_id')
        document_id = data.get('document_id')
        report_content = data.get('report_content')

        if not user_id or not document_id or not report_content:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO document_reports (user_id, document_id, report_content)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (user_id, document_id, report_content))
        conn.commit()
        return jsonify({"message": "Report submitted successfully"}), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()
@documents_bp.route('/api/check-ip-blocked', methods=['GET'])
def check_ip_blocked():
    # Lấy IP client; nếu bạn deploy sau proxy/nginx, có thể cần dùng X-Forwarded-For
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM ip_blocks WHERE ip_address = %s LIMIT 1",
            (ip,)
        )
        blocked = cursor.fetchone() is not None
    finally:
        cursor.close()
        conn.close()

    return jsonify({ "blocked": blocked })
@documents_bp.route('/get_verification_info', methods=['GET'])
def get_verification_info():
    try:
        # Giả định user_id được lấy từ session
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Unauthorized, please log in"}), 401

        # Lấy kết nối từ pool
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Truy vấn để lấy bản ghi gần nhất có status = 'rejected'
        query = """
            SELECT status, uploaded_at, note
            FROM user_images
            WHERE user_id = %s AND status = 'rejected'
            ORDER BY uploaded_at DESC
            LIMIT 1
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        # Đóng cursor và kết nối
        cursor.close()
        conn.close()

        # Kiểm tra nếu không có dữ liệu
        if not result:
            return jsonify({
                "message": "Chưa có thông tin xác thực nào bị từ chối.",
                "status": None,
                "last_rejected_time": None,
                "note": None
            }), 200

        # Xử lý dữ liệu trả về
        last_rejected_time = result['uploaded_at'].strftime('%d/%m/%Y %H:%M')
        note = result['note'] if result['note'] else "Không có ghi chú"

        # Trả về thông tin cần thiết
        response = {
            "status": result['status'],
            "last_rejected_time": last_rejected_time,
            "note": note
        }
        return jsonify(response), 200

    except mysql.connector.Error as db_error:
        return jsonify({"error": f"Database error: {str(db_error)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
@documents_bp.route('/api/user_images')
def api_user_images():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, user_id, image_path, note, uploaded_at FROM user_images WHERE status = 'normal'"
    cursor.execute(query)
    images = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(images)

# Route cập nhật ghi chú cho một ảnh
@documents_bp.route('/update_image_note', methods=['POST'])
def update_image_note():
    image_id = request.form.get('image_id')
    new_note = request.form.get('note', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE user_images SET note = %s WHERE id = %s"
    cursor.execute(query, (new_note, image_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Ghi chú của ảnh đã được cập nhật thành công'})
@documents_bp.route('/handle_approval', methods=['POST'])
def handle_approval1111():
    image_id = request.form.get('image_id')
    action = request.form.get('action')
    note = request.form.get('note', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Lấy user_id từ bảng user_images dựa theo image_id
    cursor.execute("SELECT user_id FROM user_images WHERE id = %s", (image_id,))
    result = cursor.fetchone()
    if not result:
        cursor.close()
        conn.close()
        return jsonify({'status': 'error', 'message': 'Không tìm thấy yêu cầu'}), 404

    user_id = result['user_id']

    if action == 'approve':
        # Cập nhật account_status của user thành 'đã duyệt'
        cursor.execute("UPDATE users SET account_status = 'đã duyệt' WHERE id = %s", (user_id,))
        # Xóa TẤT CẢ các yêu cầu của user đó trong bảng user_images
        cursor.execute("DELETE FROM user_images WHERE user_id = %s", (user_id,))
        # Tạo thông báo hệ thống cho user
        system_message = "Yêu cầu xác thực tài khoản của bạn đã được duyệt."
        cursor.execute(
            "INSERT INTO notifications (user_id, type, action) VALUES (%s, 'system', %s)",
            (user_id, system_message)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Yêu cầu đã được duyệt và tất cả yêu cầu của user đã được xóa.'})
    
    elif action == 'reject':
        # Cập nhật trạng thái của TẤT CẢ các yêu cầu của user thành 'rejected' và cập nhật ghi chú
        cursor.execute("UPDATE user_images SET status = 'rejected', note = %s WHERE user_id = %s", (note, user_id))
        # Chuyển trạng thái của user trong bảng users về 'bình thường'
        cursor.execute("UPDATE users SET account_status = 'bình thường' WHERE id = %s", (user_id,))
        # Tạo thông báo hệ thống cho user với lí do từ chối
        system_message = "Yêu cầu xác thực tài khoản của bạn đã bị từ chối. Lí do: " + note
        cursor.execute(
            "INSERT INTO notifications (user_id, type, action) VALUES (%s, 'system', %s)",
            (user_id, system_message)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Yêu cầu đã bị từ chối, lí do đã được lưu và trạng thái user đã chuyển về bình thường.'})
    
    else:
        cursor.close()
        conn.close()
        return jsonify({'status': 'error', 'message': 'Hành động không hợp lệ.'}), 400
