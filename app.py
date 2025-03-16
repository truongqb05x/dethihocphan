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
@app.route('/get-private-html')
def get_private_html():
    try:
        with open('html/index.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        return {"html": html_content}
    except Exception as e:
        return {"error": str(e)}, 500

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
            # Ghi nhận hoạt động đăng nhập vào bảng user_activity_logs
            log_query = """
                INSERT INTO user_activity_logs (user_id, activity_type, ip_address)
                VALUES (%s, %s, %s)
            """
            cursor.execute(log_query, (user['id'], 'login', request.remote_addr))
            conn.commit()

            session['user_id'] = user['id']
            session['username'] = user['username']
            session.permanent = True  # Lưu phiên vĩnh viễn
            
            resp = make_response(jsonify({"message": "Đăng nhập thành công", "user": {"username": user['username']}}))
            resp.set_cookie('login_token', str(user['id']), max_age=3*24*60*60)  # Lưu cookie 3 ngày
            return resp, 200
        else:
            return jsonify({"error": "Tên đăng nhập hoặc mật khẩu không đúng"}), 401

    except mysql.connector.Error as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        cursor.close()
        conn.close()


# -----------------------------------------------------------------
# Route xử lý đăng ký người dùng
# Endpoint: /api/register
# Phương thức: POST
# Mô tả:
#   - Nhận dữ liệu đăng ký từ client (fullname, username, password, university)
#   - Kiểm tra đầy đủ các trường bắt buộc
#   - Kiểm tra xem username đã tồn tại trong cơ sở dữ liệu chưa
#   - Nếu chưa tồn tại, hash password và chèn người dùng mới vào bảng users
#   - Trả về thông báo thành công (201) hoặc lỗi tương ứng
# -----------------------------------------------------------------
@app.route('/api/register', methods=['POST'])
def register():
    # Lấy dữ liệu JSON từ request
    data = request.get_json()
    fullname = data.get('fullname')
    username = data.get('username')
    password = data.get('password')
    university = data.get('university')

    # Kiểm tra các trường bắt buộc
    if not all([fullname, username, password, university]):
        return jsonify({"error": "Tất cả các trường là bắt buộc"}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        # Sử dụng buffered cursor để tự động lấy hết các kết quả
        cursor = conn.cursor(buffered=True)

        # Kiểm tra xem username đã tồn tại chưa
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"error": "Tên đăng nhập đã tồn tại"}), 409

        # --- Phần kiểm tra IP ---
        ip_addr = request.remote_addr
        cursor.execute("SELECT * FROM user_activity_logs WHERE ip_address = %s", (ip_addr,))
        if cursor.fetchone():
            return jsonify({"error": "Đăng ký không thành công: IP đã được sử dụng"}), 409
        # --------------------------

        # Thêm người dùng mới vào bảng users (hash password để bảo mật)
        query = "INSERT INTO users (fullname, username, password, university) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (fullname, username, hash_password(password), university))
        conn.commit()
        user_id = cursor.lastrowid  # Lấy id của người dùng mới

        # Lưu log đăng kí vào bảng log (giả sử activity_type có giá trị 'register')
        log_query = """
            INSERT INTO user_activity_logs (user_id, activity_type, ip_address)
            VALUES (%s, %s, %s)
        """
        cursor.execute(log_query, (user_id, 'register', ip_addr))
        conn.commit()

        return jsonify({"message": "Đăng ký thành công"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


# -----------------------------------------------------------------
# Route kiểm tra trạng thái đăng nhập
# Endpoint: /api/check-login
# Phương thức: GET
# Mô tả:
#   - Kiểm tra session hiện tại có chứa thông tin user không
#   - Nếu không, kiểm tra cookie 'login_token' để phục hồi session
#   - Trả về trạng thái đăng nhập và username (nếu có)
# -----------------------------------------------------------------
@app.route('/api/check-login', methods=['GET'])
def check_login():
    # Nếu session đã chứa thông tin user, trả về loggedIn: True
    if 'user_id' in session:
        return jsonify({"loggedIn": True, "username": session['username']})

    # Nếu không có session, kiểm tra cookie 'login_token'
    user_id = request.cookies.get('login_token')
    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # Phục hồi session từ cookie
            session['user_id'] = user_id
            session['username'] = user['username']
            return jsonify({"loggedIn": True, "username": user['username']})

    # Nếu không tìm thấy thông tin đăng nhập, trả về loggedIn: False
    return jsonify({"loggedIn": False})


# -----------------------------------------------------------------
# Route lấy trạng thái tài khoản người dùng
# Endpoint: /api/account_status
# Phương thức: GET
# Mô tả:
#   - Lấy user_id từ session, nếu chưa đăng nhập trả về lỗi 401
#   - Truy vấn trạng thái tài khoản (account_status) từ bảng users
#   - Trả về user_id và account_status nếu thành công
# -----------------------------------------------------------------
@app.route('/api/account_status', methods=['GET'])
def get_account_status():
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


# -----------------------------------------------------------------
# Route đăng xuất người dùng
# Endpoint: /api/logout
# Phương thức: POST
# Mô tả:
#   - Xóa thông tin đăng nhập khỏi session
#   - Xóa cookie 'login_token'
#   - Trả về thông báo đăng xuất thành công
# -----------------------------------------------------------------
@app.route('/api/logout', methods=['POST'])
def logout():
    # Xóa user_id và username khỏi session
    session.pop('user_id', None)
    session.pop('username', None)
    
    # Tạo response và xóa cookie 'login_token'
    resp = make_response(jsonify({"message": "Đăng xuất thành công"}))
    resp.set_cookie('login_token', '', expires=0)
    return resp, 200


# -----------------------------------------------------------------
# Route lấy danh sách trường
# Endpoint: /api/schools
# Phương thức: GET
# Mô tả:
#   - Truy vấn danh sách trường từ bảng schools
#   - Tính số lượng khoa của từng trường
#   - Chỉ trả về các trường có id trong danh sách định sẵn (ví dụ: 1, 2, 5)
# -----------------------------------------------------------------
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
          WHERE s.id IN (1, 2,3,4,5)
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


# -----------------------------------------------------------------
# Route lấy danh sách khoa theo trường
# Endpoint: /api/schools/<int:school_id>/faculties
# Phương thức: GET
# Mô tả:
#   - Dựa vào school_id truyền từ URL, truy vấn danh sách khoa của trường đó
#   - Tính số lượng môn học của mỗi khoa
# -----------------------------------------------------------------
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


# -----------------------------------------------------------------
# Route lấy danh sách môn học theo khoa
# Endpoint: /api/faculties/<int:faculty_id>/subjects
# Phương thức: GET
# Mô tả:
#   - Lấy faculty_id từ URL và tham số 'type' từ query (mặc định là 'exam')
#   - Truy vấn danh sách môn học của khoa cùng với số lượng tài liệu của từng môn
# -----------------------------------------------------------------
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


# -----------------------------------------------------------------
# Route lấy danh sách tài liệu của môn học, nhóm theo năm
# Endpoint: /api/subjects/<int:subject_id>/documents_by_year
# Phương thức: GET
# Mô tả:
#   - Lấy subject_id từ URL và tham số 'type' từ query (mặc định là 'exam')
#   - Truy vấn danh sách tài liệu của môn học theo điều kiện và sắp xếp theo năm giảm dần
#   - Nhóm tài liệu theo năm và trả về dạng JSON
# -----------------------------------------------------------------
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
        # Nhóm tài liệu theo năm
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


# -----------------------------------------------------------------
# Route lấy danh sách tài liệu của môn học tại một năm cụ thể
# Endpoint: /api/subjects/<int:subject_id>/documents/<int:year>
# Phương thức: GET
# Mô tả:
#   - Lấy subject_id và year từ URL
#   - Truy vấn bảng documents với điều kiện subject_id và year
#   - Trả về danh sách tài liệu dưới dạng JSON
# -----------------------------------------------------------------
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


# -----------------------------------------------------------------
# Route tìm kiếm môn học
# Endpoint: /api/search/subjects
# Phương thức: GET
# Mô tả:
#   - Nhận từ khóa tìm kiếm (term) và các tham số lọc (school_id, faculty_id) từ query
#   - Xây dựng câu lệnh SQL với điều kiện LIKE và các điều kiện lọc nếu có
#   - Trả về danh sách môn học phù hợp dưới dạng JSON
# -----------------------------------------------------------------
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
        
        # Base query với điều kiện tìm kiếm theo tên môn học
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
        
        # Thêm điều kiện lọc theo school_id nếu có
        if school_id and school_id > 0:
            query += " AND sc.id = %s"
            params.append(school_id)
        # Thêm điều kiện lọc theo faculty_id nếu có
        if faculty_id and faculty_id > 0:
            query += " AND f.id = %s"
            params.append(faculty_id)
            
        query += " ORDER BY s.name"
        
        cursor.execute(query, params)
        subjects = cursor.fetchall()
        return jsonify(subjects)
        
    except Exception as e:
        print("Lỗi database:", str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# -----------------------------------------------------------------
# Route tìm kiếm tài liệu
# Endpoint: /api/search/documents
# Phương thức: GET
# Mô tả:
#   - Nhận từ khóa tìm kiếm (term) và document_type (exam hoặc syllabus) từ query
#   - Truy vấn bảng documents với điều kiện tìm kiếm theo tên file
#   - Nếu có document_type, thêm điều kiện lọc theo document_type
#   - Trả về kết quả dưới dạng JSON
# -----------------------------------------------------------------
@app.route('/api/search/documents', methods=['GET'])
def search_documents():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized: User not logged in'}), 401

    term = request.args.get('term', '')
    document_type = request.args.get('type', '')
    
    conn = None
    cursor = None
    try:
        conn = pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Lấy school_id của user
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
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# -----------------------------------------------------------------
# Route lấy danh sách trường - phiên bản 2
# Endpoint: /api/get_schools_v2
# Phương thức: GET
# Mô tả:
#   - Truy vấn bảng schools với alias name thành school_name để phù hợp với frontend
#   - Ghi log danh sách trường ra console (debug)
# -----------------------------------------------------------------
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


# -----------------------------------------------------------------
# Route lấy danh sách khoa - phiên bản 2
# Endpoint: /api/faculties_v2/<int:school_id>
# Phương thức: GET
# Mô tả:
#   - Lấy danh sách khoa theo school_id, đổi alias name thành faculty_name để tương thích với frontend
#   - Ghi log danh sách khoa ra console
# -----------------------------------------------------------------
@app.route('/api/faculties_v2/<int:school_id>', methods=['GET'])
def get_faculties_v2(school_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT id, name AS faculty_name FROM faculties WHERE school_id = %s"
    cursor.execute(query, (school_id,))
    faculties = cursor.fetchall()
    
    app.logger.debug("Faculties for school_id %d: %s", school_id, faculties)
    
    cursor.close()
    conn.close()
    
    return jsonify(faculties)


# -----------------------------------------------------------------
# Route lấy danh sách môn học - phiên bản 2
# Endpoint: /api/subjects_v2/<int:faculty_id>
# Phương thức: GET
# Mô tả:
#   - Lấy danh sách môn học theo faculty_id, đổi alias name thành subject_name để tương thích với frontend
#   - Ghi log danh sách môn học ra console
# -----------------------------------------------------------------
@app.route('/api/subjects_v2/<int:faculty_id>', methods=['GET'])
def get_subjects_v2(faculty_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT id, name AS subject_name FROM subjects WHERE faculty_id = %s"
    cursor.execute(query, (faculty_id,))
    subjects = cursor.fetchall()
    
    app.logger.debug("Subjects for faculty_id %d: %s", faculty_id, subjects)
    
    cursor.close()
    conn.close()
    
    return jsonify(subjects)


# -----------------------------------------------------------------
# Định nghĩa thư mục upload và các định dạng file cho phép
# UPLOAD_FOLDER: Thư mục lưu file upload
# ALLOWED_EXTENSIONS: Các phần mở rộng file được phép upload
# -----------------------------------------------------------------
UPLOAD_FOLDER = 'static/exams'
ALLOWED_EXTENSIONS = set(['pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg', 'jpeg', 'gif', 'txt', 'zip', 'rar', '7z', 'ppt', 'pptx'])

def allowed_file(filename):
    # Kiểm tra xem file có phần mở rộng hợp lệ không
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------------------------------------------------
# Route upload tài liệu - phiên bản 2
# Endpoint: /api/upload_v2
# Phương thức: POST
# Mô tả:
#   - Kiểm tra file upload có tồn tại và hợp lệ không
#   - Lưu file vào thư mục UPLOAD_FOLDER sau khi làm sạch tên file
#   - Lấy thông tin tài liệu từ form (subject, năm, tên đề thi, info, loại tài liệu)
#   - Chèn dữ liệu file vào bảng documents
#   - Trả về thông báo thành công cùng document_id
# -----------------------------------------------------------------
@app.route('/api/upload_v2', methods=['POST'])
def upload_document_v2():
    if 'fileInput' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['fileInput']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Tạo thư mục upload nếu chưa tồn tại
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_save_path)

        # Lấy dữ liệu từ form
        subject_id = request.form.get("mon", type=int)
        year = request.form.get("nam")
        if not year:
            return jsonify({"error": "Thiếu năm"}), 400

        document_name = request.form.get("tenDeThi") or filename
        file_info = request.form.get("infoTitle") or ""
        loai = request.form.get("loai")
        if loai == "deThi":
            document_type = "exam"
        elif loai == "taiLieu":
            document_type = "syllabus"
        else:
            document_type = "exam"

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


# -----------------------------------------------------------------
# Route thêm trường - phiên bản 2
# Endpoint: /api/add_school_v2
# Phương thức: POST
# Mô tả:
#   - Nhận tên trường từ form (tenTruong)
#   - Chèn tên trường mới vào bảng schools
#   - Trả về thông báo thành công và school_id
# -----------------------------------------------------------------
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


# -----------------------------------------------------------------
# Route thêm khoa - phiên bản 2
# Endpoint: /api/add_department_v2
# Phương thức: POST
# Mô tả:
#   - Nhận tên khoa (tenKhoa) và thông tin trường (truongKhoa) từ form
#   - Xử lý chuỗi truongKhoa để lấy school_id
#   - Chèn dữ liệu vào bảng faculties và trả về faculty_id
# -----------------------------------------------------------------
@app.route('/api/add_department_v2', methods=['POST'])
def add_department_v2():
    name = request.form.get("tenKhoa")
    truongKhoa = request.form.get("truongKhoa")
    if not name or not truongKhoa:
        return jsonify({"error": "Thiếu tên khoa hoặc trường"}), 400

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


# -----------------------------------------------------------------
# Route thêm môn học - phiên bản 2
# Endpoint: /api/add_subject_v2
# Phương thức: POST
# Mô tả:
#   - Nhận tên môn học (tenMon) và khoa (khoaMon) từ form
#   - Kiểm tra dữ liệu và chuyển đổi khoa thành kiểu int
#   - Chèn môn học mới vào bảng subjects và trả về subject_id
# -----------------------------------------------------------------
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


# -----------------------------------------------------------------
# Route log file open
# Endpoint: /api/log-file-open
# Phương thức: POST
# Mô tả:
#   - Nhận JSON chứa documentId khi một file được mở
#   - Ghi log vào bảng file_open_logs
#   - Trả về thông báo thành công hoặc lỗi nếu có
# -----------------------------------------------------------------
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
        print("Error logging file open:", e)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# -----------------------------------------------------------------
# Route lấy nhật ký hoạt động người dùng
# Endpoint: /api/user-activity
# Phương thức: GET
# Mô tả:
#   - Truy vấn bảng file_open_logs kết hợp với bảng documents
#   - Lấy thông tin file_name và thời gian mở (opened_at)
#   - Sắp xếp theo thời gian mở giảm dần, giới hạn kết quả (ví dụ: 3 dòng)
#   - Chuyển đổi datetime sang chuỗi ISO nếu cần
# -----------------------------------------------------------------
@app.route('/api/user-activity', methods=['GET'])
def get_user_activity():
    try:
        conn = get_db_connection()
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

        for activity in activities:
            if isinstance(activity['opened_at'], datetime):
                activity['opened_at'] = activity['opened_at'].isoformat()

        return jsonify(activities), 200
    except Exception as e:
        print("Error fetching user activity:", e)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# -----------------------------------------------------------------
# Route đăng ký nhận thông báo
# Endpoint: /api/register_notification
# Phương thức: POST
# Mô tả:
#   - Nhận dữ liệu JSON gồm school_id, faculty_id, email
#   - Kiểm tra tính đầy đủ của thông tin
#   - Chèn dữ liệu vào bảng subscriptions để lưu đăng ký nhận thông báo
# -----------------------------------------------------------------
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


# -----------------------------------------------------------------
# Thiết lập thư mục upload cho exam_donggop
# Nếu thư mục chưa tồn tại, tạo mới
# -----------------------------------------------------------------
EXAM_UPLOAD_DIR = os.path.join(app.root_path, 'exam_donggop')
if not os.path.exists(EXAM_UPLOAD_DIR):
    os.makedirs(EXAM_UPLOAD_DIR)


# -----------------------------------------------------------------
# Route upload bài thi (exam)
# Endpoint: /api/upload_exam
# Phương thức: POST
# Mô tả:
#   - Lấy mã trường từ form (field)
#   - Kiểm tra xem có file upload với key 'examFile[]' hay không
#   - Lặp qua các file upload, làm sạch tên file và lưu vào EXAM_UPLOAD_DIR
#   - Lưu thông tin file vào bảng exam_donggop trong cơ sở dữ liệu
#   - Trả về thông báo thành công và danh sách file đã lưu
# -----------------------------------------------------------------
@app.route('/api/upload_exam', methods=['POST'])
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
            conn = pool.get_connection()  # Sử dụng connection pool
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


# -----------------------------------------------------------------
# Thiết lập thư mục upload phiên bản 2 cho xác thực tài khoản
# Lưu file vào thư mục static/xacthuctaikhoan
# -----------------------------------------------------------------
upload_folder_v2 = os.path.join(app.root_path, 'static', 'xacthuctaikhoan')
app.config['UPLOAD_FOLDER_V2'] = upload_folder_v2
os.makedirs(upload_folder_v2, exist_ok=True)


# -----------------------------------------------------------------
# Route upload file (phiên bản 2) cho xác thực tài khoản
# Endpoint: /upload_v2
# Phương thức: POST
# Mô tả:
#   - Kiểm tra xem request có chứa file với key 'file' hay không
#   - Làm sạch tên file và thêm tiền tố nếu có tham số 'type'
#   - Lưu file vào thư mục UPLOAD_FOLDER_V2 và tạo đường dẫn tương đối
#   - Nếu người dùng đã đăng nhập, lưu thông tin file vào bảng user_images
#   - Trả về thông báo upload thành công và đường dẫn file
# -----------------------------------------------------------------
@app.route('/upload_v2', methods=['POST'])
def upload_file_v2():
    if 'file' not in request.files:
        return jsonify({"error": "Không tìm thấy file upload"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Không có file nào được chọn"}), 400

    try:
        filename = secure_filename(file.filename)
        file_type = request.form.get('type', '')
        if file_type:
            filename = f"{file_type}_{filename}"
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER_V2'], filename)
        file.save(file_path)
        
        relative_path = f"/static/xacthuctaikhoan/{filename}"

        user_id = session.get('user_id')
        if user_id:
            conn = get_db_connection()
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


# -----------------------------------------------------------------
# Route cập nhật trạng thái tài khoản - phiên bản 2
# Endpoint: /update_account_status_v2
# Phương thức: POST
# Mô tả:
#   - Kiểm tra người dùng đã đăng nhập chưa (dựa vào session)
#   - Cập nhật trạng thái tài khoản của user thành "đang duyệt" trong bảng users
#   - Trả về thông báo thành công hoặc lỗi nếu có
# -----------------------------------------------------------------
import logging
import traceback
from flask import request, jsonify, session

# Cấu hình logging (đặt ở đầu file, nếu chưa có)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/update_account_status_v2', methods=['POST'])
def update_account_status_v2():
    logger.debug("===== Bắt đầu xử lý /update_account_status_v2 =====")
    
    # Lấy user_id từ session
    user_id = session.get('user_id')
    logger.debug("Extracted user_id từ session: %s", user_id)
    if not user_id:
        logger.error("ERROR: User chưa đăng nhập")
        return jsonify({"error": "User chưa đăng nhập"}), 401

    try:
        user_id = int(user_id)  # Đảm bảo user_id là số nguyên
    except Exception as e:
        logger.error("ERROR: user_id không hợp lệ - %s", str(e))
        return jsonify({"error": "user_id không hợp lệ"}), 400

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(buffered=True)
        
        # Cập nhật trạng thái tài khoản
        update_query = "UPDATE users SET account_status = %s WHERE id = %s"
        cursor.execute(update_query, ("đang duyệt", user_id))
        logger.debug("Số dòng cập nhật: %s", cursor.rowcount)
        
        if cursor.rowcount == 0:
            logger.error("ERROR: Không tìm thấy user")
            conn.rollback()
            return jsonify({"error": "Không tìm thấy user"}), 404

        conn.commit()
        logger.debug("Cập nhật trạng thái thành công!")
        return jsonify({"message": "Trạng thái tài khoản đã được cập nhật"}), 200
    except Exception as e:
        if conn:
            conn.rollback()
        logger.exception("ERROR: Lỗi khi cập nhật trạng thái - %s", str(e))
        return jsonify({"error": f"Lỗi hệ thống: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()
# log hoạt động user
@app.route('/api/log-view-exam', methods=['POST'])
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
    except mysql.connector.Error as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        cursor.close()
        conn.close()
import datetime
from flask import jsonify, session, request

@app.route('/api/check-file-open-timer', methods=['GET'])
def check_file_open_timer():
    if 'user_id' not in session:
        return jsonify({"error": "User chưa đăng nhập"}), 401
    conn = None
    cursor = None
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
            last_open = result['last_open']  # datetime object
            now = datetime.datetime.now(last_open.tzinfo) if last_open.tzinfo else datetime.datetime.now()
            diff = (now - last_open).total_seconds()
            if diff >= 15:
                return jsonify({"can_open": True})
            else:
                return jsonify({"can_open": False, "seconds_left": 15 - diff})
        else:
            # Nếu chưa có log nào thì cho phép mở file
            return jsonify({"can_open": True})
    except mysql.connector.Error as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# get pr5
@app.route('/api/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        return jsonify({"error": "Người dùng chưa đăng nhập"}), 401

    try:
        conn = get_db_connection()

        # Query 1: Lấy thông tin người dùng, bao gồm họ tên và tên trường học
        # Giả sử cột "university" trong bảng users lưu trữ id của trường học
        cursor = conn.cursor()
        query_user = """
            SELECT u.fullname, s.name AS school_name
            FROM users u
            JOIN schools s ON u.university = s.id
            WHERE u.id = %s
        """
        cursor.execute(query_user, (session['user_id'],))
        user = cursor.fetchone()
        cursor.close()
        if not user:
            return jsonify({"error": "User not found"}), 404
        # user là tuple: (fullname, school_name)
        fullname, school_name = user

        # Query 2: Đếm số tài liệu đã xem (chỉ đếm activity_type 'view_exam')
        cursor = conn.cursor()
        query_viewed = """
            SELECT COUNT(*) 
            FROM user_activity_logs 
            WHERE user_id = %s AND activity_type = 'view_exam'
        """
        cursor.execute(query_viewed, (session['user_id'],))
        result_viewed = cursor.fetchone()
        cursor.close()
        viewed_count = result_viewed[0] if result_viewed else 0

        # Query 3: Lấy 5 hoạt động gần đây
        cursor = conn.cursor()
        query_activities = """
            SELECT activity_type, activity_time 
            FROM user_activity_logs 
            WHERE user_id = %s 
            ORDER BY activity_time DESC 
            LIMIT 5
        """
        cursor.execute(query_activities, (session['user_id'],))
        recent_activities = cursor.fetchall()
        cursor.close()

        # Chuyển đổi dữ liệu cho hoạt động gần đây
        activities = []
        for activity in recent_activities:
            act_type, act_time = activity
            if act_type == 'login':
                description = 'Đăng nhập hệ thống'
            elif act_type == 'view_exam':
                description = 'Đã xem đề thi'
            else:
                description = act_type
            formatted_time = act_time.strftime('%I:%M %p') if hasattr(act_time, 'strftime') else str(act_time)
            activities.append({
                "activity_type": act_type,
                "description": description,
                "activity_time": formatted_time
            })

        return jsonify({
            "fullname": fullname,
            "university": school_name,  # Trả về tên trường học thay vì id
            "viewed_count": viewed_count,
            "recent_activities": activities
        }), 200

    except mysql.connector.Error as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        conn.close()
# get log từ hệ thống
@app.route('/api/system-activities', methods=['GET'])
def system_activities():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Lấy thông tin hoạt động của tất cả người dùng,
        # mỗi loại hoạt động (activity_type) lấy 5 bản ghi,
        # bao gồm thông tin người dùng, trường và tên đề thi (nếu có)
        query = """
            WITH cte AS (
                SELECT 
                    u.id AS user_id, 
                    u.fullname, 
                    s.name AS school_name, 
                    ua.activity_type, 
                    ua.activity_time,
                    d.file_name AS document_name,
                    ROW_NUMBER() OVER (PARTITION BY ua.activity_type ORDER BY ua.activity_time DESC) as rn
                FROM user_activity_logs ua
                JOIN users u ON ua.user_id = u.id
                JOIN schools s ON u.university = s.id
                LEFT JOIN documents d ON ua.document_id = d.id
            )
            SELECT 
                user_id, fullname, school_name, activity_type, activity_time, document_name
            FROM cte
            WHERE rn <= 5
            ORDER BY activity_time DESC
        """
        cursor.execute(query)
        activities = cursor.fetchall()
        cursor.close()

        result = []
        for record in activities:
            act_time = record['activity_time']
            # Trả về thời gian đầy đủ ở định dạng ISO (nếu có thể)
            if hasattr(act_time, 'isoformat'):
                full_time = act_time.isoformat()
            else:
                full_time = str(act_time)
                
            act_type = record['activity_type']
            if act_type == 'login':
                description = 'Đăng nhập hệ thống'
            elif act_type == 'view_exam':
                if record.get('document_name'):
                    description = f'{record["document_name"]}'
                else:
                    description = ''
            elif act_type == 'register':
                description = ''
            else:
                description = act_type

            result.append({
                "user_id": record['user_id'],
                "fullname": record['fullname'],
                "school": record['school_name'],
                "activity_type": act_type,
                "description": description,
                "activity_time": full_time,  # trả về full timestamp
                "document_name": record.get("document_name")
            })

        return jsonify(result), 200

    except mysql.connector.Error as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        conn.close()
# get tài liệu mới nhất
import os

@app.route('/api/documents/latest', methods=['GET'])
def latest_documents():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Lấy 5 bản ghi tài liệu mới nhất theo thời gian tạo
        query = """
            SELECT 
                file_name, 
                document_type, 
                file_path, 
                created_at
            FROM documents
            ORDER BY created_at DESC
            LIMIT 5
        """
        cursor.execute(query)
        docs = cursor.fetchall()
        cursor.close()

        result = []
        for doc in docs:
            file_path = doc["file_path"]
            # Lấy kích thước file (bytes), nếu file không tồn tại trả về 0
            try:
                file_size = os.path.getsize(file_path)
            except Exception:
                file_size = 0
            # Chuyển đổi từ bytes sang MB
            file_size_mb = round(file_size / (1024 * 1024), 2)

            created_at = doc["created_at"]
            if hasattr(created_at, 'isoformat'):
                created_at = created_at.isoformat()
            else:
                created_at = str(created_at)

            result.append({
                "file_name": doc["file_name"],
                "created_at": created_at,
                "document_type": doc["document_type"],
                "file_size_mb": file_size_mb
            })

        return jsonify(result), 200

    except mysql.connector.Error as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        conn.close()
# get user theo trường
@app.route('/api/users/statistics', methods=['GET'])
def user_statistics():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Giả sử trường users.university lưu giá trị id của trường (mặc dù kiểu dữ liệu VARCHAR)
        query = """
            SELECT s.name AS school, COUNT(u.id) AS user_count
            FROM schools s
            LEFT JOIN users u ON u.university = s.id
            GROUP BY s.id
            HAVING COUNT(u.id) >= 1
            ORDER BY user_count DESC
        """
        cursor.execute(query)
        stats = cursor.fetchall()
        cursor.close()
        return jsonify(stats), 200

    except mysql.connector.Error as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        conn.close()
# API lấy danh sách ảnh dưới dạng JSON
@app.route('/api/user_images')
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
@app.route('/update_image_note', methods=['POST'])
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
@app.route('/handle_approval', methods=['POST'])
def handle_approval():
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
        # Xóa yêu cầu khỏi bảng user_images
        cursor.execute("DELETE FROM user_images WHERE id = %s", (image_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Yêu cầu đã được duyệt và xóa.'})
    elif action == 'reject':
        # Cập nhật trạng thái của yêu cầu thành 'rejected' và cập nhật ghi chú
        cursor.execute("UPDATE user_images SET status = 'rejected', note = %s WHERE id = %s", (note, image_id))
        # Chuyển trạng thái của user trong bảng users về 'bình thường'
        cursor.execute("UPDATE users SET account_status = 'bình thường' WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Yêu cầu đã bị từ chối, lí do đã được lưu và trạng thái user đã chuyển về bình thường.'})
    else:
        cursor.close()
        conn.close()
        return jsonify({'status': 'error', 'message': 'Hành động không hợp lệ.'}), 400

@app.route('/get_verification_info', methods=['GET'])
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
@app.route('/user/university', methods=['GET'])
def get_user_university():
    # Lấy user id từ session
    user_id = session.get('user_id')
    if not user_id:
        abort(401, description="Unauthorized: User not logged in")
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Giả sử users.university chứa mã của trường học (ID)
        query = """
            SELECT u.university, s.name AS school_name 
            FROM users u 
            LEFT JOIN schools s ON s.id = u.university
            WHERE u.id = %s
        """
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        if row:
            return jsonify({
                'user_id': user_id,
                'university': row['university'],
                'school_name': row['school_name']
            })
        else:
            abort(404, description="User not found")
    finally:
        cursor.close()
        conn.close()
@app.route('/api/accounts_by_ip', methods=['GET'])
def accounts_by_ip():
    ip_addr = request.remote_addr
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)
        # Lấy danh sách username từ các tài khoản có log tương ứng với IP hiện tại
        query = """
            SELECT DISTINCT u.username
            FROM users u
            JOIN user_activity_logs l ON u.id = l.user_id
            WHERE l.ip_address = %s
        """
        cursor.execute(query, (ip_addr,))
        results = cursor.fetchall()
        # Chỉ lấy username từ kết quả
        usernames = [row['username'] for row in results]
        return jsonify({
            "ip": ip_addr,
            "usernames": usernames
        }), 200

    except mysql.connector.Error as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
@app.route('/api/request_password_reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    
    # Kiểm tra các trường bắt buộc
    if not username or not email:
        return jsonify({"error": "Username và email là bắt buộc"}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()  # Hàm kết nối cơ sở dữ liệu của bạn
        cursor = conn.cursor()
        query = "INSERT INTO password_reset_requests (username, email) VALUES (%s, %s)"
        cursor.execute(query, (username, email))
        conn.commit()
        return jsonify({"message": "Yêu cầu cấp lại mật khẩu đã được ghi nhận. Vui lòng kiểm tra email."}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

if __name__ == '__main__':

    app.run(port=8080, debug=True)