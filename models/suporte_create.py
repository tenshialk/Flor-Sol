from utils import db

class Suporte(db.Model):
    __tablename__ = "suporte"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Suporte {self.id}>"
