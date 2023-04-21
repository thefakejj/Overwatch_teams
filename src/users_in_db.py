from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import ow_db

def user_exists(username):
    sql = text('SELECT * FROM users WHERE name=:username')
    result = ow_db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        return True

def insert_user(username, password):
    if not user_exists(username):
        hash_value = generate_password_hash(password)
        sql = text('INSERT INTO users (name, password) VALUES (:username, :password)')
        ow_db.session.execute(sql, {"username":username, "password":hash_value})
        ow_db.session.commit()
        return True
    else:
        return False


def check_username_password(username, password):
    if user_exists(username):
        sql = text('SELECT id, password FROM users WHERE name=:username')
        result = ow_db.session.execute(sql, {"username":username})
        user = result.fetchone()
        hash_value = user[1]
        return check_password_hash(hash_value, password)