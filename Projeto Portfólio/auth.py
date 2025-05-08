# src/routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os

from ..forms import LoginForm, RegistrationForm
from ..models.user import User
from ..extensions import db, login_manager

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Configure o user_loader para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home")) # Supondo que você terá uma rota principal "home"
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        existing_user_email = User.query.filter_by(email=email).first()
        if existing_user_email:
            flash("Este email já está cadastrado. Por favor, faça login ou use outro email.", "danger")
            return redirect(url_for("auth.register"))

        existing_user_username = User.query.filter_by(username=username).first()
        if existing_user_username:
            flash("Este nome de usuário já está em uso. Por favor, escolha outro.", "danger")
            return redirect(url_for("auth.register"))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        # Lógica de upload da imagem de perfil
        if form.profile_image.data:
            # É preciso configurar UPLOAD_FOLDER no app Flask
            # from flask import current_app
            # upload_folder = current_app.config.get('UPLOAD_FOLDER', 'src/static/profile_pics')
            # Este path deve ser configurado corretamente no app factory
            upload_folder = os.path.join(os.getcwd(), "src", "static", "profile_pics") # Caminho absoluto
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            
            profile_pic = form.profile_image.data
            filename = secure_filename(profile_pic.filename)
            # Para evitar conflitos de nome, pode-se adicionar o ID do usuário ou um UUID ao nome do arquivo
            # Isso seria feito após salvar o usuário para obter o ID, ou gerar um nome único antes.
            # Por simplicidade, vamos usar o nome original, mas isso não é ideal para produção.
            # Uma melhor abordagem seria: filename = f"{new_user.id}_{secure_filename(profile_pic.filename)}" após o commit inicial do usuário.
            # Ou, gerar um UUID para o nome do arquivo.
            # Para agora, vamos salvar o usuário primeiro, depois a imagem.
            
            # Salva o usuário para obter o ID
            try:
                db.session.add(new_user)
                db.session.commit() # Commit para obter o ID do usuário
                
                # Agora salva a imagem com o ID do usuário no nome
                if profile_pic:
                    _, f_ext = os.path.splitext(filename)
                    # Garante que o nome do arquivo seja único e relacionado ao usuário
                    final_filename = f"{new_user.id}{f_ext}"
                    file_path = os.path.join(upload_folder, final_filename)
                    profile_pic.save(file_path)
                    new_user.profile_image_url = url_for("static", filename=f"profile_pics/{final_filename}", _external=False)
                    db.session.commit() # Commit da URL da imagem

                flash(f"Conta criada para {form.username.data}! Você já pode fazer login.", "success")
                return redirect(url_for("auth.login"))
            except Exception as e:
                db.session.rollback()
                flash(f"Erro ao criar conta: {e}", "danger")
                # Logar o erro e.str() para debug
        else:
            try:
                db.session.add(new_user)
                db.session.commit()
                flash(f"Conta criada para {form.username.data}! Você já pode fazer login.", "success")
                return redirect(url_for("auth.login"))
            except Exception as e:
                db.session.rollback()
                flash(f"Erro ao criar conta: {e}", "danger")

    return render_template("register.html", title="Cadastro", form=form) # Criar template register.html

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login realizado com sucesso!", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login falhou. Verifique seu email e senha.", "danger")
    return render_template("login.html", title="Login", form=form) # Criar template login.html

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você foi desconectado.", "info")
    return redirect(url_for("auth.login"))

# É necessário criar os templates register.html e login.html
# E também uma rota principal 'main.home' para redirecionamento

