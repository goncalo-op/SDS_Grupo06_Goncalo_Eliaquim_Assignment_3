import os
import sys

# Adiciona o diretório raiz do projeto ao sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)

# Depuração: Imprimir o sys.path para verificar
print("sys.path:", sys.path)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import check_password_hash
from app.models import db, User, Package, Tracking
from app.config import Config
from datetime import datetime

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

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Admins only')
        return redirect('http://localhost:5000/dashboard')
    packages = Package.query.all()
    return render_template('admin_dashboard.html', packages=packages)

@app.route('/add_package', methods=['POST'])
@login_required
def add_package():
    if not current_user.is_admin:
        flash('Admins only')
        return redirect(url_for('admin'))
    description = request.form['description']
    user_id = request.form['user_id']
    package = Package(description=description, user_id=user_id)
    db.session.add(package)
    db.session.commit()
    flash('Package added')
    return redirect(url_for('admin'))

@app.route('/remove_package/<int:package_id>')
@login_required
def remove_package(package_id):
    if not current_user.is_admin:
        flash('Admins only')
        return redirect(url_for('admin'))
    package = Package.query.get_or_404(package_id)
    db.session.delete(package)
    db.session.commit()
    flash('Package removed')
    return redirect(url_for('admin'))

@app.route('/update_tracking/<int:package_id>', methods=['POST'])
@login_required
def update_tracking(package_id):
    if not current_user.is_admin:
        flash('Admins only')
        return redirect(url_for('admin'))
    city = request.form['city']
    tracking = Tracking(package_id=package_id, location=city, timestamp=datetime.utcnow())
    db.session.add(tracking)
    db.session.commit()
    flash('Tracking updated')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(port=5001, debug=True)