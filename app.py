import sys
import os
import logging
from datetime import datetime, timezone
import hashlib
from flask import Flask, request, jsonify, session, render_template, redirect, url_for, abort, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import mysql.connector
from mysql.connector import pooling, Error

from werkzeug.security import generate_password_hash
import bcrypt
import requests
app = Flask(__name__, static_folder='static', static_url_path='/static')

CORS(app)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Đặt secret key cho Flask

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

@app.route('/home')
def home():
    return send_from_directory('html', 'dethi.html')

@app.route('/exam')
def dethi():
    return send_from_directory('html', 'dethi.html')

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
# Hàm mã hóa mật khẩu (sử dụng SHA-256)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
from datetime import timedelta
from flask import make_response

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Tên đăng nhập và mật khẩu là bắt buộc"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, hash_password(password)))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session.permanent = True  # Lưu phiên vĩnh viễn
            
            resp = make_response(jsonify({"message": "Đăng nhập thành công", "user": {"username": user['username']}}))
            resp.set_cookie('login_token', str(user['id']), max_age=30*24*60*60)  # Lưu cookie 30 ngày
            return resp, 200
        else:
            return jsonify({"error": "Tên đăng nhập hoặc mật khẩu không đúng"}), 401

    except mysql.connector.Error as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        cursor.close()
        conn.close()

