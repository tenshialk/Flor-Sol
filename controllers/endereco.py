from utils import db

class Endereco(db.Model):
    __tablename__ = "endereco"
    id = db.Column(db.Integer, primary_key=True)

    logradouro  = db.Column(db.String(200), nullable=False)
    numero      = db.Column(db.String(50), nullable=False)
    complemento = db.Column(db.String(200))
    bairro      = db.Column(db.String(100), nullable=False)
    cidade      = db.Column(db.String(100), nullable=False)
    estado      = db.Column(db.String(50), nullable=False)
    cep         = db.Column(db.String(20), nullable=False)
    referencia  = db.Column(db.String(200))

    # Relacionamento (se quiser vincular endereço ao usuário)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    def __init__(self, logradouro, numero, complemento, bairro, cidade, estado, cep, referencia, usuario_id=None):
        self.logradouro  = logradouro
        self.numero      = numero
        self.complemento = complemento
        self.bairro      = bairro
        self.cidade      = cidade
        self.estado      = estado
        self.cep         = cep
        self.referencia  = referencia
        self.usuario_id  = usuario_id

    def __repr__(self):
        return f"<Endereco {self.logradouro}, {self.numero}>"


