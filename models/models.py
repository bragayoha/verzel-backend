from config.config import db
from werkzeug.security import generate_password_hash, check_password_hash
from validate_docbr import CPF
from validate_email_address import validate_email

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    cars = db.relationship('Car', backref='user', lazy=True)

    def __init__(self, name, email, cpf, password):
        self.name = name
        self.set_email(email)
        self.set_cpf(cpf)
        self.set_password(password)

    def set_email(self, email):
        if not email_validator(email):
            raise ValueError('Invalid email format')
        self.email = email

    def set_cpf(self, cpf):
        if not cpf_validator(cpf):
            raise ValueError('Invalid CPF format')
        self.cpf = cpf

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'

def email_validator(email):
    return validate_email(email, verify=True)

def cpf_validator(cpf):
    cpf = CPF()
    return cpf.validate(cpf)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False) 
    image = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Car {self.brand} {self.model} {self.year}>'