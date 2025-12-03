from utils import db

class roupa_create(db.Model):
    __tablename__ = "roupa_create"
    
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(200))      # link ou caminho da imagem
    preco = db.Column(db.Float)             # preço do item
    titulo = db.Column(db.String(100))
    descricao = db.Column(db.String(300))   # descrição do item

    def __init__(self, imagem, preco, titulo, descricao):
        self.imagem = imagem
        self.preco = preco
        self.titulo = titulo
        self.descricao = descricao

    def __repr__(self):
        return "<roupa_create {}>".format(self.id)
