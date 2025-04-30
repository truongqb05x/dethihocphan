from flask import Blueprint, request, jsonify, session, make_response
from utils.db import get_db_connection
from utils.helpers import hash_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
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

        if not user:
            return jsonify({"error": "Tên đăng nhập hoặc mật khẩu không đúng"}), 401

        cursor.execute(
            "INSERT INTO user_activity_logs (user_id, activity_type, ip_address) VALUES (%s, %s, %s)",
            (user['id'], 'login', request.remote_addr)
        )
        conn.commit()

        session['user_id'] = user['id']
        session['username'] = user['username']
        session.permanent = True

        resp = make_response(jsonify({
            "message": "Đăng nhập thành công",
            "user": {"username": user['username']}
        }))
        resp.set_cookie(
            'login_token',
            str(user['id']),
            max_age=3*24*60*60,
            secure=False,
            httponly=True,
            samesite='None',
            path='/'
        )
        return resp, 200

    except Exception as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {err}"}), 500
    finally:
        cursor.close()
        conn.close()

@auth_bp.route('/api/register', methods=['POST'])
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
        cursor = conn.cursor(dictionary=True, buffered=True)

        cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"error": "Tên đăng nhập đã tồn tại"}), 409

        insert_user = """
            INSERT INTO users (fullname, username, password, university)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_user, (fullname, username, hash_password(password), university))
        conn.commit()
        user_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO user_activity_logs (user_id, activity_type, ip_address) VALUES (%s, %s, %s)",
            (user_id, 'register', request.remote_addr)
        )
        conn.commit()

        cursor.execute("""
            SELECT COUNT(*) AS member_number
            FROM users
            WHERE university = %s AND id <= %s
        """, (university, user_id))
        membership_number = cursor.fetchone()['member_number']

        cursor.execute("SELECT name FROM schools WHERE id = %s", (university,))
        school_row = cursor.fetchone()
        university_name = school_row['name'] if school_row else "Unknown"

        return jsonify({
            "message": "Đăng ký thành công",
            "membership_number": membership_number,
            "university": university_name
        }), 201

    except Exception as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {err}"}), 500
    finally:
        cursor.close()
        conn.close()

@auth_bp.route('/api/check-login', methods=['GET'])
def check_login():
    if 'user_id' in session:
        return jsonify({
            "loggedIn": True,
            "username": session['username'],
            "userId": session['user_id']
        })

    user_id = request.cookies.get('login_token')
    if user_id:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                session['user_id'] = user_id
                session['username'] = user['username']
                return jsonify({
                    "loggedIn": True,
                    "username": session['username'],
                    "userId": session['user_id']
                })
        finally:
            cursor.close()
            conn.close()

    return jsonify({"loggedIn": False})

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    
    resp = make_response(jsonify({"message": "Đăng xuất thành công"}))
    resp.set_cookie('login_token', '', expires=0)
    return resp, 200