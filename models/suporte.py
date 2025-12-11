from utils import db

class suporte(db.Model, UserMixin):
    __tablename__= "suporte"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mensagem = db.Column(db.String(100))


    def __init__(self, nome, email, mensagem):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem
      
    def __repr__(self):
        return "<Usuario {}>".format(self.id)