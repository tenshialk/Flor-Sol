from utils import db

class livros_create(db.Model):
    __tablename__= "livros_create"
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100))
    ano = db.Column(db.String(100))
    curso = db.Column(db.String(100))
    link = db.Column(db.String(100))
    materia = db.Column(db.String(100))

    def __init__(self, titulo, ano, curso, link , materia):
        self.titulo = titulo
        self.ano = ano
        self.curso = curso
        self.link = link
        self.materia = materia

    def __repr__(self):
        return "<livros_create {}>".format(self.id)