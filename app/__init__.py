import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import psycopg2
from urllib.parse import urlparse

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '..', '.env'))  # Carrega o .env na raiz do projeto

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'uma-chavesecreta-muito-segura')

    database_url = os.getenv('DATABASE_URL')
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        
        try:
            # Tenta conectar no PostgreSQL para garantir que está disponível
            parsed = urlparse(database_url)
            conn = psycopg2.connect(
                dbname=parsed.path[1:],  # Remove a barra inicial
                user=parsed.username,
                password=parsed.password,
                host=parsed.hostname,
                port=parsed.port,
                connect_timeout=3
            )
            conn.close()

            app.config['SQLALCHEMY_DATABASE_URI'] = database_url
            print("Conectado ao PostgreSQL com sucesso.")
        except Exception as e:
            print(f"⚠️ Não foi possível conectar ao PostgreSQL: {e}")
            # Fallback para SQLite
            instance_path = os.path.join(basedir, '..', 'instance')
            if not os.path.exists(instance_path):
                os.makedirs(instance_path)
            db_path = os.path.join(instance_path, 'database.db')
            print(f"Usando SQLite em fallback: {db_path}")
            app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    else:
        # Sem DATABASE_URL, usa SQLite
        instance_path = os.path.join(basedir, '..', 'instance')
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
        db_path = os.path.join(instance_path, 'database.db')
        print(f"Banco SQLite em: {db_path}")
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    from .routes import main
    app.register_blueprint(main)

    return app
