from flask import Blueprint, request, jsonify, session
from utils.db import get_db_connection

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/account_status', methods=['GET'])
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

    except Exception as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        cursor.close()
        conn.close()

@users_bp.route('/update_account_status_v2', methods=['POST'])
def update_account_status_v2():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User chưa đăng nhập"}), 401

    try:
        user_id = int(user_id)
    except Exception:
        return jsonify({"error": "user_id không hợp lệ"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(buffered=True)
        
        update_query = "UPDATE users SET account_status = %s WHERE id = %s"
        cursor.execute(update_query, ("đang duyệt", user_id))
        
        if cursor.rowcount == 0:
            conn.rollback()
            return jsonify({"error": "Không tìm thấy user"}), 404

        conn.commit()
        return jsonify({"message": "Trạng thái tài khoản đã được cập nhật"}), 200
    except Exception as err:
        if conn:
            conn.rollback()
        return jsonify({"error": f"Lỗi hệ thống: {str(err)}"}), 500
    finally:
        cursor.close()
        conn.close()

@users_bp.route('/api/users/statistics', methods=['GET'])
def user_statistics():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
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
        return jsonify(stats), 200
    except Exception as err:
        return jsonify({"error": f"Lỗi cơ sở dữ liệu: {str(err)}"}), 500
    finally:
        cursor.close()
        conn.close()

@users_bp.route('/user/university', methods=['GET'])
def get_user_university():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized: User not logged in"}), 401
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
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
            return jsonify({"error": "User not found"}), 404
    finally:
        cursor.close()
        conn.close()

@users_bp.route('/membership_number', methods=['GET'])
def membership_number():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT university FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        university_id = user['university']
        cursor.execute("SELECT name FROM schools WHERE id = %s", (university_id,))
        school = cursor.fetchone()
        university_name = school['name'] if school else "Unknown"

        cursor.execute("""
            SELECT COUNT(*) AS member_number 
            FROM users 
            WHERE university = %s AND id <= %s
        """, (university_id, user_id))
        result = cursor.fetchone()
        membership_number = result['member_number']

        return jsonify({
            'membership_number': membership_number,
            'university': university_name
        })
    finally:
        cursor.close()
        conn.close()

@users_bp.route('/api/welcome_checked', methods=['GET'])
def get_welcome_checked():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT welcome_checked FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        
        if result is None:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'welcome_checked': result['welcome_checked']})
    finally:
        cursor.close()
        conn.close()

@users_bp.route('/api/update_welcome', methods=['POST'])
def update_welcome():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.get_json()
    if not data or 'welcome_checked' not in data:
        return jsonify({'error': 'Missing welcome_checked field'}), 400

    welcome_checked = data.get('welcome_checked')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE users SET welcome_checked = %s WHERE id = %s"
        cursor.execute(query, (welcome_checked, user_id))
        conn.commit()
        return jsonify({'success': True, 'welcome_checked': welcome_checked})
    except Exception as err:
        conn.rollback()
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()