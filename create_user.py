from app.models import db, User
from werkzeug.security import generate_password_hash
from app.config import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

    #Credenciais
    username = "admin"
    password = "admin123"
    is_admin = True

    if not User.query.filter_by(username=username).first():
        hashed_pw = generate_password_hash(password)
        user = User(username=username, password=hashed_pw, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()
        print(f"Utilizador '{username}' criado com sucesso.")
    else:
        print(f"O utilizador '{username}' já existe.")
