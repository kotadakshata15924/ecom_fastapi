import bcrypt

def hash_password(password):
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password

def verify_password(req_pw, db_pw):
    return bcrypt.checkpw(req_pw.encode('utf-8'), db_pw)