# Route xử lý đăng ký
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    fullname = data.get('fullname')
    username = data.get('username')
    password = data.get('password')
    university = data.get('university')

    if not all([fullname, username, password, university]):
        return jsonify({"error": "Tất cả các trường là bắt buộc"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Kiểm tra xem username đã tồn tại chưa
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"error": "Tên đăng nhập đã tồn tại"}), 409

        # Thêm người dùng mới
        query = "INSERT INTO users (fullname, username, password, university) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (fullname, username, hash_password(password), university))
        conn.commit()

        return jsonify({"message": "Đăng ký thành công"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        cursor.close()
        conn.close()
# Route kiểm tra trạng thái đăng nhập
@app.route('/api/check-login', methods=['GET'])
def check_login():
    if 'user_id' in session:
        return jsonify({"loggedIn": True, "username": session['username']})

    # Nếu không có session, kiểm tra cookie
    user_id = request.cookies.get('login_token')
    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user_id  # Phục hồi session từ cookie
            session['username'] = user['username']
            return jsonify({"loggedIn": True, "username": user['username']})

    return jsonify({"loggedIn": False})
@app.route('/api/account_status', methods=['GET'])
def get_account_status():
    # Kiểm tra xem user đã đăng nhập hay chưa (user_id lưu trong session)
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User chưa đăng nhập"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT account_status FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result:
            return jsonify({
                "user_id": user_id,
                "account_status": result['account_status']
            }), 200
        else:
            return jsonify({"error": "User không tồn tại"}), 404

    except mysql.connector.Error as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    
    resp = make_response(jsonify({"message": "Đăng xuất thành công"}))
    resp.set_cookie('login_token', '', expires=0)  # Xóa cookie
    return resp, 200

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
          WHERE s.id IN (1, 2)
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
    document_type = request.args.get('type', 'exam')  # Mặc định là 'exam'
    conn = None
    cursor = None
    try:
        conn = pool.get_connection()
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
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/subjects/<int:subject_id>/documents_by_year', methods=['GET'])
def get_documents_by_subject_grouped(subject_id):
    document_type = request.args.get('type', 'exam')  # Mặc định là 'exam'
    conn = None
    cursor = None
    try:
        conn = pool.get_connection()
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
    school_id = request.args.get('school_id', type=int)
    faculty_id = request.args.get('faculty_id', type=int)
    
    conn = None
    cursor = None
    try:
        conn = pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Base query
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
        
        # Thêm điều kiện lọc theo trường/khoa
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
        print("Lỗi database:", str(e))  # Log lỗi
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
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

# upload
# --- Route lấy danh sách trường ---
@app.route('/api/get_schools_v2', methods=['GET'])
def get_schools_v2():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, name AS school_name FROM schools"
    cursor.execute(query)
    schools = cursor.fetchall()
    app.logger.debug("Schools: %s", schools)  # Sử dụng debug thay vì print
    cursor.close()
    conn.close()
    return jsonify(schools)

@app.route('/api/faculties_v2/<int:school_id>', methods=['GET'])
def get_faculties_v2(school_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Alias name thành faculty_name để khớp với frontend
    query = "SELECT id, name AS faculty_name FROM faculties WHERE school_id = %s"
    cursor.execute(query, (school_id,))
    faculties = cursor.fetchall()
    
    # Debug: in ra danh sách khoa
    app.logger.debug("Faculties for school_id %d: %s", school_id, faculties)
    
    cursor.close()
    conn.close()
    
    return jsonify(faculties)

@app.route('/api/subjects_v2/<int:faculty_id>', methods=['GET'])
def get_subjects_v2(faculty_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Alias name thành subject_name để khớp với frontend
    query = "SELECT id, name AS subject_name FROM subjects WHERE faculty_id = %s"
    cursor.execute(query, (faculty_id,))
    subjects = cursor.fetchall()
    
    # Debug: in ra danh sách môn học
    app.logger.debug("Subjects for faculty_id %d: %s", faculty_id, subjects)
    
    cursor.close()
    conn.close()
    
    return jsonify(subjects)
# Thư mục lưu file upload
UPLOAD_FOLDER = 'static/exams'
ALLOWED_EXTENSIONS = set(['pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg', 'jpeg', 'gif', 'txt', 'zip', 'rar', '7z', 'ppt', 'pptx'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload_v2', methods=['POST'])
def upload_document_v2():
    # Kiểm tra file có trong request không
    if 'fileInput' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['fileInput']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Tạo folder nếu chưa tồn tại
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_save_path)

        # Lấy các dữ liệu từ form
        subject_id = request.form.get("mon", type=int)  # Giá trị select "Chọn Môn" là subject_id
        
        # Lấy giá trị năm dưới dạng chuỗi, vì cột year là varchar
        year = request.form.get("nam")
        if not year:
            return jsonify({"error": "Thiếu năm"}), 400

        document_name = request.form.get("tenDeThi") or filename
        file_info = request.form.get("infoTitle") or ""
        loai = request.form.get("loai")
        # Chuyển đổi loại tài liệu: "deThi" -> exam, "taiLieu" -> syllabus
        if loai == "deThi":
            document_type = "exam"
        elif loai == "taiLieu":
            document_type = "syllabus"
        else:
            document_type = "exam"  # mặc định

        # Insert dữ liệu vào bảng documents
        conn = get_db_connection()
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO documents (subject_id, year, file_name, file_info, document_type, file_path)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (subject_id, year, document_name, file_info, document_type, file_save_path))
        conn.commit()
        inserted_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"message": "Upload successful", "document_id": inserted_id}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

# --- Route Thêm Trường ---
@app.route('/api/add_school_v2', methods=['POST'])
def add_school_v2():
    name = request.form.get("tenTruong")
    if not name:
        return jsonify({"error": "Thiếu tên trường"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO schools (name) VALUES (%s)"
    cursor.execute(query, (name,))
    conn.commit()
    school_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({"message": "Thêm trường thành công", "school_id": school_id}), 200

# --- Route Thêm Khoa ---
@app.route('/api/add_department_v2', methods=['POST'])
def add_department_v2():
    name = request.form.get("tenKhoa")
    truongKhoa = request.form.get("truongKhoa")
    if not name or not truongKhoa:
        return jsonify({"error": "Thiếu tên khoa hoặc trường"}), 400

    # Giả sử giá trị của truongKhoa có dạng "1-truong-a", ta lấy phần trước dấu '-' là id
    try:
        school_id = int(truongKhoa.split('-')[0])
    except Exception as e:
        return jsonify({"error": "Giá trị trường không hợp lệ"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO faculties (school_id, name) VALUES (%s, %s)"
    cursor.execute(query, (school_id, name))
    conn.commit()
    faculty_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({"message": "Thêm khoa thành công", "faculty_id": faculty_id}), 200

# --- Route Thêm Môn Học ---
@app.route('/api/add_subject_v2', methods=['POST'])
def add_subject_v2():
    name = request.form.get("tenMon")
    faculty_id = request.form.get("khoaMon")
    
    if not name or not faculty_id:
        return jsonify({"error": "Thiếu tên môn hoặc khoa"}), 400

    try:
        faculty_id = int(faculty_id)
    except ValueError:
        return jsonify({"error": "Giá trị khoa không hợp lệ"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO subjects (faculty_id, name) VALUES (%s, %s)"
    cursor.execute(query, (faculty_id, name))
    conn.commit()
    subject_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({"message": "Thêm môn học thành công", "subject_id": subject_id}), 200
def get_latest_exams():
    try:
        conn = get_db_connection()  # Lấy kết nối từ pool
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT file_name, file_path, created_at
        FROM documents
        WHERE document_type = 'exam'
        ORDER BY created_at DESC
        LIMIT 3
        """
        cursor.execute(query)
        exams = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return exams
    
    except Exception as e:
        app.logger.debug("Lỗi khi truy vấn database: %s", e)
        return []

@app.route('/api/latest-exams', methods=['GET'])
def latest_exams():
    exams = get_latest_exams()
    return jsonify(exams)
@app.route('/api/log-file-open', methods=['POST'])
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
        cursor.close()
        conn.close()
        return jsonify({"message": "Log recorded successfully"}), 200
    except Exception as e:
        # Ghi log lỗi nếu cần
        print("Error logging file open:", e)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
@app.route('/api/user-activity', methods=['GET'])
def get_user_activity():
    try:
        conn = get_db_connection()
        # Sử dụng cursor dạng dictionary để lấy dữ liệu dưới dạng dict
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT d.file_name, fol.opened_at
            FROM file_open_logs AS fol
            JOIN documents AS d ON fol.document_id = d.id
            ORDER BY fol.opened_at DESC
            LIMIT 3
        """
        cursor.execute(sql)
        activities = cursor.fetchall()
        cursor.close()
        conn.close()

        # Chuyển đổi đối tượng datetime sang chuỗi ISO nếu cần
        for activity in activities:
            if isinstance(activity['opened_at'], datetime):
                activity['opened_at'] = activity['opened_at'].isoformat()

        return jsonify(activities), 200
    except Exception as e:
        print("Error fetching user activity:", e)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/api/register_notification', methods=['POST'])
def register_notification():
    data = request.get_json()
    school_id = data.get('school_id')
    faculty_id = data.get('faculty_id')
    email = data.get('email')

    if not (school_id and faculty_id and email):
        return jsonify({"error": "Thiếu thông tin yêu cầu"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Giả sử bạn đã tạo bảng subscriptions để lưu đăng ký
    query = """
        INSERT INTO subscriptions (school_id, faculty_id, email)
        VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(query, (school_id, faculty_id, email))
        conn.commit()
    except Exception as e:
        app.logger.error("Lỗi khi lưu đăng ký: %s", e)
        conn.rollback()
        return jsonify({"error": "Lỗi khi lưu đăng ký"}), 500
    finally:
        cursor.close()
        conn.close()
    
    return jsonify({"message": "Đăng ký nhận thông báo thành công!"}), 200
# Thiết lập thư mục upload với tên biến khác: EXAM_UPLOAD_DIR
EXAM_UPLOAD_DIR = os.path.join(app.root_path, 'exam_donggop')
if not os.path.exists(EXAM_UPLOAD_DIR):
    os.makedirs(EXAM_UPLOAD_DIR)

@app.route('/api/upload_exam', methods=['POST'])
def upload_exam():
    # Lấy mã trường từ form
    school_id = request.form.get('field')
    if not school_id:
        return jsonify({'error': 'Chưa chọn trường'}), 400

    # Kiểm tra file upload
    if 'examFile[]' not in request.files:
        return jsonify({'error': 'Không có file upload'}), 400

    files = request.files.getlist('examFile[]')
    if not files:
        return jsonify({'error': 'Không có file nào được gửi'}), 400

    saved_files = []
    for file in files:
        if file.filename == '':
            continue
        # Làm sạch tên file
        filename = secure_filename(file.filename)
        file_path = os.path.join(EXAM_UPLOAD_DIR, filename)
        file.save(file_path)

        # Lưu thông tin file vào database
        try:
            conn = pool.get_connection()  # Giả sử bạn đã thiết lập connection pool
            cursor = conn.cursor()
            query = "INSERT INTO exam_donggop (school_id, filename, filepath) VALUES (%s, %s, %s)"
            cursor.execute(query, (school_id, filename, file_path))
            conn.commit()
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        saved_files.append({'filename': filename, 'filepath': file_path})
    
    return jsonify({'message': 'Upload thành công', 'files': saved_files})
upload_folder_v2 = os.path.join(app.root_path, 'static', 'xacthuctaikhoan')
app.config['UPLOAD_FOLDER_V2'] = upload_folder_v2
os.makedirs(upload_folder_v2, exist_ok=True)

@app.route('/upload_v2', methods=['POST'])
def upload_file_v2():
    # Kiểm tra file có trong request hay không
    if 'file' not in request.files:
        return jsonify({"error": "Không tìm thấy file upload"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Không có file nào được chọn"}), 400

    try:
        # Tạo tên file an toàn, thêm tiền tố theo type nếu có
        filename = secure_filename(file.filename)
        file_type = request.form.get('type', '')
        if file_type:
            filename = f"{file_type}_{filename}"
        
        # Lưu file vào thư mục đã chỉ định
        file_path = os.path.join(app.config['UPLOAD_FOLDER_V2'], filename)
        file.save(file_path)
        
        # Tạo đường dẫn tương đối để sử dụng trên web
        relative_path = f"/static/xacthuctaikhoan/{filename}"

        # Lưu thông tin file vào DB nếu người dùng đã đăng nhập (lấy user_id từ session)
        user_id = session.get('user_id')
        if user_id:
            conn = get_db_connection()
            # Sử dụng buffered cursor để tránh lỗi "Commands out of sync"
            cursor = conn.cursor(buffered=True)
            query = "INSERT INTO user_images (user_id, image_path) VALUES (%s, %s)"
            cursor.execute(query, (user_id, relative_path))
            conn.commit()
            cursor.close()
            conn.close()

        return jsonify({
            "message": "Upload thành công",
            "filepath": relative_path
        }), 200

    except Exception as e:
        return jsonify({"error": f"Lỗi khi lưu file: {str(e)}"}), 500
@app.route('/update_account_status_v2', methods=['POST'])
def update_account_status_v2():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User chưa đăng nhập"}), 401
    try:
        conn = get_db_connection()
        # Sử dụng buffered cursor để tránh lỗi "Commands out of sync"
        cursor = conn.cursor(buffered=True)
        query = "UPDATE users SET account_status = %s WHERE id = %s"
        cursor.execute(query, ("đang duyệt", user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Trạng thái tài khoản đã được cập nhật thành 'đang duyệt'"}), 200
    except Exception as e:
        return jsonify({"error": f"Lỗi khi cập nhật trạng thái tài khoản: {str(e)}"}), 500

if __name__ == '__main__':

    app.run(port=8080, debug=True)