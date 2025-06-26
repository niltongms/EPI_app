from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from .models import User
from . import db

main = Blueprint('main', __name__)

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Acesso negado.')
            return redirect(url_for('main.dashboard'))
        return func(*args, **kwargs)
    return wrapper

@main.route('/usuarios')
@login_required
@admin_required
def usuarios():
    users = User.query.all()
    return render_template('usuarios.html', users=users)

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
            flash('Preencha todos os campos obrigatórios.')
            return redirect(url_for('main.editar_usuario', user_id=user.id))

        # Verifica se já existe outro usuário com esse username
        user_exist = User.query.filter(User.username == username, User.id != user.id).first()
        if user_exist:
            flash('Usuário já existe.')
            return redirect(url_for('main.editar_usuario', user_id=user.id))

        user.username = username
        user.role = role
        if password:
            user.password = generate_password_hash(password)

        db.session.commit()
        flash('Usuário atualizado com sucesso.')
        return redirect(url_for('main.usuarios'))

    return render_template('editar_usuario.html', user=user)

@main.route('/usuarios/deletar/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def deletar_usuario(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash('Você não pode excluir seu próprio usuário.')
        return redirect(url_for('main.usuarios'))

    db.session.delete(user)
    db.session.commit()
    flash('Usuário excluído com sucesso.')
    return redirect(url_for('main.usuarios'))
