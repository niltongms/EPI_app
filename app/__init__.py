from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'uma-chavesecreta-muito-segura'  # Altere para algo bem secreto
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Certifique-se que esta função esteja **dentro** da create_app, após login_manager.init_app()
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    from .routes import main
    app.register_blueprint(main)

    return app
