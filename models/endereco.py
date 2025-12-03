from utils import db

class Endereco(db.Model):
    __tablename__ = "endereco"

    id = db.Column(db.Integer, primary_key=True)
    logradouro = db.Column(db.String(200))
    numero = db.Column(db.String(20))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    cep = db.Column(db.String(20))
    referencia = db.Column(db.String(200))

    # Se quiser ligar endereço a um usuário:
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    def __init__(self, logradouro, numero, complemento, bairro, cidade, estado, cep, referencia, usuario_id=None):
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        self.referencia = referencia
        self.usuario_id = usuario_id
   
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))  # vínculo com o usuário
    usuario = db.relationship('Usuario', backref='enderecos')