import os
import sys

# Adiciona o diretório raiz do projeto ao sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)

# Depuração: Imprimir o sys.path para verificar
print("sys.path:", sys.path)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.models import db, User, Package, Tracking
from app.config import Config

# Define o caminho para os diretórios de templates e static
template_dir = os.path.join(project_root, 'app', 'templates')
static_dir = os.path.join(project_root, 'app', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config.from_object(Config)

db.init_app(app)

# Inicializa o banco de dados com o contexto da aplicação
with app.app_context():
    db.create_all()  # Cria as tabelas se não existirem

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin', _external=True, _scheme='http', _server='localhost', _port=5001))
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin', _external=True, _scheme='http', _server='localhost', _port=5001))
    packages = Package.query.filter_by(user_id=current_user.id).all()
    return render_template('user_dashboard.html', packages=packages)

@app.route('/search')
@login_required
def search():
    query = request.args.get('query', '')
    packages = Package.query.filter(Package.description.contains(query), Package.user_id==current_user.id).all()
    return render_template('user_dashboard.html', packages=packages)

@app.route('/track/<int:package_id>')
@login_required
def track(package_id):
    package = Package.query.get_or_404(package_id)
    if package.user_id != current_user.id:
        flash('Unauthorized')
        return redirect(url_for('dashboard'))
    trackings = package.trackings
    return render_template('user_dashboard.html', packages=[package], trackings=trackings)

if __name__ == '__main__':
    app.run(port=5000, debug=True)