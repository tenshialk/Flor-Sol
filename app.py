from flask import Flask, Blueprint, render_template, request, redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from utils import db,lm
from controllers.usuario import bp_usuarios
from controllers.roupa_create import bp_roupa_create
from models.usuario import Usuario
from models.roupa_create import roupa_create
from models.endereco import Endereco


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

@app.route('/roupa_create')
def roupa_create():
    return render_template('roupa_create.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/gestao_endereco')
def gestao_endereco():
    endereco = Endereco.query.first()  # pegar o primeiro endereço
    return render_template('gestao_endereco.html', endereco=endereco)

@app.route('/salvar_endereco', methods=['POST'])
def salvar_endereco():
    # Pega dados do formulário
    logradouro  = request.form['logradouro']
    numero      = request.form['numero']
    complemento = request.form['complemento']
    bairro      = request.form['bairro']
    cidade      = request.form['cidade']
    estado      = request.form['estado']
    cep         = request.form['cep']
    referencia  = request.form['referencia']

    # Cria o endereço
    endereco = Endereco(
        logradouro=logradouro,
        numero=numero,
        complemento=complemento,
        bairro=bairro,
        cidade=cidade,
        estado=estado,
        cep=cep,
        referencia=referencia
    )

    # Salva no banco
    db.session.add(endereco)
    db.session.commit()

    # Redireciona para a página que exibe o endereço cadastrado
    return render_template('salvar_endereco.html', endereco=endereco)


@app.route('/atualizar_endereco', methods=['POST'])
def atualizar_endereco():
    endereco = Endereco.query.get(request.form['id'])
    endereco.logradouro  = request.form['logradouro']
    endereco.numero      = request.form['numero']
    endereco.complemento = request.form['complemento']
    endereco.bairro      = request.form['bairro']
    endereco.cidade      = request.form['cidade']
    endereco.estado      = request.form['estado']
    endereco.cep         = request.form['cep']
    endereco.referencia  = request.form['referencia']
    db.session.commit()
    # Redireciona para a página de gestão de endereços
    return redirect(url_for('gestao_endereco'))


@app.route('/excluir_endereco',methods=['POST'])
def excluir_endereco():
    usuario = Usuario.query.first()
    return render_template('excluir_endereco.html', dados=usuario, enderecos=usuario.enderecos)

@app.route('/seus_dados')
def seus_dados():
    usuario = Usuario.query.first()
    endereco = Endereco.query.first()
    return render_template('seus_dados.html', dados=usuario, endereco=endereco)


@app.route('/atualizar_dados', methods=['POST'])
def atualizar_dados():
    usuario = Usuario.query.first()  # Pega o primeiro usuário (ou ajuste para pegar pelo id)
    usuario.nome  = request.form['nome']
    usuario.email = request.form['email']
    usuario.senha = request.form['senha']
    db.session.commit()  # Salva as alterações no banco de dados
    # Redireciona para a página que mostra os dados atualizados
    return redirect(url_for('seus_dados'))


@app.route('/altera_seus_dados',)
def altera_seus_dados():
    usuario = Usuario.query.first()
    return render_template('altera_seus_dados.html', dados=usuario)

@app.errorhandler(401)
def acesso_negado(e):
    return render_template('acesso_negado.html'), 404

if __name__ == '__main__':
    app.run(debug=True)