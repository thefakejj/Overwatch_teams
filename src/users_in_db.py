from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import ow_db

def insert_user(username, password):
    hash_value = generate_password_hash(password)
    sql = text('INSERT INTO users (name, password) VALUES (:username, :password)')
    ow_db.session.execute(sql, {"username":username, "password":hash_value})
    ow_db.session.commit()

def check_username_password(username, password):
    sql = text('SELECT id, password FROM users WHERE name=:username')
    result = ow_db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
        # TODO: invalid username

    else:
        hash_value = user[1]
        if check_password_hash(hash_value, password):
            return True
            # TODO: correct username and password
        else:
            return False
            # TODO: invalid password