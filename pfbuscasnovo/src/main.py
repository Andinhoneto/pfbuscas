import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
import secrets
from datetime import datetime

# Inicialização do app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do banco de dados
db = SQLAlchemy(app)

# Inicialização do gerenciador de login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

# Modelo de usuário
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    theme = db.Column(db.String(20), default='light')
    primary_color = db.Column(db.String(20), default='#007bff')
    secondary_color = db.Column(db.String(20), default='#6c757d')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Modelo para histórico de buscas
class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"SearchHistory('{self.cpf}', '{self.timestamp}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rotas para autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login falhou. Por favor, verifique seu nome de usuário e senha.', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return render_template('register.html')
        
        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()
        
        if user_exists:
            flash('Nome de usuário já existe. Por favor, escolha outro.', 'danger')
        elif email_exists:
            flash('Email já está em uso. Por favor, use outro email.', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Sua conta foi criada! Agora você pode fazer login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Rota para a página inicial
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Rota para o painel principal
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Rota para buscar CPF
@app.route('/search', methods=['POST'])
@login_required
def search():
    cpf = request.form.get('cpf')
    
    # Remover caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    if not cpf or len(cpf) != 11:
        return jsonify({'error': 'CPF inválido. Por favor, insira um CPF válido com 11 dígitos.'}), 400
    
    try:
        # Registrar a busca no histórico
        search_history = SearchHistory(user_id=current_user.id, cpf=cpf)
        db.session.add(search_history)
        db.session.commit()
        
        # Fazer a requisição para a API
        response = requests.get(f"http://api2.minerdapifoda.xyz:8080/api/cpf?cpf={cpf}")
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({'error': 'Erro ao buscar dados. Por favor, tente novamente mais tarde.'}), response.status_code
    
    except Exception as e:
        return jsonify({'error': f'Erro ao processar a requisição: {str(e)}'}), 500

# Rota para configurações de tema
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        theme = request.form.get('theme')
        primary_color = request.form.get('primary_color')
        secondary_color = request.form.get('secondary_color')
        
        current_user.theme = theme
        current_user.primary_color = primary_color
        current_user.secondary_color = secondary_color
        
        db.session.commit()
        flash('Configurações atualizadas com sucesso!', 'success')
        
    return render_template('settings.html')

# Rota para histórico de buscas
@app.route('/history')
@login_required
def history():
    searches = SearchHistory.query.filter_by(user_id=current_user.id).order_by(SearchHistory.timestamp.desc()).all()
    return render_template('history.html', searches=searches)

# Criar todas as tabelas do banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
