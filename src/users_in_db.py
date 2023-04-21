from werkzeug.security import check_password_hash, generate_password_hash
from db import ow_db

def insert_user(username, password):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    ow_db.session.execute(sql, {"username":username, "password":hash_value})
    ow_db.session.commit()

def check_username_password(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = ow_db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if not user:
        pass
        # TODO: invalid username
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            pass
            # TODO: correct username and password
        else:
            pass
            # TODO: invalid password