import os
import sys

# Adiciona o diretório raiz do projeto ao sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from flask import Flask
from app.models import db, User, Package, Tracking
from app.config import Config
from werkzeug.security import generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def init_db():
    with app.app_context():
        db.drop_all()  # Remove todas as tabelas (útil para reiniciar o banco)
        db.create_all()

        # Criação de usuários (verifica se já existem para evitar duplicatas)
        if not User.query.filter_by(username='user1').first():
            user = User(username='user1', password=generate_password_hash('password'), is_admin=False)
            db.session.add(user)
        if not User.query.filter_by(username='admin1').first():
            admin = User(username='admin1', password=generate_password_hash('adminpass'), is_admin=True)
            db.session.add(admin)

        # Criação de pacote (verifica se já existe)
        if not Package.query.filter_by(description='Sample Package').first():
            package = Package(user_id=1, description='Sample Package')
            db.session.add(package)

        # Adição de rastreamento (usa 'location' em vez de 'city')
        if not Tracking.query.filter_by(package_id=1).first():
            tracking = Tracking(status='Enviado', location='New York', package_id=1)  # timestamp será preenchido pelo valor padrão
            db.session.add(tracking)

        db.session.commit()  # Commit único após todas as adições

if __name__ == '__main__':
    init_db()
    print("Base de dados inicializada com sucesso!")