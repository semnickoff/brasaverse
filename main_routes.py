# src/routes/main_routes.py
from flask import Blueprint, render_template, send_from_directory, current_app, flash, redirect, url_for # Adicionado flash, redirect, url_for
from flask_login import current_user, login_required # Importar se precisar de dados do usuário
import os
from ..models.project import Project # Importar modelo Project
from ..models.comment import Comment # Importar modelo Comment
from ..forms import CommentForm # Supondo que teremos um CommentForm
from ..extensions import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    # Futuramente, buscar projetos recentes do banco
    # recent_projects = Project.query.order_by(Project.published_at.desc()).limit(3).all()
    recent_projects = [] # Placeholder
    return render_template("home.html", title="Início", recent_projects=recent_projects)

@main_bp.route("/sobre")
def about():
    resume_filename = "curriculo_placeholder.pdf"
    # Usar RESUMES_FOLDER da configuração do app
    resumes_folder_path = current_app.config.get("RESUMES_FOLDER", os.path.join(current_app.static_folder, "resumes"))
    resume_exists = os.path.exists(os.path.join(resumes_folder_path, resume_filename))
    return render_template("about.html", title="Sobre Mim", resume_filename=resume_filename, resume_exists=resume_exists)

@main_bp.route("/download-resume/<filename>")
def download_resume(filename):
    resumes_dir = current_app.config.get("RESUMES_FOLDER", os.path.join(current_app.static_folder, "resumes"))
    # Validação básica do nome do arquivo
    if not filename.endswith(".pdf") or ".." in filename or "/" in filename:
        flash("Nome de arquivo inválido.", "danger")
        return redirect(url_for("main.about"))
    try:
        return send_from_directory(resumes_dir, filename, as_attachment=True)
    except FileNotFoundError:
        flash("Arquivo de currículo não encontrado.", "danger")
        return redirect(url_for("main.about"))

@main_bp.route("/projetos")
def list_projects():
    # Paginação será adicionada futuramente
    # projects = Project.query.order_by(Project.published_at.desc()).all()
    # Placeholder data
    projects_data = [
        {"id": 1, "title": "Projeto Alpha", "short_description": "Descrição curta do Projeto Alpha.", "cover_image_url": "https://via.placeholder.com/300x200.png?text=Projeto+Alpha", "tags": "Python,Flask,JavaScript"},
        {"id": 2, "title": "Sistema Beta", "short_description": "Descrição curta do Sistema Beta.", "cover_image_url": "https://via.placeholder.com/300x200.png?text=Sistema+Beta", "tags": "React,Node.js,MongoDB"},
        {"id": 3, "title": "Ferramenta Gamma", "short_description": "Descrição curta da Ferramenta Gamma.", "cover_image_url": "https://via.placeholder.com/300x200.png?text=Ferramenta+Gamma", "tags": "Data Science,Python,Pandas"}
    ]
    return render_template("projects.html", title="Projetos", projects=projects_data)

@main_bp.route("/projeto/<int:project_id>", methods=["GET", "POST"])
def project_detail(project_id):
    # project = Project.query.get_or_404(project_id)
    # comments = Comment.query.filter_by(project_id=project_id, parent_id=None).order_by(Comment.created_at.desc()).all()
    # comment_form = CommentForm()

    # Placeholder data
    project_data = {"id": project_id, "title": f"Detalhes do Projeto {project_id}", 
                    "long_description": "Esta é uma descrição longa e detalhada do projeto. Inclui informações sobre as tecnologias utilizadas, os desafios enfrentados e as soluções implementadas. O objetivo é fornecer uma visão completa do trabalho realizado.", 
                    "cover_image_url": f"https://via.placeholder.com/600x400.png?text=Projeto+{project_id}", 
                    "tags": "Placeholder,Tags", "author": {"username": "Autor Exemplo"}, "published_at": "2024-01-15" }
    comments_data = [
        {"id": 1, "text": "Ótimo projeto!", "commenter": {"username": "Usuário1", "is_admin": False}, "created_at": "2024-01-16", "replies": [
            {"id": 3, "text": "Obrigado!", "commenter": {"username": "Autor Exemplo", "is_admin": True}, "created_at": "2024-01-17"}
        ]},
        {"id": 2, "text": "Muito interessante.", "commenter": {"username": "Usuário2", "is_admin": False}, "created_at": "2024-01-18", "replies": []}
    ]
    comment_form = None # Placeholder para o formulário de comentário

    # Lógica de submissão de comentário (requer login)
    # if comment_form.validate_on_submit():
    #     if not current_user.is_authenticated:
    #         flash("Você precisa estar logado para comentar.", "warning")
    #         return redirect(url_for("auth.login", next=url_for("main.project_detail", project_id=project_id)))
        
    #     parent_comment_id = request.form.get("parent_id")
    #     new_comment = Comment(
    #         text=comment_form.text.data,
    #         user_id=current_user.id,
    #         project_id=project.id,
    #         parent_id=int(parent_comment_id) if parent_comment_id else None
    #     )
    #     db.session.add(new_comment)
    #     db.session.commit()
    #     flash("Comentário adicionado com sucesso!", "success")
    #     return redirect(url_for("main.project_detail", project_id=project_id))

    return render_template("project_detail.html", title=project_data["title"], project=project_data, comments=comments_data, form=comment_form)

# Adicionar rota para Contato aqui futuramente

