from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Carregar variáveis de ambiente
load_dotenv()

def create_app():


    # Obter o caminho absoluto para a pasta templates
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    app = Flask(__name__, template_folder=template_dir)

    # Configurar a chave secreta
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Configurar a conexão com o banco de dados
    # Valor padrão: instance/finance.db na raiz do projeto
    basedir = os.path.abspath(os.path.dirname(__file__))
    instance_dir = os.path.abspath(os.path.join(basedir, '..', 'instance'))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_dir, 'finance.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar o banco de dados
    db.init_app(app)

    # criar todas as tabelas
    with app.app_context():
        db.create_all()

    # registrar blueprints
    from app.main import main_bp
    from app.auth import auth_bp
    from app.finance import finance_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(finance_bp)
    return app




