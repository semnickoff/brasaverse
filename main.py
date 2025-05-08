# src/main.py
import sys
import os

from flask import Flask, render_template, flash, redirect, url_for # Adicionado flash, redirect, url_for
from .extensions import db, migrate, login_manager, csrf
from .models.user import User
from .models.project import Project
from .models.comment import Comment
from .models.like import Like
from .models.contact_message import ContactMessage
from .models.notification import Notification
from .routes.auth import auth_bp
from .routes.main_routes import main_bp # Importado o main_bp
from .routes.admin.admin_routes import admin_bp # Importado o admin_bp
from .routes.notifications import notifications_bp # Importado o notifications_bp

# Variáveis de ambiente para configuração do banco de dados
DB_USERNAME = os.getenv("DB_USERNAME", "user_portfolio")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password_portfolio")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "portfolio_db")

# Diretório para upload
UPLOAD_FOLDER_BASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static")
PROFILE_PICS_FOLDER = os.path.join(UPLOAD_FOLDER_BASE, "profile_pics")
RESUMES_FOLDER = os.path.join(UPLOAD_FOLDER_BASE, "resumes") # Adicionado para currículos
PROJECT_IMAGES_FOLDER = os.path.join(UPLOAD_FOLDER_BASE, "project_images") # Adicionado para imagens de projeto

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "uma_chave_secreta_muito_forte_padrao")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Configuração das pastas de upload
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER_BASE # Pasta base para uploads
    app.config["PROFILE_PICS_FOLDER"] = PROFILE_PICS_FOLDER
    app.config["RESUMES_FOLDER"] = RESUMES_FOLDER
    app.config["PROJECT_IMAGES_FOLDER"] = PROJECT_IMAGES_FOLDER

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.login_message = "Por favor, faça login para acessar esta página."

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp) # Registrado o admin_bp
    app.register_blueprint(notifications_bp) # Registrado o notifications_bp

    with app.app_context():
        if not os.path.exists(app.config["PROFILE_PICS_FOLDER"]):
            os.makedirs(app.config["PROFILE_PICS_FOLDER"])
        if not os.path.exists(app.config["RESUMES_FOLDER"]):
            os.makedirs(app.config["RESUMES_FOLDER"])
        if not os.path.exists(app.config["PROJECT_IMAGES_FOLDER"]):
            os.makedirs(app.config["PROJECT_IMAGES_FOLDER"])

    # Adicionar um filtro Jinja para formatar datetime
    @app.template_filter("datetimeformat")
    def datetimeformat(value, format="%d/%m/%Y %H:%M"):
        if value is None:
            return ""
        return value.strftime(format)

    # Adicionar cabeçalhos de segurança HTTP
    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        # response.headers["Content-Security-Policy"] = "default-src \'self\'; img-src *; style-src \'self\' https://cdn.tailwindcss.com; script-src \'self\' \'unsafe-inline\';"
        # CSP é complexo e precisa ser ajustado cuidadosamente. O exemplo acima é básico.
        # Para produção, considere HSTS: response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

    return app

