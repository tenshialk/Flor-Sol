from utils import db

class Suporte(db.Model):
    __tablename__ = "suporte"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(500), nullable=False) 
    email = db.Column(db.String(500), nullable=False)
    mensagem = db.Column(db.String(2000), nullable=False)

    def __init__(self,id, nome, email, mensagem):
        self.id = id
        self.nome = nome
        self.email = email
        self.mensagem = mensagem
    
           
    def __repr__(self):
        return f"<suporte_usuario{self.id, self.nome, self.email, self.mensagem}>"