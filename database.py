from sqlalchemy.sql.expression import null
from werkzeug.security import generate_password_hash
from app import db
from flask_sqlalchemy import *

class signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phoneno = db.Column(db.String(12), nullable=False)
    cnic = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    resetCode = db.Column(db.Integer,default=None, nullable=False)

