#!/bin/bash

# Script para instalar o Tailwind CSS e inicializar um projeto Flask

# Instalar o Tailwind CSS e suas dependências
echo "Instalando Tailwind CSS e dependências..."
sudo npm install -g tailwindcss

# Criar um novo projeto Flask (substitua 'meu_projeto_flask' pelo nome do seu projeto)
PROJECT_NAME="meu_projeto_flask"

if [ -d "$PROJECT_NAME" ]; then
  echo "O diretório $PROJECT_NAME já existe. Pulando a criação do projeto."
else
  mkdir "$PROJECT_NAME"
  cd "$PROJECT_NAME"

  # Criar um ambiente virtual e ativá-lo
  python3 -m venv venv
  source venv/bin/activate

  # Instalar Flask e outras dependências necessárias
  pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-WTF python-dotenv

  # Criar a estrutura básica do projeto Flask
  mkdir app
  mkdir app/static
  mkdir app/templates
  mkdir app/static/css

  # Criar arquivos básicos
  touch app/__init__.py
  touch app/routes.py
  touch app/models.py
  touch app/forms.py
  touch app/config.py
  touch app/extensions.py
  touch app/static/css/input.css
  touch app/templates/base.html
  touch app/templates/index.html

  # Adicionar conteúdo básico aos arquivos (opcional, mas útil)
  echo "from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
" > app/__init__.py

  echo "from flask import render_template
from app import app

@app.route('/')
def index():
    return render_template('index.html', title='Home')
" > app/routes.py

  echo "import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
" > app/config.py

  echo "<!doctype html>
<html>
<head>
    <title>{{ title }} - Meu App</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/output.css') }}">
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>" > app/templates/base.html

  echo "{% extends 'base.html' %}

{% block content %}
    <h1 class=\"text-2xl font-bold text-blue-500\">Olá, Tailwind CSS!</h1>
{% endblock %}
" > app/templates/index.html

  echo "@tailwind base;
@tailwind components;
@tailwind utilities;" > app/static/css/input.css

  # Inicializar o Tailwind CSS
  npx tailwindcss init -p

  # Configurar o tailwind.config.js para incluir os templates HTML
  echo "module.exports = {
  content: [\"./app/templates/**/*.html\"],
  theme: {
    extend: {},
  },
  plugins: [],
}" > tailwind.config.js

  echo "Flask app setup complete. Remember to run 'flask db init', 'flask db migrate', and 'flask db upgrade' for database setup."
fi

