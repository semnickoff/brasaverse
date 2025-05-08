from datetime import datetime
from sqlalchemy.orm import relationship
from ..extensions import db

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    cover_image_url = db.Column(db.String(255), nullable=True)
    short_description = db.Column(db.Text, nullable=False)
    long_description = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(255), nullable=True)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    comments = db.relationship('Comment', backref='project', lazy=True, cascade="all, delete-orphan")
    likes = db.relationship('Like', backref='project', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Project {self.title}>' 

# models/comment.py
from datetime import datetime
from ..extensions import db

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)

    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    project = db.relationship('Project', backref=db.backref('project_comments', lazy=True))
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')

    def __repr__(self):
        return f'<Comment {self.id} by User {self.user_id} on Project {self.project_id}>'

# models/like.py
from datetime import datetime
from ..extensions import db

class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('likes', lazy=True))
    project = db.relationship('Project', backref=db.backref('project_likes', lazy=True))

    __table_args__ = (db.UniqueConstraint('user_id', 'project_id', name='_user_project_uc'),)

    def __repr__(self):
        return f'<Like by User {self.user_id} on Project {self.project_id}>'

# models/user.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    profile_image_url = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(20), default='user', nullable=False)  # e.g., 'user', 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# models/contact_message.py
from datetime import datetime
from ..extensions import db

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<ContactMessage {self.id} from {self.name}>'

# models/__init__.py
from .user import User
from .project import Project
from .comment import Comment
from .like import Like
from .contact_message import ContactMessage

__all__ = ['User', 'Project', 'Comment', 'Like', 'ContactMessage']

# routes/main_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import db, Project, Comment, ContactMessage, User
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    projects = Project.query.order_by(Project.published_at.desc()).limit(3).all()
    return render_template('home.html', projects=projects)

@main_bp.route('/projects')
def list_projects():
    projects = Project.query.order_by(Project.published_at.desc()).all()
    return render_template('projects.html', projects=projects)

@main_bp.route('/project/<int:project_id>', methods=['GET', 'POST'])
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    comments = Comment.query.filter_by(project_id=project_id).order_by(Comment.created_at.desc()).all()
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        if current_user.is_authenticated:
            new_comment = Comment(
                text=comment_form.text.data,
                user_id=current_user.id,
                project_id=project.id
            )
            db.session.add(new_comment)
            db.session.commit()
            flash('Seu comentário foi adicionado!', 'success')
            return redirect(url_for('main.project_detail', project_id=project.id))
        else:
            flash('Você precisa estar logado para comentar.', 'warning')
            return redirect(url_for('auth.login', next=url_for('main.project_detail', project_id=project.id)))

    return render_template('project_detail.html', project=project, comments=comments, form=comment_form)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Sua mensagem foi enviada com sucesso!', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', form=form)

# routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import db, User
from ..forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Sua conta foi criada! Você já pode fazer login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Registrar', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login sem sucesso. Por favor, verifique o email e a senha.', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cadastrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nome de usuário já está em uso. Por favor, escolha outro.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já está em uso. Por favor, escolha outro.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar-me')
    submit = SubmitField('Login')

class CommentForm(FlaskForm):
    text = TextAreaField('Comentário', validators=[DataRequired()])
    submit = SubmitField('Adicionar Comentário')

# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma_chave_secreta_muito_forte_padrao'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# __init__.py
from flask import Flask
from .extensions import db, login_manager
from .routes.main import main_bp
from .routes.auth import auth_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

# Adicionar o restante do código para os arquivos restantes (models.py, forms.py, etc.)
# models/user.py (já fornecido)
# models/project.py (já fornecido)
# models/comment.py (já fornecido)
# models/like.py (já fornecido)

# forms.py (já fornecido)

# routes/main_routes.py (já fornecido)
# routes/auth_routes.py (já fornecido)

# app.py (já fornecido)

# templates/base.html (já fornecido)
# templates/home.html (já fornecido)
# templates/login.html (já fornecido)
# templates/register.html (já fornecido)
# templates/admin/dashboard.html (já fornecido)
# templates/admin/manage_projects.html (já fornecido)
# templates/admin/manage_users.html (já fornecido)
# templates/admin/view_contacts.html (já fornecido)

# requirements.txt (já fornecido)

# .env.example (já fornecido)

# .gitignore (já fornecido)

# README.md (já fornecido)

# O código restante para os arquivos de templates (base.html, home.html, login.html, register.html, admin/dashboard.html, admin/manage_projects.html, admin/manage_users.html, admin/view_contacts.html) e o arquivo README.md devem ser criados com base nas informações fornecidas anteriormente e nas necessidades do projeto.
# Por exemplo, o base.html deve incluir a estrutura HTML básica, links para CSS e JavaScript, e blocos para conteúdo específico da página.
# Os templates de cada página devem estender o base.html e preencher os blocos de conteúdo.
# O README.md deve conter instruções sobre como configurar e executar o projeto.

# Lembre-se de que este é um esqueleto e você precisará preencher os detalhes e a lógica específica para cada funcionalidade.
# Além disso, considere adicionar mais funcionalidades, como edição de perfil, paginação, busca, etc., conforme necessário.
