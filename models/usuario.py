from utils import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__= "usuario"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(100))
    admin = db.Column(db.Integer)


    def __init__(self, nome, email, senha, admin):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.admin = admin

    def __repr__(self):
        return "<Usuario {}>".format(self.nome)