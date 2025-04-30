from flask import Blueprint, request, jsonify, session, send_from_directory
from werkzeug.utils import secure_filename
from utils.db import get_db_connection
from utils.helpers import time_ago
from config.config import DISCUSSION_UPLOAD_FOLDER
import os

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/get-data', methods=['GET'])
def get_data():
    try:
        document_id = request.args.get('document_id', type=int)
        if document_id is None:
            return jsonify({"error": "document_id không được cung cấp"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT
                c.id, c.content, c.created_at, c.user_id, c.parent_id,
                u.fullname AS user_full_name, u.username,
                a.file_url, a.file_name, a.file_type
            FROM Comments c
            LEFT JOIN users u ON c.user_id = u.id
            LEFT JOIN (
                SELECT
                    comment_id,
                    MAX(file_url) AS file_url,
                    MAX(file_name) AS file_name,
                    MAX(file_type) AS file_type
                FROM Attachments
                GROUP BY comment_id
            ) a ON c.id = a.comment_id
            WHERE c.document_id = %s
            ORDER BY c.created_at DESC
        """
        cursor.execute(query, (document_id,))
        comments = cursor.fetchall()

        cursor.execute("SELECT * FROM Likes")
        likes = cursor.fetchall()

        likes_by_comment = {}
        for like in likes:
            cid = like['comment_id']
            likes_by_comment.setdefault(cid, []).append(like)

        for comment in comments:
            comment['user_full_name'] = comment.get('user_full_name') or comment.get('username') or 'Ẩn danh'
            comment['likes'] = likes_by_comment.get(comment['id'], [])
            comment['likes_count'] = len(comment['likes'])
            comment['liked_by_user'] = any(
                like['user_id'] == session.get('user_id')
                for like in comment['likes']
            )
            if comment['created_at']:
                comment['time_ago'] = time_ago(comment['created_at'])
            else:
                comment['time_ago'] = "Không xác định"

        return jsonify({
            "comments": comments,
            "current_user": {
                "full_name": session.get('full_name'),
                "avatar": session.get('avatar_url')
            }
        }), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@comments_bp.route('/comment', methods=['POST'])
def post_comment():
    try:
        user_id = request.form.get('user_id')
        document_id = request.form.get('document_id')
        content = request.form.get('content')

        if not user_id or not document_id or not content:
            return jsonify({"error": "Missing required fields"}), 400

        file_url = None
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                os.makedirs(DISCUSSION_UPLOAD_FOLDER, exist_ok=True)
                file_path = os.path.join(DISCUSSION_UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                file_url = f"/{file_path}"

        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO Comments (document_id, user_id, parent_id, content)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (document_id, user_id, None, content))
        comment_id = cursor.lastrowid

        if file_url:
            sql_attach = """
                INSERT INTO Attachments (comment_id, file_name, file_type, file_url)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_attach, (comment_id, file.filename, file.content_type, file_url))

        conn.commit()
        return jsonify({
            "message": "Comment posted successfully",
            "comment_id": comment_id,
            "file_url": file_url
        }), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@comments_bp.route('/static/thaoluan/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(DISCUSSION_UPLOAD_FOLDER, filename)

@comments_bp.route('/reply', methods=['POST'])
def post_reply():
    try:
        user_id = request.form.get('user_id')
        parent_id = request.form.get('parent_id')
        document_id = request.form.get('document_id')
        content = request.form.get('content')

        if not user_id or not parent_id or not document_id or not content:
            return jsonify({"error": "Missing required fields"}), 400

        file_url = None
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                os.makedirs(DISCUSSION_UPLOAD_FOLDER, exist_ok=True)
                filename = f"{parent_id}_{file.filename}"
                file_path = os.path.join(DISCUSSION_UPLOAD_FOLDER, filename)
                file.save(file_path)
                file_url = f"/{file_path}"

        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO Comments (document_id, user_id, parent_id, content)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (document_id, user_id, parent_id, content))
        reply_id = cursor.lastrowid

        if file_url:
            sql_attach = """
                INSERT INTO Attachments (comment_id, file_name, file_type, file_url)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_attach, (reply_id, file.filename, file.content_type, file_url))

        conn.commit()
        return jsonify({
            "message": "Reply posted successfully",
            "reply_id": reply_id,
            "file_url": file_url
        }), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@comments_bp.route('/like', methods=['POST'])
def like_comment():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        comment_id = data.get('comment_id')
        action = data.get('action')

        if not user_id or not comment_id or not action:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        if action == 'like':
            sql = """
                INSERT INTO Likes (user_id, comment_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE created_at = CURRENT_TIMESTAMP
            """
            cursor.execute(sql, (user_id, comment_id))
        elif action == 'unlike':
            sql = "DELETE FROM Likes WHERE user_id = %s AND comment_id = %s"
            cursor.execute(sql, (user_id, comment_id))
        else:
            return jsonify({"error": "Invalid action"}), 400

        conn.commit()
        return jsonify({"message": "Like updated successfully"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@comments_bp.route('/comments/count', methods=['GET'])
def get_comment_count():
    try:
        document_id = request.args.get('document_id', type=int)
        if document_id is None:
            return jsonify({"error": "document_id không được cung cấp"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT COUNT(*) AS total FROM Comments WHERE document_id = %s"
        cursor.execute(query, (document_id,))
        result = cursor.fetchone()
        return jsonify({"count": result["total"]})
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()