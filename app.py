from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flor_sol.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    roupas = db.relationship('Roupa', backref='user', lazy=True, cascade='all, delete-orphan')

class Roupa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text)
    cor = db.Column(db.String(50))
    tamanho = db.Column(db.String(10))
    categoria = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            return 'Username already exists', 400
        
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password', 401
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    roupas = Roupa.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', roupas=roupas)

@app.route('/roupa/create', methods=['GET', 'POST'])
@login_required
def roupa_create():
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        cor = request.form.get('cor')
        tamanho = request.form.get('tamanho')
        categoria = request.form.get('categoria')
        
        roupa = Roupa(
            nome=nome,
            descricao=descricao,
            cor=cor,
            tamanho=tamanho,
            categoria=categoria,
            user_id=current_user.id
        )
        
        db.session.add(roupa)
        db.session.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('roupa_form.html')

@app.route('/roupa/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def roupa_edit(id):
    roupa = Roupa.query.get_or_404(id)
    
    if roupa.user_id != current_user.id:
        return 'Unauthorized', 403
    
    if request.method == 'POST':
        roupa.nome = request.form.get('nome')
        roupa.descricao = request.form.get('descricao')
        roupa.cor = request.form.get('cor')
        roupa.tamanho = request.form.get('tamanho')
        roupa.categoria = request.form.get('categoria')
        
        db.session.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('roupa_form.html', roupa=roupa)

@app.route('/roupa/<int:id>/delete', methods=['POST'])
@login_required
def roupa_delete(id):
    roupa = Roupa.query.get_or_404(id)
    
    if roupa.user_id != current_user.id:
        return 'Unauthorized', 403
    
    db.session.delete(roupa)
    db.session.commit()
    
    return redirect(url_for('dashboard'))

@app.route('/api/roupas')
@login_required
def api_roupas():
    roupas = Roupa.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': roupa.id,
        'nome': roupa.nome,
        'descricao': roupa.descricao,
        'cor': roupa.cor,
        'tamanho': roupa.tamanho,
        'categoria': roupa.categoria
    } for roupa in roupas])

if __name__ == '__main__':
    app.run(debug=True)
