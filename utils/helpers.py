import hashlib
from datetime import datetime, timezone, timedelta
from config.config import ALLOWED_EXTENSIONS

def hash_password(password):
    """Mã hóa mật khẩu bằng SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def allowed_file(filename):
    """Kiểm tra định dạng file hợp lệ"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def time_ago(time_obj):
    """Tính thời gian tương đối"""
    if isinstance(time_obj, str):
        try:
            time_obj = datetime.fromisoformat(time_obj.replace('Z', '+00:00'))
        except ValueError:
            return "Không xác định"

    now = datetime.now(timezone.utc)
    if time_obj.tzinfo is None:
        local_tz = timezone(timedelta(hours=7))  # Múi giờ Việt Nam
        time_obj = time_obj.replace(tzinfo=local_tz).astimezone(timezone.utc)

    diff = now - time_obj
    seconds = diff.total_seconds()

    if seconds < 60:
        return f"{int(seconds)} giây trước"
    elif seconds < 3600:
        return f"{int(seconds / 60)} phút trước"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} giờ trước"
    elif seconds < 2592000:
        return f"{int(seconds / 86400)} ngày trước"
    elif seconds < 31536000:
        return f"{int(seconds / 2592000)} tháng trước"
    else:
        return f"{int(seconds / 31536000)} năm trước"