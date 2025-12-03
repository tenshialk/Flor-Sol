from flask import Flask, Blueprint, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from utils import db,lm
from controllers.usuario import bp_usuarios
from models.usuario import Usuario


# Inicializando o Flask
app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'PIZZA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o banco de dados
db.init_app(app)
lm.init_app(app)
migrate = Migrate(app, db)

# Registrando Blueprints
app.register_blueprint(bp_usuarios, url_prefix='/user')

# Rotas principais
@app.route('/')
def capa():
    return render_template('capa.html')

@app.route('/Volta')
def Volta():
    return render_template('volta.html')

@app.route('/biblioteca')
def biblioteca():
    return render_template('biblioteca.html')


@app.route('/inicio')
def inicio():
    return render_template('capa.html')


@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/seus_dados')
def seus_dados():
    usuario = Usuario.query.first()
    return render_template('seus_dados.html', dados=usuario)

@app.route('/altera_seus_dados')
def altera_seus_dados():
    usuario = Usuario.query.first()
    return render_template('altera_seus_dados.html', dados=usuario)

@app.route('/atualizar_dados', methods=['POST'])
def atualizar_dados():
    usuario = Usuario.query.first()   # pegue o usuário certo aqui
    usuario.nome = request.form['nome']
    usuario.email = request.form['email']
    usuario.senha = request.form['senha']

    db.session.commit()
    return redirect('/seus_dados')


@app.errorhandler(401)
def acesso_negado(e):
    return render_template('acesso_negado.html'), 404

if __name__ == '__main__':
    app.run(debug=True)