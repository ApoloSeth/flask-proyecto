from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    
    def __init__(self, id, nombre, email, password, is_admin = False):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
        
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"User {self.email}"
    
users = []

def get_user(email):
    for user in users:
        if user.email == email:
            return user
    return None