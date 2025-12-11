from utils import db
from datetime import datetime

class Suporte(db.Model):
    __tablename__ = "suporte_admin"
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=True)  
    assunto = db.Column(db.String(200), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    data_abertura = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="Aberto") 

    def __init__(self, assunto, mensagem, usuario_id=None):
        self.assunto = assunto
        self.mensagem = mensagem
        self.usuario_id = usuario_id
        self.status = "Aberto"
        self.data_abertura = datetime.utcnow()

    def __repr__(self):
        return f"<pedidos_suporte {self.id}>"

