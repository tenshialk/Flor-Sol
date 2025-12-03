from flask import Blueprint, render_template, request, redirect, url_for
from utils import db
from models.roupa_create import roupa_create
from flask_login import login_required

bp_roupa_create = Blueprint("roupa_create", __name__, template_folder='templates')


# ------------------ CRIAR ------------------
@login_required
@bp_roupa_create.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('roupa_create.html')

    if request.method == 'POST':
        imagem = request.form.get('imagem')
        preco = request.form.get('preco')
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')

        nova_roupa = roupa_create(imagem, preco, titulo, descricao)
        db.session.add(nova_roupa)
        db.session.commit()

        return redirect(url_for('biblioteca'))

# ------------------ ATUALIZAR ------------------
@login_required
@bp_roupa_create.route('/<id>/update', methods=['GET', 'POST'])
def update(id):
    roupa = roupa_create.query.filter_by(id=id).first()

    if request.method == 'GET':
        return render_template('roupa_update.html', roupa=roupa)

    if request.method == 'POST':
        roupa.imagem = request.form.get('imagem')
        roupa.preco = request.form.get('preco')
        roupa.titulo = request.form.get('titulo')
        roupa.descricao = request.form.get('descricao')

        db.session.commit()
        return redirect(url_for('biblioteca'))


# ------------------ DELETAR ------------------
@bp_roupa_create.route('/<id>/delete')
def delete(id):
    roupa = roupa_create.query.filter_by(id=id).first()
    db.session.delete(roupa)
    db.session.commit()
    return redirect(url_for('biblioteca'))


# ------------------ RECUPERAR E LISTAR ------------------
@bp_roupa_create.route('/recovery')
def recovery():
    roupas = roupa_create.query.all()
    print(roupas)
    return render_template("biblioteca.html", roupas=roupas)
