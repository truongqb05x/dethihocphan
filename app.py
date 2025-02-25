import sys
from flask import Flask, request, jsonify, session, render_template
import mysql.connector
from flask import Flask, render_template, session, redirect, url_for
from flask import Flask, request, abort, send_from_directory
from datetime import datetime, timezone

app = Flask(__name__, static_folder='static', static_url_path='/static')


from mysql.connector import pooling
from werkzeug.security import generate_password_hash
import os
import logging


import bcrypt
import requests
from flask_cors import CORS
from flask import Flask, request, jsonify
from mysql.connector import pooling, Error
from datetime import datetime

CORS(app)
from flask import send_from_directory
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
@app.route('/document')
def testtt():
    return send_from_directory('html', 'tailieu.html')
@app.route('/handbook')
def handbook_sinhvien():
    return send_from_directory('html', 'camnangsinhvien.html')

@app.route('/home')
def home():
    return send_from_directory('html', 'dethi.html')

@app.route('/exam')
def dethi():
    return send_from_directory('html', 'dethi.html')
@app.route('/lecturer-info')
def connect_lecturer_info():
    return send_from_directory('html', 'connect.html')


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


# Đường dẫn thư mục lưu ảnh (static/exams)
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'exams')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Thêm dòng này để khai báo cấu hình
@app.route('/api/examsview', methods=['GET'])
def get_exam1s():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Lấy tham số tìm kiếm
    search = request.args.get('search', '').strip()

    if search:
        # Nếu có từ khóa tìm kiếm, lọc tiêu đề và chỉ lấy loại "Đề thi"
        query = """
            SELECT id, title, image_url, views, identifier 
            FROM exam_contributions 
            WHERE title LIKE %s AND type = 'Đề thi'
        """
        cursor.execute(query, (f"%{search}%",))
        exams = cursor.fetchall()

        # Sắp xếp theo năm giảm dần
        exams.sort(key=lambda exam: extract_year(exam[1]), reverse=True)
    else:
        # Nếu không có từ khóa, trả về danh sách "Đề thi" mặc định
        query = "SELECT id, title, image_url, views, identifier FROM exam_contributions WHERE type = 'Đề thi' ORDER BY id ASC"
        cursor.execute(query)
        exams = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify([{
        'id': exam[0],
        'title': exam[1],
        'images': exam[2].split(','),  # Tách các đường dẫn ảnh bằng dấu phẩy
        'views': exam[3],  # Lấy views từ cơ sở dữ liệu
        'identifier': exam[4]  # Thêm mã định danh cho mỗi đề thi
    } for exam in exams])
# @app.route('/api/documentsview', methods=['GET'])
# def get_documents():
#     connection = get_db_connection()
#     cursor = connection.cursor()

#     # Lấy tham số tìm kiếm
#     search = request.args.get('search', '').strip()

#     if search:
#         # Nếu có từ khóa tìm kiếm, lọc tiêu đề và chỉ lấy loại "Đề thi"
#         query = """
#             SELECT id, title, image_url, views, identifier 
#             FROM exam_contributions 
#             WHERE title LIKE %s AND type = 'Tài liệu'
#         """
#         cursor.execute(query, (f"%{search}%",))
#         exams = cursor.fetchall()

#         # Sắp xếp theo năm giảm dần
#         exams.sort(key=lambda exam: extract_year(exam[1]), reverse=True)
#     else:
#         # Nếu không có từ khóa, trả về danh sách "Đề thi" mặc định
#         query = "SELECT id, title, image_url, views, identifier FROM exam_contributions WHERE type = 'Tài liệu' ORDER BY id ASC"
#         cursor.execute(query)
#         exams = cursor.fetchall()

#     cursor.close()
#     connection.close()

#     return jsonify([{
#         'id': exam[0],
#         'title': exam[1],
#         'images': exam[2].split(','),  # Tách các đường dẫn ảnh bằng dấu phẩy
#         'views': exam[3],  # Lấy views từ cơ sở dữ liệu
#         'identifier': exam[4]  # Thêm mã định danh cho mỗi đề thi
#     } for exam in exams])

def extract_year(title):
    """Trích xuất năm từ tiêu đề."""
    import re
    match = re.search(r'\b(20\d{2})\b', title)
    return int(match.group(1)) if match else 0

