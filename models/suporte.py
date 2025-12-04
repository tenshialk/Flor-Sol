from utils import db

class Suporte(db.Model):
    __tablename__ = "suporte"
    id = db.Column(db.Integer, primary_key=True)
    mensagem = db.Column(db.String(500), nullable=False)  

    def __init__(self,mensagem):
        self.mensagem = mensagem
    
    def __repr__(self):
        return f"<Suporte{self.mensagem}>"