from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Inicialização do SQLAlchemy - será movida para o app factory em main.py
# Temporariamente aqui para evitar erros de importação circular ou de contexto de app
# Em um projeto real, db = SQLAlchemy() seria inicializado no app factory
# e importado aqui como: from .. import db

# Placeholder para o objeto db. Será substituído pela instância real do SQLAlchemy.
# Este é um artifício comum ao definir modelos em arquivos separados antes que o app Flask seja totalmente configurado.
# A maneira correta é: from .. import db (após db ser inicializado e o app factory estar pronto)

# Para fins de desenvolvimento isolado dos modelos, podemos instanciar um SQLAlchemy temporário
# No entanto, para integração com o app Flask, isso precisa ser gerenciado centralmente.
# Por agora, vamos assumir que 'db' será um objeto SQLAlchemy injetado ou importado.

# Correção: Definir db globalmente ou passá-lo. Para este contexto, vamos definir um db temporário
# que será substituído pela instância real do SQLAlchemy do app principal.
# Esta abordagem é apenas para permitir a definição da classe do modelo.
# A inicialização real e a vinculação ao aplicativo Flask ocorrerão em `main.py`.

# from .. import db # Esta seria a importação ideal em um projeto Flask estruturado

# Como estamos construindo passo a passo e o 'db' de main.py ainda não está configurado
# para ser importado aqui sem causar problemas de importação circular ou de contexto de app,
# vamos definir os modelos e depois integrá-los.
# O objeto 'db' real virá de 'main.py' ou de um arquivo 'extensions.py'.

# Vamos criar um arquivo extensions.py para centralizar as extensões.

# models/user.py

from ..extensions import db # Importando db de extensions.py

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False) # Aumentado para 256
    profile_image_url = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    projects = db.relationship('Project', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commenter', lazy=True)
    likes = db.relationship('Like', backref='liker', lazy=True)
    notifications = db.relationship('Notification', backref='recipient', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Flask-Login integration
    def get_id(self):
        return str(self.id)

    @property
    def is_admin(self):
        return self.role == 'admin'