@app.route('/report_error', methods=['POST'])
def report_error():
    # Lấy dữ liệu từ request
    exam_id = request.json.get('exam_id')
    user_id = request.json.get('user_id')
    error_message = request.json.get('error_message')

    # Kiểm tra xem tất cả các thông tin cần thiết có được cung cấp không
    if not exam_id or not error_message:
        return jsonify({'error': 'Missing exam_id or error_message'}), 400

    try:
        # Kết nối đến cơ sở dữ liệu
        conn = get_db_connection()
        cursor = conn.cursor()

        # Thực thi câu lệnh SQL để chèn báo lỗi vào bảng error_reports
        query = """
        INSERT INTO error_reports (exam_id, user_id, error_message, report_date)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (exam_id, user_id, error_message, datetime.now()))
        conn.commit()

        # Đóng kết nối
        cursor.close()
        conn.close()

        return jsonify({'message': 'Error report submitted successfully'}), 201
    except Exception as e:
        return jsonify({'error': f'Error saving report: {str(e)}'}), 500


@app.route('/api/exam-contributions', methods=['GET'])
def get_exam_contributions():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Lấy tham số tìm kiếm (nếu có)
    search = request.args.get('search', '').strip()

    if search:
        # Nếu có từ khóa tìm kiếm, lọc tiêu đề và chỉ lấy loại "Tài liệu"
        query = """
            SELECT id, title, image_url, views, identifier 
            FROM exam_contributions 
            WHERE title LIKE %s AND type = 'Tài liệu'
        """
        cursor.execute(query, (f"%{search}%",))
        documents = cursor.fetchall()

    else:
        # Nếu không có từ khóa tìm kiếm, chỉ trả về danh sách "Tài liệu"
        query = "SELECT id, title, image_url, views, identifier FROM exam_contributions WHERE type = 'Tài liệu' ORDER BY id ASC"
        cursor.execute(query)
        documents = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify([{
        'id': document[0],
        'title': document[1],
        'images': document[2].split(','),  # Tách các đường dẫn ảnh bằng dấu phẩy
        'views': document[3],  # Lấy views từ cơ sở dữ liệu
        'identifier': document[4]  # Thêm mã định danh cho mỗi tài liệu
    } for document in documents])

@app.route('/api/exams/count_last_24h', methods=['GET'])
def count_recent_exams():
    query = """
    SELECT COUNT(*) AS exam_count
    FROM exam_contributions
    WHERE created_at >= NOW() - INTERVAL 1 DAY
    AND type = 'Đề thi';
    """
    
    connection = None
    try:
        # Lấy kết nối từ pool
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        
        # Lấy kết quả
        result = cursor.fetchone()
        return jsonify({"exam_count": result[0]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if connection:
            connection.close()
@app.route('/api/documents/count_last_24h', methods=['GET'])
def count_recent_documents():
    query = """
    SELECT COUNT(*) AS document_count
    FROM exam_contributions
    WHERE created_at >= NOW() - INTERVAL 1 DAY
    AND type = 'Tài liệu';
    """
    
    connection = None
    try:
        # Lấy kết nối từ pool
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        
        # Lấy kết quả
        result = cursor.fetchone()
        return jsonify({"document_count": result[0]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if connection:
            connection.close()

@app.route('/api/exams/<int:exam_id>/increment_views', methods=['POST'])
def increment_views(exam_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Tăng lượt xem của đề thi
        cursor.execute("UPDATE exam_contributions SET views = views + 1 WHERE id = %s", (exam_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'success': True, 'message': 'Lượt xem đã được tăng thành công.'})
    except Exception as e:
        print(f"Lỗi khi tăng lượt xem: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

import random
import string
import os
from flask import Flask, request, jsonify

# Hàm tạo mã định danh ngẫu nhiên cho mỗi lần upload
def generate_identifier(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
@app.route('/api/exams', methods=['POST'])
def upload_exam():
    title = request.form['title']
    images = request.files.getlist('image')  # Lấy tất cả các tệp ảnh từ form

    if title and images:
        # Tạo thư mục nếu chưa tồn tại
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # Tạo mã định danh duy nhất cho lần tải lên (chung cho tất cả các file)
        identifier = generate_identifier()

        # Xác định type dựa trên hai chữ đầu của title
        if title[:6] == "Đề thi":
            exam_type = "Đề thi"
        else:
            exam_type = "Tài liệu"

        # Kết nối với cơ sở dữ liệu
        connection = get_db_connection()
        cursor = connection.cursor()

        # Thêm đề thi vào bảng exam_contributions và gán identifier chung
        cursor.execute("INSERT INTO exam_contributions (title, identifier, type) VALUES (%s, %s, %s)", (title, identifier, exam_type))
        connection.commit()

        # Lấy ID của đề thi vừa được thêm vào
        exam_id = cursor.lastrowid
        
        image_urls = []

        # Lưu các ảnh vào thư mục và thu thập đường dẫn ảnh
        for image in images:
            # Đặt tên file với mã định danh, ví dụ: "ABC123_image1.jpg"
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{identifier}_{image.filename}")
            image.save(image_filename)
            image_url = os.path.join('static', 'exams', f"{identifier}_{image.filename}")
            image_urls.append(image_url)
        
        # Lưu tất cả các đường dẫn ảnh vào cột image_url, phân tách bằng dấu phẩy
        image_urls_str = ",".join(image_urls)
        
        # Cập nhật lại bảng exam_contributions với các đường dẫn ảnh và định danh
        cursor.execute("UPDATE exam_contributions SET image_url = %s WHERE id = %s", (image_urls_str, exam_id))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Đề thi và ảnh đã được tải lên!", "identifier": identifier}), 201
    else:
        return jsonify({"message": "Vui lòng điền đủ thông tin!"}), 400


# Đường dẫn thư mục lưu ảnh (static/exams)
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'exams')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Thêm dòng này để khai báo cấu hình
from werkzeug.utils import secure_filename  # Thêm dòng này để import secure_filename

# Kiểm tra loại file hợp lệ
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/contribute_exam', methods=['POST'])
def contribute_exam():
    # Kiểm tra nếu file được tải lên
    if 'exam_file' not in request.files:
        return jsonify({"error": "Chưa chọn file đề thi!"}), 400
    file = request.files['exam_file']
    
    # Kiểm tra file có hợp lệ không
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)  # Sử dụng secure_filename ở đây
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Kiểm tra và tạo thư mục nếu chưa có
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file.save(file_path)  # Lưu file vào thư mục

        # Nhận dữ liệu từ frontend
        data = request.form

        school = data.get('school')
        subject = data.get('subject')
        payment_account = data.get('payment_account')

        # Kết nối cơ sở dữ liệu và lưu dữ liệu vào bảng contributions
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO contributions (school, subject, payment_account, exam_file)
            VALUES (%s, %s, %s, %s)
        """, (school, subject, payment_account, file_path))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Đóng góp đề thi thành công!"}), 200
    else:
        return jsonify({"error": "File không hợp lệ. Vui lòng tải lên file JPG!"}), 400

