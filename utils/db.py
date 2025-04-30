import mysql.connector
from mysql.connector import pooling
from config.config import DB_CONFIG

# Tạo connection pool
pool = pooling.MySQLConnectionPool(
    **DB_CONFIG,
    pool_name="mypool",
    pool_size=7
)

def get_db_connection():
    """Lấy kết nối từ pool"""
    return pool.get_connection()