from flask import Blueprint, render_template, request, redirect, url_for
from utils import db
from models.suporte_create import Suporte
from flask_login import login_required, current_user

bp_suporte_create = Blueprint('bp_suporte_create', __name__)

@login_required
@bp_suporte_create.route('/suporte', methods=['GET', 'POST'])
def create_suporte():
    if request.method == 'GET':
        return render_template('suporte_create.html') 

    if request.method == 'POST':
        usuario_id = current_user.id        
        assunto = request.form.get('assunto')  
        mensagem = request.form.get('mensagem')

        # Cria o objeto Suporte
        novo_suporte = Suporte(assunto=assunto, mensagem=mensagem, usuario_id=usuario_id)
        db.session.add(novo_suporte)
        db.session.commit()

        # Redireciona para a página do usuário, por exemplo a biblioteca
        return redirect(url_for('pedidos_suporte'))