import logging
from flask import session, jsonify
import requests

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app.secret_key = 'your_secret_key_here'  # Ensure you have a secret key for session encryption

@app.route('/view_user', methods=['GET'])
def view_user():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Truy vấn ngẫu nhiên UID Facebook, họ tên và trường đại học
    logger.debug("Bước 1: Truy vấn thông tin người dùng")
    cursor.execute("SELECT uid_facebook, full_name, university, facebook_url, url_ig FROM users_info WHERE url_ig IS NOT NULL ORDER BY RAND() LIMIT 1")
    
    # Handling potential database issues (acci 126 - assuming it's related to MySQL access)
    try:
        user = cursor.fetchone()
    except Exception as e:
        logger.error(f"Database error: {e}")
        cursor.close()
        connection.close()
        return jsonify({'message': 'Database error'}), 500

    if user:
        logger.debug(f"Bước 2: Người dùng tìm thấy: {user['full_name']} ({user['uid_facebook']})")
        
        # Lưu UID vào session và cập nhật session ngay lập tức
        session['uid_facebook'] = user['uid_facebook']
        session.modified = True  # Ensure session is saved immediately

        cursor.close()
        connection.close()

        # Lấy ảnh đại diện từ Facebook bằng API Graph
        logger.debug("Bước 5: Lấy ảnh đại diện từ Facebook API")
        access_token = "EAAAAUaZA8jlABO2J5h2bqABKGVBW5jUaRM1PJCBOWCZBwUNQ6UtgZArpfU8aVxDxUAdu21yNqyHGnnZAr7CIZCbXaGMh35A0Lb9tHZAG58oC469L02gpyZBpoKk9b7ydzcVgisKP193PRZBw4I5u9wITWKdixJZApTI1GoPbX55lnv10ZAuOZBLRQljNHjghHhImVkuNVCNfb5FrwZDZD"
        fb_api_url = f"https://graph.facebook.com/{user['uid_facebook']}/picture?type=large&access_token={access_token}"

        return jsonify({
            'uid_facebook': user['uid_facebook'],
            'full_name': user['full_name'],
            'university': user['university'],
            'facebook_url': user['facebook_url'],
            'url_ig': user['url_ig'],
            'avatar_url': fb_api_url,
        })
    else:
        cursor.close()
        connection.close()
        logger.debug("Bước 6: Không tìm thấy người dùng.")
        return jsonify({'message': 'No user found'}), 404

