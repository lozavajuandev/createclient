from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()

class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.String(20), nullable=False, unique=True)
    document_type = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Client {self.first_name} {self.last_name}>"
    

class User(db.Model):
        __tablename__ = "users"
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(20), nullable=False, unique=True)
        password = db.Column(db.String(20), nullable=False)
        
        def __repr__(self):
            return f"<User {self.username}"