import os
from flask_cors import CORS

# Cấu hình Flask
SECRET_KEY = 'your-secret-key-here'
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# Cấu hình CORS
CORS_ORIGINS = ["https://dethihocphan.com/"]
CORS_SUPPORTS_CREDENTIALS = True

# Cấu hình thư mục upload
UPLOAD_FOLDER = 'static/exams'
UPLOAD_FOLDER_V2 = os.path.join('static', 'xacthuctaikhoan')
EXAM_UPLOAD_DIR = os.path.join('exam_donggop')
DISCUSSION_UPLOAD_FOLDER = os.path.join('static', 'thaoluan')
FEEDBACK_UPLOAD_FOLDER = 'uploads'

# Định dạng file được phép
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg', 'jpeg', 'gif', 'txt', 'zip', 'rar', '7z', 'ppt', 'pptx'}

# Cấu hình database
DB_CONFIG = {
    'host': 'localhost',
    'user': 'mmddllg_huehub',
    'password': 'Ngoctruong123@',
    'database': 'mmddllg_huehub',
    'charset': 'utf8mb4'
}

# Cấu hình API Gemini
API_KEY = "AIzaSyD9EAIhLpfgpV120ygqPizMs2tKkqVmnow"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"