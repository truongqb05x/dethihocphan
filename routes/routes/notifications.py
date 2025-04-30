from flask import Blueprint, request, jsonify, session
from utils.db import get_db_connection
from datetime import datetime

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/api/notifications', methods=['GET'])
def get_notifications():
    if 'user_id' not in session:
        return jsonify({"error": "Bạn cần đăng nhập để xem thông báo"}), 401

    filter_type = request.args.get('type', 'all')
    user_id = session['user_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        if filter_type == 'all':
            query = """
                SELECT n.notification_id AS id, n.type, n.action, n.interaction, n.unread, 
                       n.created_at, u.fullname, NULL AS avatar, p.title AS post
                FROM notifications n
                LEFT JOIN users u ON n.user_id = u.id
                LEFT JOIN posts p ON n.post_id = p.post_id
                WHERE n.user_id = %s AND n.deleted_at IS NULL
                ORDER BY n.created_at DESC
            """
            cursor.execute(query, (user_id,))
        else:
            query = """
                SELECT n.notification_id AS id, n.type, n.action, n.interaction, n.unread, 
                       n.created_at, u.fullname, NULL AS avatar, p.title AS post
                FROM notifications n
                LEFT JOIN users u ON n.user_id = u.id
                LEFT JOIN posts p ON n.post_id = p.post_id
                WHERE n.user_id = %s AND n.type = %s AND n.deleted_at IS NULL
                ORDER BY n.created_at DESC
            """
            cursor.execute(query, (user_id, filter_type))
        
        notifications = cursor.fetchall()
        
        now = datetime.now()
        for noti in notifications:
            time_diff = now - noti['created_at']
            if time_diff.days > 7:
                noti['time'] = f"{time_diff.days // 7} tuần trước"
            elif time_diff.days > 0:
                noti['time'] = f"{time_diff.days} ngày trước"
            elif time_diff.seconds > 3600:
                noti['time'] = f"{time_diff.seconds // 3600} giờ trước"
            else:
                noti['time'] = f"{time_diff.seconds // 60} phút trước"
            del noti['created_at']
        
        return jsonify(notifications)
    finally:
        cursor.close()
        conn.close()

@notifications_bp.route('/api/notifications/<int:id>/read', methods=['POST'])
def mark_notification_read(id):
    if 'user_id' not in session:
        return jsonify({"error": "Bạn cần đăng nhập để thực hiện hành động này"}), 401

    user_id = session['user_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE notifications SET unread = FALSE WHERE notification_id = %s AND user_id = %s"
        cursor.execute(query, (id, user_id))
        if cursor.rowcount == 0:
            return jsonify({"error": "Thông báo không tồn tại hoặc không thuộc về bạn"}), 404
        conn.commit()
        return jsonify({"message": "Notification marked as read"}), 200
    finally:
        cursor.close()
        conn.close()

@notifications_bp.route('/api/notifications/<int:id>', methods=['DELETE'])
def delete_notification(id):
    if 'user_id' not in session:
        return jsonify({"error": "Bạn cần đăng nhập để thực hiện hành động này"}), 401

    user_id = session['user_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE notifications SET deleted_at = NOW() WHERE notification_id = %s AND user_id = %s"
        cursor.execute(query, (id, user_id))
        if cursor.rowcount == 0:
            return jsonify({"error": "Thông báo không tồn tại hoặc không thuộc về bạn"}), 404
        conn.commit()
        return jsonify({"message": "Notification deleted"}), 200
    finally:
        cursor.close()
        conn.close()

@notifications_bp.route('/api/notifications/read-all', methods=['POST'])
def mark_all_read():
    if 'user_id' not in session:
        return jsonify({"error": "Bạn cần đăng nhập để thực hiện hành động này"}), 401

    user_id = session['user_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE notifications SET unread = FALSE WHERE unread = TRUE AND deleted_at IS NULL AND user_id = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        return jsonify({"message": "All notifications marked as read"}), 200
    finally:
        cursor.close()
        conn.close()

@notifications_bp.route('/api/notifications/<int:id>/update-details', methods=['GET'])
def get_update_details(id):
    if 'user_id' not in session:
        return jsonify({"error": "Bạn cần đăng nhập để xem chi tiết cập nhật"}), 401

    user_id = session['user_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        check_query = "SELECT user_id FROM notifications WHERE notification_id = %s"
        cursor.execute(check_query, (id,))
        result = cursor.fetchone()
        if not result or str(result['user_id']) != str(user_id):
            return jsonify({"error": "Thông báo không tồn tại hoặc không thuộc về bạn"}), 404

        query = """
            SELECT su.version, su.update_date AS date,
                   ud.detail_id, ud.type, ud.description AS text
            FROM system_updates su
            LEFT JOIN update_details ud ON su.update_id = ud.update_id
            WHERE su.notification_id = %s
        """
        cursor.execute(query, (id,))
        details = cursor.fetchall()
        
        if not details:
            return jsonify({"error": "No update details found"}), 404
        
        result = {
            "version": details[0]["version"],
            "date": details[0]["date"].strftime("%d/%m/%Y"),
            "changes": [{"type": d["type"], "text": d["text"]} for d in details if d["type"]]
        }
        
        return jsonify(result)
    finally:
        cursor.close()
        conn.close()