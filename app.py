import logging
from flask import Flask, request, render_template, send_from_directory, abort
from config.config import SECRET_KEY, CORS_ORIGINS, CORS_SUPPORTS_CREDENTIALS
from flask_cors import CORS
from routes.auth import auth_bp
from routes.users import users_bp
from routes.schools import schools_bp
from routes.documents import documents_bp
from routes.feedback import feedback_bp
from routes.notifications import notifications_bp
from routes.comments import comments_bp

# Thiết lập logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = SECRET_KEY
app.config.update(
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True
)

# Cấu hình CORS
CORS(app, supports_credentials=CORS_SUPPORTS_CREDENTIALS, origins=CORS_ORIGINS)

# Đăng ký các Blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(schools_bp)
app.register_blueprint(documents_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(comments_bp)


@app.route('/static/image/<filename>')
def serve_image(filename):
    return send_from_directory('static/image', filename)

@app.route('/html/<path:filename>')
def send_html(filename):
    return send_from_directory('html', filename)

@app.route('/')
def index():
    if 'Mozilla' not in request.headers.get('User-Agent', ''):
        abort(403)
    return render_template('index.html')


@app.route('/login')
def dangnhap():
    return send_from_directory('html', 'login.html')

@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory('html', '404.html'), 404

if __name__ == '__main__':
    app.run(port=8080, debug=True)