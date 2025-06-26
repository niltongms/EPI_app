from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, EPI
from . import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def home():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Usuário ou senha incorretos')

    return render_template('login.html')

@main.route('/dashboard')
@login_required
def dashboard():
    epis = EPI.query.all()
    return render_template('dashboard.html', user=current_user, epis=epis)

@main.route('/cadastrar_epi', methods=['GET', 'POST'])
@login_required
def cadastrar_epi():
    if current_user.role != 'admin':
        flash('Acesso negado: apenas administradores podem cadastrar EPIs.')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        valor = request.form.get('valor')
        localizacao = request.form.get('localizacao')
        validade = request.form.get('validade')

        novo_epi = EPI(nome=nome, valor=valor, localizacao=localizacao, validade=validade)
        db.session.add(novo_epi)
        db.session.commit()
        flash('EPI cadastrado com sucesso!')
        return redirect(url_for('main.dashboard'))

    return render_template('cadastrar_epi.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
