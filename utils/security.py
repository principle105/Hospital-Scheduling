# Importing dependencies
import bcrypt

# Hashes a plain text password
def hash_password(p):
    p = p.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(p, salt)
    return hashed

# Authenticates password
def check_password(p,hash):
    p,hash = p.encode("utf-8"), hash.encode("utf-8")
    return True if bcrypt.checkpw(p,hash) else False