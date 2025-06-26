import os
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')

if not os.path.exists(instance_path):
    os.makedirs(instance_path)
    print("Pasta 'instance' criada.")
else:
    print("Pasta 'instance' já existe.")

with app.app_context():
    db.create_all()

    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username='admin',
            password=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Usuário admin criado com sucesso (admin/admin123)")
    else:
        print("Usuário admin já existe.")
