from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # 'admin' ou 'user'

    def __repr__(self):
        return f'<User {self.username}>'

class EPI(db.Model):
    __tablename__ = 'epis'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    localizacao = db.Column(db.String(100), nullable=False)
    validade = db.Column(db.String(20), nullable=True)  # Pode ser melhorado com DateTime

    def __repr__(self):
        return f'<EPI {self.nome}>'
