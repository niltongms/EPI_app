from flask import Blueprint, render_template, redirect, url_for, request, flash, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User, EPI
from . import db
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

main = Blueprint('main', __name__)

# Decorator para verificar permissão admin
def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Acesso negado.')
            return redirect(url_for('main.dashboard'))
        return func(*args, **kwargs)
    return wrapper

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Usuário ou senha inválidos.')

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    epis = EPI.query.all() if current_user.is_authenticated else []
    return render_template('dashboard.html', user=current_user, epis=epis)

@main.route('/cadastrar_epi', methods=['GET', 'POST'])
@login_required
@admin_required
def cadastrar_epi():
    if request.method == 'POST':
        nome = request.form['nome']
        valor = request.form['valor']
        localizacao = request.form['localizacao']
        validade = request.form['validade']
        ca = request.form['ca']  # Novo campo

        if not nome or not valor or not localizacao or not ca:
            flash('Preencha todos os campos obrigatórios, incluindo C.A.')
            return redirect(url_for('main.cadastrar_epi'))

        try:
            valor = float(valor)
        except:
            flash('Valor inválido.')
            return redirect(url_for('main.cadastrar_epi'))

        novo = EPI(nome=nome, valor=valor, localizacao=localizacao, validade=validade, ca=ca)
        db.session.add(novo)
        db.session.commit()
        flash('EPI cadastrado com sucesso!')
        return redirect(url_for('main.dashboard'))

    return render_template('cadastrar_epi.html')

@main.route('/editar_epi/<int:epi_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_epi(epi_id):
    epi = EPI.query.get_or_404(epi_id)

    if request.method == 'POST':
        nome = request.form['nome']
        valor = request.form['valor']
        localizacao = request.form['localizacao']
        validade = request.form['validade']
        ca = request.form['ca']  # Novo campo

        if not nome or not valor or not localizacao or not ca:
            flash('Preencha todos os campos obrigatórios, incluindo C.A.')
            return redirect(url_for('main.editar_epi', epi_id=epi.id))

        try:
            valor = float(valor)
        except:
            flash('Valor inválido.')
            return redirect(url_for('main.editar_epi', epi_id=epi.id))

        epi.nome = nome
        epi.valor = valor
        epi.localizacao = localizacao
        epi.validade = validade
        epi.ca = ca  # Atualiza o campo C.A.
        db.session.commit()
        flash('EPI atualizado.')
        return redirect(url_for('main.dashboard'))

    return render_template('editar_epi.html', epi=epi)

@main.route('/deletar_epi/<int:epi_id>', methods=['POST'])
@login_required
@admin_required
def deletar_epi(epi_id):
    epi = EPI.query.get_or_404(epi_id)
    db.session.delete(epi)
    db.session.commit()
    flash('EPI excluído.')
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
@admin_required
def usuarios():
    users = User.query.all()
    return render_template('usuarios.html', users=users)

@main.route('/cadastrar_usuario', methods=['GET', 'POST'])
@login_required
@admin_required
def cadastrar_usuario():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if not username or not password or not role:
            flash('Preencha todos os campos.')
            return redirect(url_for('main.cadastrar_usuario'))

        if User.query.filter_by(username=username).first():
            flash('Usuário já existe.')
            return redirect(url_for('main.cadastrar_usuario'))

        novo = User(username=username,
                   password=generate_password_hash(password),
                   role=role)
        db.session.add(novo)
        db.session.commit()
        flash('Usuário cadastrado.')
        return redirect(url_for('main.usuarios'))

    return render_template('cadastrar_usuario.html')

@main.route('/usuarios/editar/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_usuario(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        password = request.form.get('password')

        if not username or not role:
            flash('Preencha todos os campos.')
            return redirect(url_for('main.editar_usuario', user_id=user.id))

        exists = User.query.filter(User.username==username, User.id!=user.id).first()
        if exists:
            flash('Usuário já existe.')
            return redirect(url_for('main.editar_usuario', user_id=user.id))

        user.username = username
        user.role = role
        if password:
            user.password = generate_password_hash(password)
        db.session.commit()
        flash('Usuário atualizado.')
        return redirect(url_for('main.usuarios'))

    return render_template('editar_usuario.html', user=user)

@main.route('/usuarios/deletar/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def deletar_usuario(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Não pode excluir seu próprio usuário.')
        return redirect(url_for('main.usuarios'))

    db.session.delete(user)
    db.session.commit()
    flash('Usuário excluído.')
    return redirect(url_for('main.usuarios'))

@main.route('/relatorio-epi')
@login_required
@admin_required
def relatorio_epi():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Relatório de EPIs")

    c.setFont("Helvetica", 12)
    y = height - 100
    total_valor = 0

    epis = EPI.query.all()
    for epi in epis:
        linha = f"{epi.nome} - C.A.: {epi.ca} - Valor: R${epi.valor:.2f}"
        c.drawString(50, y, linha)
        y -= 20
        total_valor += epi.valor

        if y < 100:
            c.showPage()
            y = height - 50

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y - 30, f"TOTAL Valor: R$ {total_valor:.2f}")

    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='relatorio_epi.pdf', mimetype='application/pdf')
