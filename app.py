from flask import Flask, render_template, abort, jsonify, request
from jinja2 import TemplateNotFound
import mysql.connector
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import bcrypt
from flask import Flask, request, jsonify, session
from mysql.connector import Error
from flask import Flask, jsonify, request
import os
import math
from mysql.connector import Error
from werkzeug.utils import secure_filename

# Cấu hình kết nối đến MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'mmddllg_huehub',
    'password': 'Ngoctruong123@',
    'database': 'mmddllg_huehub',
    'charset': 'utf8mb4'
}


# Khởi tạo ứng dụng Flask
app = Flask(__name__, template_folder='templates_v2')
app.secret_key = 'your_secret_key'  # Nên là chuỗi bảo mật, dùng riêng tư

# Hàm tiện lợi để lấy kết nối
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirmPassword')

        # Input validation
        if not username or not password:
            return jsonify({'error': 'Tên đăng nhập và mật khẩu là bắt buộc'}), 400
        if password != confirm_password:
            return jsonify({'error': 'Mật khẩu không khớp'}), 400

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if username exists
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Tên đăng nhập đã tồn tại'}), 400

        # Insert new user
        cursor.execute(
            'INSERT INTO users (username, password) VALUES (%s, %s)',
            (username, hashed_password.decode('utf-8'))
        )
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'message': 'Đăng ký thành công'}), 201

    except mysql.connector.Error as db_err:
        return jsonify({'error': f'Lỗi cơ sở dữ liệu: {str(db_err)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Input validation
        if not username or not password:
            return jsonify({'error': 'Tên đăng nhập và mật khẩu là bắt buộc'}), 400

        # Database connection
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check user
        cursor.execute(
            'SELECT id, username, password FROM users WHERE username = %s',
            (username,)
        )
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            return jsonify({'error': 'Tên đăng nhập không tồn tại'}), 401

        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Lưu thông tin user vào session
            session['user_id'] = user['id']
            session['username'] = user['username']

            return jsonify({'message': 'Đăng nhập thành công', 'username': user['username']}), 200
        else:
            return jsonify({'error': 'Mật khẩu không đúng'}), 401

    except mysql.connector.Error as db_err:
        return jsonify({'error': f'Lỗi cơ sở dữ liệu: {str(db_err)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

# Hàm định dạng kích thước file
def format_file_size(size_bytes):
    if size_bytes == 0:
        return '0 KB'
    size_units = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    size = float(size_bytes)
    while size >= 1024 and i < len(size_units) - 1:
        size /= 1024
        i += 1
    return f"{size:.2f} {size_units[i]}"
@app.route('/check-session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'loggedIn': False}), 200

    # Kiểm tra user_id có trong CSDL không
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({
                'loggedIn': True,
                'user_id': user_id,
                'username': session.get('username')
            }), 200
        else:
            # user_id không tồn tại trong CSDL
            session.clear()  # Xóa session luôn cho chắc
            return jsonify({'loggedIn': False}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
# Hàm định dạng kích thước file
def format_file_size(size_bytes):
    if size_bytes == 0:
        return '0 KB'
    size_units = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    size = float(size_bytes)
    while size >= 1024 and i < len(size_units) - 1:
        size /= 1024
        i += 1
    return f"{size:.2f} {size_units[i]}"

# Route cho trang chủ, render file index.html
@app.route('/')
def index():
    return render_template('index.html')

# Route cho các trang tĩnh trong templates (không cần .html)
@app.route('/<page>')
def render_page(page):
    try:
        return render_template(f"{page}.html")
    except TemplateNotFound:
        abort(404)

# Calculate file size in human-readable format
def format_file_size(size_bytes):
    try:
        size_bytes = int(size_bytes) if size_bytes is not None else 0
        if size_bytes <= 0:
            return "0 KB"
        size_name = ("B", "KB", "MB", "GB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"
    except (ValueError, TypeError):
        return "0 KB"

# API to return list of schools with document stats
@app.route('/api/schools', methods=['GET'])
def api_schools():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.id, s.name, 
                  MAX(d.created_at) as latest_updated, 
                  SUM(d.file_size) as total_size,
                  COUNT(d.id) as document_count
            FROM schools s
            LEFT JOIN faculties f ON f.school_id = s.id
            LEFT JOIN subjects sub ON sub.faculty_id = f.id
            LEFT JOIN documents d ON d.subject_id = sub.id
            GROUP BY s.id, s.name
            ORDER BY s.name
        """)
        schools = cursor.fetchall()
        for school in schools:
            if school['latest_updated']:
                school['latest_updated'] = school['latest_updated'].strftime('%Y-%m-%d')
            school['total_size'] = format_file_size(school['total_size'])
            school['document_count'] = int(school['document_count'] or 0)
        cursor.close()
        conn.close()
        return jsonify(schools)
    except Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# API to return list of faculties for a given school with document stats
@app.route('/api/faculties', methods=['GET'])
def api_faculties():
    school_id = request.args.get('school_id', type=int)
    if not school_id:
        return jsonify({'error': 'school_id is required'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT f.id, f.name, 
                  MAX(d.created_at) as latest_updated, 
                  SUM(d.file_size) as total_size,
                  COUNT(d.id) as document_count
            FROM faculties f
            LEFT JOIN subjects sub ON sub.faculty_id = f.id
            LEFT JOIN documents d ON d.subject_id = sub.id
            WHERE f.school_id = %s
            GROUP BY f.id, f.name
            ORDER BY f.name
        """, (school_id,))
        faculties = cursor.fetchall()
        for faculty in faculties:
            if faculty['latest_updated']:
                faculty['latest_updated'] = faculty['latest_updated'].strftime('%Y-%m-%d')
            faculty['total_size'] = format_file_size(faculty['total_size'])
            faculty['document_count'] = int(faculty['document_count'] or 0)
        cursor.close()
        conn.close()
        return jsonify(faculties)
    except Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# API to return list of subjects for a given faculty with document stats
@app.route('/api/subjects', methods=['GET'])
def api_subjects():
    faculty_id = request.args.get('faculty_id', type=int)
    if not faculty_id:
        return jsonify({'error': 'faculty_id is required'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.id, s.name, 
                  MAX(d.created_at) as latest_updated, 
                  SUM(d.file_size) as total_size,
                  COUNT(d.id) as document_count
            FROM subjects s
            LEFT JOIN documents d ON d.subject_id = s.id
            WHERE s.faculty_id = %s
            GROUP BY s.id, s.name
            ORDER BY s.name
        """, (faculty_id,))
        subjects = cursor.fetchall()
        for subject in subjects:
            if subject['latest_updated']:
                subject['latest_updated'] = subject['latest_updated'].strftime('%Y-%m-%d')
            subject['total_size'] = format_file_size(subject['total_size'])
            subject['document_count'] = int(subject['document_count'] or 0)
        cursor.close()
        conn.close()
        return jsonify(subjects)
    except Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# API to return list of document types for a given subject
@app.route('/api/document_types', methods=['GET'])
def api_document_types():
    subject_id = request.args.get('subject_id', type=int)
    if not subject_id:
        return jsonify({'error': 'subject_id is required'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT document_type, 
                  MAX(created_at) as latest_updated, 
                  SUM(file_size) as total_size,
                  COUNT(id) as document_count
            FROM documents
            WHERE subject_id = %s
            GROUP BY document_type
            ORDER BY document_type
        """, (subject_id,))
        document_types = cursor.fetchall()
        for doc_type in document_types:
            if doc_type['latest_updated']:
                doc_type['latest_updated'] = doc_type['latest_updated'].strftime('%Y-%m-%d')
            doc_type['total_size'] = format_file_size(doc_type['total_size'])
            doc_type['document_count'] = int(doc_type['document_count'] or 0)
        cursor.close()
        conn.close()
        return jsonify(document_types)
    except Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# API to return list of years with documents for a given subject and document type
@app.route('/api/years', methods=['GET'])
def api_years():
    subject_id = request.args.get('subject_id', type=int)
    document_type = request.args.get('document_type')
    if not subject_id or not document_type:
        return jsonify({'error': 'subject_id and document_type are required'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT year, 
                  MAX(created_at) as latest_updated, 
                  SUM(file_size) as total_size,
                  COUNT(id) as document_count
            FROM documents
            WHERE subject_id = %s AND document_type = %s
            GROUP BY year
            ORDER BY year
        """, (subject_id, document_type))
        years = cursor.fetchall()
        for year in years:
            if year['latest_updated']:
                year['latest_updated'] = year['latest_updated'].strftime('%Y-%m-%d')
            year['total_size'] = format_file_size(year['total_size'])
            year['document_count'] = int(year['document_count'] or 0)
        cursor.close()
        conn.close()
        return jsonify(years)
    except Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# API to return list of documents
@app.route('/api/documents', methods=['GET'])
def api_documents():
    subject_id = request.args.get('subject_id', type=int)
    document_type = request.args.get('document_type')
    year = request.args.get('year')
    keyword = request.args.get('keyword', default='', type=str).strip()

    print(f"API /api/documents called with: subject_id={subject_id}, document_type={document_type}, year={year}, keyword={keyword}")

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if subject_id and document_type and year:
            query = (
                "SELECT d.id, d.file_name, d.file_path, d.document_type, "
                "d.created_at, d.year, "
                "s.name as subject_name, f.name as faculty_name, sc.name as school_name "
                "FROM documents d "
                "JOIN subjects s ON d.subject_id = s.id "
                "JOIN faculties f ON s.faculty_id = f.id "
                "JOIN schools sc ON f.school_id = sc.id "
                "WHERE d.subject_id = %s AND d.document_type = %s AND d.year = %s"
            )
            params = [subject_id, document_type, year]
        else:
            query = (
                "SELECT d.id, d.file_name, d.file_path, d.document_type, "
                "d.created_at, d.year, "
                "s.name as subject_name, f.name as faculty_name, sc.name as school_name "
                "FROM documents d "
                "JOIN subjects s ON d.subject_id = s.id "
                "JOIN faculties f ON s.faculty_id = f.id "
                "JOIN schools sc ON f.school_id = sc.id "
                "WHERE 1=1"
            )
            params = []

        if keyword:
            keywords = keyword.split()
            for kw in keywords:
                query += f" AND d.file_name LIKE %s"
                params.append(f"%{kw}%")

        if document_type and not (subject_id and year):
            query += " AND d.document_type = %s"
            params.append(document_type)

        query += " ORDER BY d.created_at DESC"

        print(f"Executing query: {query} with params: {params}")
        cursor.execute(query, params)
        documents = cursor.fetchall()
        print(f"Documents found: {len(documents)}")

        for doc in documents:
            if doc['created_at']:
                doc['created_at'] = doc['created_at'].strftime('%d/%m/%Y')
            try:
                if os.path.exists(doc['file_path']):
                    file_size = os.path.getsize(doc['file_path'])
                    doc['file_size'] = format_file_size(file_size)
                else:
                    doc['file_size'] = "0 KB"
            except (OSError, TypeError):
                doc['file_size'] = "0 KB"

        cursor.close()
        conn.close()
        return jsonify(documents)

    except Error as e:
        print(f"Database error: {str(e)}")
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(e)}"}), 500
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({"error": f"Lỗi máy chủ: {str(e)}"}), 500
# File upload configuration
UPLOAD_FOLDER = 'static/exam'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    # Allow all file formats
    return True

@app.route('/view_document', methods=['POST'])
def view_document():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Vui lòng đăng nhập để xem tài liệu'}), 401

        data = request.get_json()
        document_path = data.get('document_path')
        if not document_path:
            return jsonify({'error': 'document_path là bắt buộc'}), 400

        conn = get_db_connection()
        # Tạo cursor buffered để tránh lỗi "Unread result found"
        cursor = conn.cursor(buffered=True, dictionary=True)

        # 1. Lấy document_id từ documents
        cursor.execute(
            'SELECT id FROM documents WHERE file_path = %s',
            (document_path,)
        )
        doc = cursor.fetchone()
        # Với buffered cursor, nếu có thêm dòng (thực ra chỉ 1), không gây lỗi khi execute tiếp
        if not doc:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Tài liệu không tồn tại'}), 404

        document_id = doc['id']

        # 2. Kiểm tra đã xem chưa
        cursor.execute(
            'SELECT id FROM viewed_documents WHERE user_id = %s AND document_id = %s',
            (session['user_id'], document_id)
        )
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({
                'message': 'Tài liệu đã xem trước đó',
                'document_path': document_path
            }), 200

        # 3. Kiểm tra lượt xem còn lại
        cursor.execute(
            'SELECT luot_xem FROM users WHERE id = %s',
            (session['user_id'],)
        )
        user = cursor.fetchone()
        if not user:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Người dùng không tồn tại'}), 404
        if user['luot_xem'] <= 0:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Bạn đã hết lượt xem. Vui lòng đổi thêm lượt xem.'}), 403

        # 4. Trừ lượt xem và thêm bản ghi viewed_documents
        cursor.execute(
            'UPDATE users SET luot_xem = luot_xem - 1 WHERE id = %s',
            (session['user_id'],)
        )
        cursor.execute(
            'INSERT INTO viewed_documents (user_id, document_id) VALUES (%s, %s)',
            (session['user_id'], document_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'message': 'Tài liệu sẵn sàng',
            'document_path': document_path
        }), 200

    except mysql.connector.Error as db_err:
        if db_err.errno == 1062:
            return jsonify({
                'message': 'Tài liệu đã xem trước đó',
                'document_path': document_path
            }), 200
        return jsonify({'error': f'Lỗi cơ sở dữ liệu: {db_err}'}), 500

    except Exception as e:
        return jsonify({'error': f'Lỗi server: {e}'}), 500
@app.route('/api/viewed_documents', methods=['GET'])
def get_viewed_documents():
    # Kiểm tra login
    if 'user_id' not in session:
        return jsonify({'error': 'Vui lòng đăng nhập để xem danh sách tài liệu đã xem'}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Truy vấn join qua document_id, đã có d.document_type
        query = """
            SELECT 
                d.id AS document_id,
                d.file_path,
                d.file_name,
                d.file_size,
                d.year,
                d.document_type,
                vd.viewed_at,
                s.name AS subject_name,
                f.name AS faculty_name,
                sc.name AS school_name
            FROM viewed_documents vd
            JOIN documents d ON vd.document_id = d.id
            JOIN subjects s ON d.subject_id = s.id
            JOIN faculties f ON s.faculty_id = f.id
            JOIN schools sc ON f.school_id = sc.id
            WHERE vd.user_id = %s
            ORDER BY vd.viewed_at DESC
        """
        cursor.execute(query, (session['user_id'],))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        # Format response theo frontend
        viewed_list = []
        for row in rows:
            viewed_list.append({
                'id'           : row['document_id'],
                'name'         : row['file_name'],
                'file_type'    : get_file_type(row['file_name']),  # giữ phần mở rộng
                'size'         : format_file_size(row['file_size']),
                'purchaseDate' : row['viewed_at'].strftime('%d/%m/%Y'),
                'path'         : row['file_path'],
                'year'         : row['year'],
                'type'         : row['document_type'],             # exam|syllabus
                'subject_name' : row['subject_name'],
                'faculty_name' : row['faculty_name'],
                'school_name'  : row['school_name']
            })

        return jsonify(viewed_list), 200

    except mysql.connector.Error as db_err:
        return jsonify({'error': f'Lỗi cơ sở dữ liệu: {db_err}'}), 500
    except Exception as e:
        return jsonify({'error': f'Lỗi server: {e}'}), 500
def get_file_type(file_name):
    extension = file_name.split('.')[-1].lower()
    return {
        'pdf': 'PDF',
        'doc': 'Word',
        'docx': 'Word',
        'xls': 'Excel',
        'xlsx': 'Excel',
        'zip': 'ZIP',
        'rar': 'ZIP'
    }.get(extension, 'Unknown')

@app.route('/view', methods=['GET'])
def exchange_views():
    return jsonify({'message': 'Trang đổi lượt xem (chưa triển khai)'}), 200
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx'}
# Hàm kiểm tra file hợp lệ (ví dụ chỉ cho phép pdf, docx,...)
from datetime import datetime
@app.route('/api/upload_document', methods=['POST'])
def upload_document():
    try:
        # 1. Kiểm tra file
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400

        # 2. Lấy user_id
        user_id = request.form.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': 'Missing user_id'}), 400

        # 3. Lưu file lên server
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(file_path)
        file_size = os.path.getsize(file_path)

        # 4. Chèn vào bảng document_uploads (không cần document_id)
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO document_uploads (user_id, file_name, file_path, file_size, status, views_earned)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, filename, file_path, file_size, 'pending', 0))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'message': 'File uploaded and logged successfully',
            'filename': filename,
            'file_path': file_path,
            'file_size': file_size
        }), 200

    except mysql.connector.Error as db_err:
        return jsonify({'error': f'Database error: {db_err}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {e}'}), 500

@app.route('/api/contributions/<int:user_id>', methods=['GET'])
def get_contributions(user_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM document_uploads
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,))

        contributions = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(contributions), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/documents/pending', methods=['GET'])
def get_pending_documents():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            du.id as upload_id,
            du.file_name,
            du.file_size,
            du.status,
            du.created_at,
            u.id as user_id,
            u.username
        FROM document_uploads du
        JOIN users u ON du.user_id = u.id
        WHERE du.status = 'pending'
        ORDER BY du.created_at DESC
        """

        cursor.execute(query)
        documents = cursor.fetchall()

        for doc in documents:
            doc['file_size'] = f"{doc['file_size'] / 1024 / 1024:.2f}MB"
            doc['created_at'] = doc['created_at'].strftime('%d/%m/%Y')

        cursor.close()
        conn.close()

        return jsonify({'success': True, 'data': documents})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
@app.route('/api/documents/approve/<int:upload_id>', methods=['POST'])
def approve_document(upload_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Cập nhật trạng thái
        cursor.execute("""
            UPDATE document_uploads 
            SET status = 'approved'
            WHERE id = %s
        """, (upload_id,))

        # Lấy user_id từ document_uploads
        cursor.execute("""
            SELECT user_id FROM document_uploads WHERE id = %s
        """, (upload_id,))
        user_result = cursor.fetchone()
        if not user_result:
            raise Exception("Upload ID không tồn tại")
        user_id = user_result['user_id']

        # Tặng thêm 3 lượt xem
        cursor.execute("""
            UPDATE users 
            SET luot_xem = luot_xem + 3
            WHERE id = %s
        """, (user_id,))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True, 'message': 'Phê duyệt thành công'})

    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'error': str(e)}), 500
@app.route('/api/documents/reject/<int:upload_id>', methods=['POST'])
def reject_document(upload_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Cập nhật trạng thái
        cursor.execute("""
            UPDATE document_uploads 
            SET status = 'rejected'
            WHERE id = %s
        """, (upload_id,))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True, 'message': 'Từ chối tài liệu thành công'})

    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)