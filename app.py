from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///flor_sol.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    species = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_watered = db.Column(db.DateTime)
    watering_frequency = db.Column(db.Integer, default=7)  # days
    
    user = db.relationship('User', backref=db.backref('plants', lazy=True))

class WateringRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    watered_at = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float)  # in ml
    
    plant = db.relationship('Plant', backref=db.backref('watering_records', lazy=True))

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        return jsonify({'success': True}), 201
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            return jsonify({'success': True}), 200
        
        return jsonify({'error': 'Invalid username or password'}), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    plants = Plant.query.filter_by(user_id=user.id).all()
    
    plant_data = []
    for plant in plants:
        days_since_watered = None
        if plant.last_watered:
            days_since_watered = (datetime.utcnow() - plant.last_watered).days
        
        plant_data.append({
            'id': plant.id,
            'name': plant.name,
            'species': plant.species,
            'last_watered': plant.last_watered.strftime('%Y-%m-%d %H:%M') if plant.last_watered else 'Never',
            'days_since_watered': days_since_watered,
            'watering_frequency': plant.watering_frequency,
            'needs_water': days_since_watered is not None and days_since_watered >= plant.watering_frequency
        })
    
    return render_template('dashboard.html', user=user, plants=plant_data)

@app.route('/api/plants', methods=['GET', 'POST'])
@login_required
def manage_plants():
    user_id = session['user_id']
    
    if request.method == 'POST':
        data = request.get_json()
        plant = Plant(
            name=data.get('name'),
            species=data.get('species'),
            user_id=user_id,
            watering_frequency=data.get('watering_frequency', 7)
        )
        db.session.add(plant)
        db.session.commit()
        
        return jsonify({'id': plant.id, 'name': plant.name}), 201
    
    plants = Plant.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'species': p.species,
        'watering_frequency': p.watering_frequency
    } for p in plants])

@app.route('/api/plants/<int:plant_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def plant_detail(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    
    if plant.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'GET':
        return jsonify({
            'id': plant.id,
            'name': plant.name,
            'species': plant.species,
            'watering_frequency': plant.watering_frequency,
            'last_watered': plant.last_watered.isoformat() if plant.last_watered else None
        })
    
    if request.method == 'PUT':
        data = request.get_json()
        plant.name = data.get('name', plant.name)
        plant.species = data.get('species', plant.species)
        plant.watering_frequency = data.get('watering_frequency', plant.watering_frequency)
        db.session.commit()
        return jsonify({'success': True}), 200
    
    if request.method == 'DELETE':
        db.session.delete(plant)
        db.session.commit()
        return jsonify({'success': True}), 200

@app.route('/api/plants/<int:plant_id>/water', methods=['POST'])
@login_required
def water_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    
    if plant.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    record = WateringRecord(
        plant_id=plant_id,
        amount=data.get('amount', 250)
    )
    plant.last_watered = datetime.utcnow()
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'last_watered': plant.last_watered.isoformat()
    }), 200

@app.route('/api/plants/<int:plant_id>/history', methods=['GET'])
@login_required
def watering_history(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    
    if plant.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    records = WateringRecord.query.filter_by(plant_id=plant_id).order_by(WateringRecord.watered_at.desc()).limit(30).all()
    
    return jsonify([{
        'id': r.id,
        'watered_at': r.watered_at.isoformat(),
        'amount': r.amount
    } for r in records])

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/suporte')
def suporte():
    return render_template('suporte.html')

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')
    
    if not all([email, subject, message]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # TODO: Implement email sending functionality
    # For now, just log the message
    print(f"Contact form submission: {email} - {subject}")
    
    return jsonify({'success': True, 'message': 'Your message has been received'}), 200

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
