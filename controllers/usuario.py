from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils import db,lm
from models.usuario import Usuario
from flask_login import login_user, logout_user
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

bp_usuarios = Blueprint("usuarios", __name__, template_folder='templates')

@bp_usuarios.route('/create', methods=['GET', 'POST'])
def create():
    if request.method=='GET':
        return render_template('Cadastro.html')
    if request.method=='POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        senha_criptografada = generate_password_hash(senha)
        admin=request.form.get('admin')
        print(len(nome))
        if len(nome) < 3:
            flash('nome precisa de mais de 3 letras para o nome')
            return redirect(url_for('usuarios.create'))
        if len(senha) < 3 :
            flash('senha precisa de mais de 3 caractere para a senha')
            return redirect(url_for('usuarios.create'))
        if Usuario.query.filter_by(email=email).first():
            flash('Email já cadastrado!')
            return redirect(url_for('usuarios.create'))
        
          
        usuario = Usuario(nome, email, senha_criptografada, admin)
        db.session.add(usuario)
        db.session.commit()

        login_user(usuario)

        return redirect(url_for('biblioteca'))

@bp_usuarios.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if id==0:
        flash('É preciso definir um usuário para ser excluído')
        return redirect(url_for('.recovery'))

    if request.method == 'GET':
        usuario = Usuario.query.get(id)
        return render_template('usuarios_delete.html', usuario = usuario)

    if request.method == 'POST':
        usuario = Usuario.query.get(id)
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuário excluído com sucesso')
        return redirect(url_for('.recovery'))

@lm.user_loader
def load_user(id):
    usuario = Usuario.query.filter_by(id=id).first()
    #usuario = Usuario.query.get(id)
    return usuario

@bp_usuarios.route('/autenticar', methods=['GET','POST'])
def autenticar():
    if request.method == 'GET':
            return render_template('usuario_create.html')
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = Usuario.query.filter_by(email = email).first()
        if usuario is None:
            return redirect(url_for('usuarios.autenticar'))
        if (senha is not None and check_password_hash(usuario.senha, senha)):
            login_user(usuario)
            return redirect(url_for('biblioteca'))
        else:
            flash('Dados incorretos')
            return redirect(url_for('usuarios.autenticar'))
      
      
@bp_usuarios.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method=='GET':
        return render_template('usuarios_create.html')
    if request.method=='POST':
        usuario = Usuario.query.get(id)
        return render_template('usuarios_update.html', usuario=usuario)

    if (request.method=='POST'):
        usuario = Usuario.query.get(id)
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.senha = request.form.get('senha')
            
    if (request.form.get('senha') and request.form.get('senha') == request.form.get('csenha')):
        usuario.senha = request.form.get('senha')
    else:
        flash('Senhas não conferem')
        return redirect(url_for('.update', id=id)) 

        db.session.add(usuario) 
        db.session.commit()
        flash('Dados atualizados com sucesso!')
        return redirect(url_for('.recovery', id=id))
    
@bp_usuarios.route('/logout')
def logout():
    logout_user()
    return render_template('capa.html')