@app.route('/api/exam-count', methods=['GET'])
def get_exam_count():
    try:
        # Lấy kết nối từ pool
        connection = get_db_connection()
        cursor = connection.cursor()

        # Truy vấn số lượng đề thi
        query = "SELECT COUNT(*) FROM exam_contributions"
        cursor.execute(query)
        exam_count = cursor.fetchone()[0]

        return jsonify({"exam_count": exam_count}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/faq-items', methods=['GET'])
def get_faq_items():
    connection = get_db_connection()  # Lấy kết nối từ pool
    cursor = connection.cursor(dictionary=True)  # Cursors sử dụng dictionary
    cursor.execute("SELECT * FROM faq_items")  # Truy vấn bảng faq_items
    faq_items = cursor.fetchall()  # Lấy tất cả kết quả
    cursor.close()  # Đóng cursor
    connection.close()  # Trả lại kết nối vào pool
    
    return jsonify(faq_items)
    
    
@app.route('/api/faq-items/<int:item_id>/increment-views', methods=['POST'])
def increment_views_faq(item_id):
    try:
        connection = get_db_connection()  # Lấy kết nối từ pool
        cursor = connection.cursor()
        # Tăng số lượt xem
        cursor.execute("UPDATE faq_items SET views = views + 1 WHERE id = %s", (item_id,))
        connection.commit()  # Lưu thay đổi vào database
        cursor.close()
        connection.close()
        return jsonify({"message": "Views incremented successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/exam_questions/<int:exam_id>', methods=['GET'])
def get_exam_questions(exam_id):
    # Sử dụng kết nối và cursor từ get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Lấy thông tin câu hỏi từ bảng `questions` cho đề thi
    cursor.execute('''
        SELECT q.id AS question_id, q.question_text, a.id AS answer_id, a.answer_text, a.is_correct
        FROM questions q
        LEFT JOIN answers a ON q.id = a.question_id
        WHERE q.exam_contribution_id = %s
    ''', (exam_id,))

    questions_and_answers = cursor.fetchall()

    # Đảm bảo đóng kết nối và cursor sau khi sử dụng
    cursor.close()
    conn.close()

    # Tổ chức dữ liệu theo cấu trúc dễ hiểu
    exam_data = {}
    for row in questions_and_answers:
        question_id = row['question_id']
        if question_id not in exam_data:
            exam_data[question_id] = {
                'question_text': row['question_text'],
                'answers': []
            }
        answer = {
            'answer_id': row['answer_id'],
            'answer_text': row['answer_text'],
            'is_correct': row['is_correct']
        }
        exam_data[question_id]['answers'].append(answer)

    # Trả về dữ liệu dưới dạng JSON
    return jsonify(exam_data)
@app.route('/api/exams/<int:exam_id>/solution', methods=['GET'])
def get_exam_solution(exam_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Truy vấn thông tin lời giải từ bảng exam_contributions
    cursor.execute('SELECT title, solution FROM exam_contributions WHERE id = %s', (exam_id,))
    exam = cursor.fetchone()

    if exam:
        return jsonify({
            'title': exam['title'],
            'content': exam['solution']  # Lấy nội dung lời giải từ trường 'solution'
        })
    else:
        return jsonify({'message': 'Bài thi không tồn tại'}), 404
@app.route('/api/exams/<int:exam_id>/questions_with_answers', methods=['GET'])
def get_exam_questions_with_answers(exam_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Truy vấn thông tin câu hỏi và câu trả lời từ bảng `exam_contributions`, `questions`, `answers`
    cursor.execute('''
        SELECT ec.title AS exam_title, 
               q.id AS question_id, q.question_text, 
               a.id AS answer_id, a.answer_text, a.is_correct
        FROM exam_contributions ec
        JOIN questions q ON ec.id = q.exam_contribution_id
        LEFT JOIN answers a ON q.id = a.question_id
        WHERE ec.id = %s
    ''', (exam_id,))

    # Lấy dữ liệu
    questions_and_answers = cursor.fetchall()

    # Đảm bảo đóng kết nối và cursor sau khi sử dụng
    cursor.close()
    conn.close()

    # Tổ chức dữ liệu theo cấu trúc dễ hiểu
    exam_data = {}
    for row in questions_and_answers:
        # Dữ liệu đề thi
        exam_data['exam_title'] = row['exam_title']

        # Ensure the question_id is a string
        question_id = str(row['question_id'])
        if question_id not in exam_data:
            exam_data[question_id] = {
                'question_text': row['question_text'],
                'answers': []
            }
        
        # Câu trả lời
        answer = {
            'answer_id': row['answer_id'],
            'answer_text': row['answer_text'],
            'is_correct': bool(row['is_correct'])  # Ensure is_correct is a boolean
        }
        exam_data[question_id]['answers'].append(answer)

    # Trả về dữ liệu dưới dạng JSON
    return jsonify(exam_data)

# Route xử lý form khi người dùng nhấn "Lưu Thông Tin"
@app.route('/submit_question', methods=['POST'])
def submit_question():
    # Lấy dữ liệu từ form
    question_title = request.form['question-title']
    article_details = request.form['article-details']
    explanation = request.form['explanation']
    step_by_step_explanation = request.form['step-by-step-explanation']
    algorithm = request.form['algorithm']
    sample_code = request.form['sample-code']

    # Kết nối và lưu vào cơ sở dữ liệu
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    INSERT INTO programming_questions (question_title, article_details, explanation, step_by_step_explanation, algorithm, sample_code)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (question_title, article_details, explanation, step_by_step_explanation, algorithm, sample_code)

    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

    # Trả về thông báo thành công dưới dạng JSON
    return jsonify({"message": "Câu hỏi đã được lưu thành công!", "status": "success"}), 200

@app.route('/api/questions', methods=['GET'])
def get_all_questions():
    # Kết nối tới cơ sở dữ liệu
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Truy vấn lấy toàn bộ dữ liệu từ bảng 'programming_questions'
    cursor.execute('SELECT * FROM programming_questions')
    
    # Lấy tất cả kết quả
    questions = cursor.fetchall()

    cursor.close()
    connection.close()

    # Trả về dữ liệu dưới dạng JSON
    return jsonify(questions)
@app.route('/api/questions', methods=['GET'])
def get_questions():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Lấy id, tiêu đề câu hỏi và số lượt xem từ bảng programming_questions
    cursor.execute('SELECT id, question_title, view FROM programming_questions')
    questions = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return jsonify(questions)
@app.route('/api/questions/<int:question_id>', methods=['GET'])
def get_question_details(question_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Lấy thông tin câu hỏi từ bảng programming_questions theo id
    cursor.execute('SELECT * FROM programming_questions WHERE id = %s', (question_id,))
    question = cursor.fetchone()
    cursor.close()
    connection.close()

    if question:
        return jsonify({
            "question_title": question["question_title"],
            "explanation": question["explanation"],
            "article_details": question.get("article_details", "Chi tiết bài viết sẽ xuất hiện ở đây."),
            "algorithm": question.get("algorithm", "Thuật toán sẽ xuất hiện ở đây."),
            "sample_code": question.get("sample_code", "Code mẫu sẽ xuất hiện ở đây."),
            "step_by_step_explanation": question.get("step_by_step_explanation", "Giải thích từng bước sẽ xuất hiện ở đây."),
            "performance_comparison": question.get("performance_comparison", ""),
            "view": question["view"]  # Trả về số lượt xem
        })
    else:
        return jsonify({"message": "Câu hỏi không tồn tại"}), 404
@app.route('/api/questions/<int:question_id>/increase-view', methods=['POST'])
def increase_view(question_id):
    # Lógica của việc tăng lượt xem
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('UPDATE programming_questions SET view = view + 1 WHERE id = %s', (question_id,))
    connection.commit()

    # Lấy số lượt xem mới
    cursor.execute('SELECT view FROM programming_questions WHERE id = %s', (question_id,))
    updated_view = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return jsonify({"message": "View count updated", "new_view": updated_view})

# Route trả về page_number của mã định danh (browser_id)
@app.route('/get_page_number/<string:browser_id>', methods=['GET'])
def get_page_number(browser_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Lấy page_number dựa trên browser_id
        cursor.execute("SELECT page_number FROM browser_identifiers WHERE browser_id = %s;", (browser_id,))
        record = cursor.fetchone()  # Lấy một bản ghi duy nhất
        
        if record:
            return jsonify(record)  # Trả về giá trị của cột page_number
        else:
            return jsonify({"error": "Browser ID not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()
import logging

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
@app.route('/save_exam_info', methods=['POST'])
def save_exam_info():
    # Ghi log khi nhận được yêu cầu
    logging.debug("Đã nhận yêu cầu POST tại /save_exam_info")

    exam_id = request.json.get('exam_id')  # Chỉ lấy exam_id

    if exam_id:  # Kiểm tra chỉ cần exam_id
        try:
            # Kết nối đến cơ sở dữ liệu
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            # Câu lệnh SQL để chèn chỉ exam_id vào bảng exam_ids
            query = "INSERT INTO exam_ids (exam_id) VALUES (%s)"
            cursor.execute(query, (exam_id,))

            # Lưu thay đổi vào cơ sở dữ liệu
            connection.commit()

            # Đóng kết nối
            cursor.close()
            connection.close()

            return jsonify({"message": "Dữ liệu đã được lưu thành công."}), 200
        except Exception as e:
            logging.error(f"Lỗi khi lưu dữ liệu: {e}")
            return jsonify({"message": "Đã xảy ra lỗi khi lưu dữ liệu."}), 500
    else:
        logging.warning("Dữ liệu không hợp lệ.")
        return jsonify({"message": "Dữ liệu không hợp lệ."}), 400
@app.route('/api/lecturers', methods=['GET'])
def get_lecturers():
    # Kết nối với cơ sở dữ liệu
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Truy vấn dữ liệu từ bảng lecturers
    cursor.execute("SELECT * FROM lecturers")
    lecturers = cursor.fetchall()

    # Đóng kết nối
    cursor.close()
    connection.close()

    # Trả về dữ liệu dưới dạng JSON
    return jsonify(lecturers)


@app.route('/api/departments', methods=['GET'])
def get_departments():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Truy vấn lấy dữ liệu từ bảng departments_group
    cursor.execute('SELECT * FROM departments_group')
    
    # Lấy kết quả và đóng kết nối
    departments = cursor.fetchall()
    cursor.close()
    connection.close()
    
    # Trả về dữ liệu dưới dạng JSON
    return jsonify(departments)
@app.route('/api/courses', methods=['GET'])
def get_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Lấy tham số 'department' từ query string
    department_filter = request.args.get('department')

    # Truy vấn dữ liệu khóa học cùng với thông tin khoa và danh mục, áp dụng bộ lọc nếu có
    query = '''
    SELECT 
        courses.id, 
        courses.title, 
        courses.description, 
        courses.price, 
        courses.image_url, 
        courses.drive_link,  -- Thêm link khóa học
        departments.name AS department_name,
        GROUP_CONCAT(categories.name ORDER BY categories.name) AS category_names
    FROM courses_group AS courses
    LEFT JOIN departments_group AS departments ON courses.department_id = departments.id
    LEFT JOIN course_categories_group AS course_categories ON courses.id = course_categories.course_id
    LEFT JOIN categories_group AS categories ON course_categories.category_id = categories.id
    '''

    # Nếu có bộ lọc theo khoa, thêm điều kiện vào câu lệnh SQL
    if department_filter:
        query += ' WHERE departments.name = %s'
    
    query += ' GROUP BY courses.id'

    cursor.execute(query, (department_filter, ) if department_filter else ())
    courses = cursor.fetchall()

    # Truy vấn lấy các danh mục (nếu cần)
    cursor.execute('SELECT * FROM categories_group')
    categories = cursor.fetchall()

    cursor.close()
    conn.close()

    # Trả về khóa học và danh mục dưới dạng JSON
    return jsonify({"courses": courses, "categories": categories})
import os
import random
import string
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

import os
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import mysql.connector
import unidecode

app.config['IMAGE_UPLOAD_FOLDER'] = 'static/image_khoahoc'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """ Kiểm tra file có đúng định dạng ảnh không """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    """ Tạo tên file duy nhất để tránh ghi đè """
    name, ext = os.path.splitext(filename)
    unique_suffix = str(uuid.uuid4())[:8]  # Tạo chuỗi ngẫu nhiên 8 ký tự
    return f"{name}_{unique_suffix}{ext}"

def clean_filename(text):
    """ Xóa dấu tiếng Việt, chuyển về chữ thường, thay khoảng trắng bằng "_" """
    text = unidecode.unidecode(text)
    text = text.lower().replace(" ", "_")
    return "".join(c for c in text if c.isalnum() or c in {"_", "."})

@app.route('/add_data', methods=['POST'])
def add_data():
    """ Thêm khóa học mới vào cơ sở dữ liệu """
    department_name = request.form.get('department_name')
    category_name = request.form.get('category_name')
    course_title = request.form.get('course_title')
    course_description = request.form.get('course_description')
    course_price = request.form.get('course_price')
    course_link = request.form.get('course_link')
    file = request.files.get('course_image_file')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SET NAMES utf8mb4;")
        cursor.execute("SET CHARACTER SET utf8mb4;")
        cursor.execute("SET character_set_connection=utf8mb4;")

        cursor.execute("SELECT id FROM departments_group WHERE name = %s", (department_name,))
        department = cursor.fetchone()

        if not department:
            cursor.execute("INSERT INTO departments_group (name) VALUES (%s)", (department_name,))
            conn.commit()
            department_id = cursor.lastrowid
        else:
            department_id = department[0]

        image_url = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = generate_unique_filename(f"{clean_filename(course_title)}_{clean_filename(department_name)}_{filename}")
            file_path = os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], filename).replace('\\', '/')
            file.save(file_path)
            image_url = f"/{file_path}"

        cursor.execute("""
            INSERT INTO courses_group (title, description, price, department_id, image_url, drive_link)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (course_title, course_description, course_price, department_id, image_url, course_link))
        conn.commit()

        course_id = cursor.lastrowid

        cursor.execute("SELECT id FROM categories_group WHERE name = %s", (category_name,))
        category = cursor.fetchone()

        if not category:
            cursor.execute("INSERT INTO categories_group (name) VALUES (%s)", (category_name,))
            conn.commit()
            category_id = cursor.lastrowid
        else:
            category_id = category[0]

        cursor.execute("""
            INSERT INTO course_categories_group (course_id, category_id)
            VALUES (%s, %s)
        """, (course_id, category_id))
        conn.commit()

        return jsonify({
            'status': 'success',
            'message': 'Khóa học đã được thêm thành công!',
            'image_url': image_url
        })
    
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': f'Đã xảy ra lỗi: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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
    khoaMon = request.form.get("khoaMon")
    if not name or not khoaMon:
        return jsonify({"error": "Thiếu tên môn hoặc khoa"}), 400

    # Giả sử giá trị của khoaMon có dạng "khoa1", ta loại bỏ chữ "khoa" và chuyển thành số
    try:
        faculty_id = int(khoaMon.replace("khoa", ""))
    except Exception as e:
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

if __name__ == '__main__':

    app.run(port=8080, debug=True)