# src/routes/admin/admin_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ...extensions import db
from ...models.user import User
from ...models.project import Project
from ...models.comment import Comment
from ...models.contact_message import ContactMessage
from ...forms import ProjectForm # Supondo que teremos um ProjectForm para admin
from functools import wraps

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Decorator para restringir acesso a administradores
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Acesso negado. Você precisa ser um administrador para ver esta página.", "danger")
            return redirect(url_for("main.home"))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    # Coletar estatísticas básicas
    user_count = User.query.count()
    project_count = Project.query.count()
    comment_count = Comment.query.count()
    contact_message_count = ContactMessage.query.count()
    # Adicionar mais estatísticas conforme necessário
    stats = {
        "user_count": user_count,
        "project_count": project_count,
        "comment_count": comment_count,
        "contact_message_count": contact_message_count
    }
    return render_template("admin/dashboard.html", title="Painel Administrativo", stats=stats)

# Gerenciamento de Projetos
@admin_bp.route("/projects")
@login_required
@admin_required
def manage_projects():
    projects = Project.query.order_by(Project.published_at.desc()).all()
    return render_template("admin/manage_projects.html", title="Gerenciar Projetos", projects=projects)

@admin_bp.route("/projects/new", methods=["GET", "POST"])
@login_required
@admin_required
def create_project():
    form = ProjectForm() # Usar um formulário específico para criação/edição de projetos
    if form.validate_on_submit():
        # Lógica para criar novo projeto
        # new_project = Project(title=form.title.data, ... , user_id=current_user.id)
        # db.session.add(new_project)
        # db.session.commit()
        flash("Projeto criado com sucesso! (Placeholder)", "success")
        return redirect(url_for("admin.manage_projects"))
    return render_template("admin/edit_project.html", title="Novo Projeto", form=form, project=None)

@admin_bp.route("/projects/edit/<int:project_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project) # Preencher formulário com dados do projeto
    if form.validate_on_submit():
        # Lógica para atualizar o projeto
        # form.populate_obj(project)
        # db.session.commit()
        flash("Projeto atualizado com sucesso! (Placeholder)", "success")
        return redirect(url_for("admin.manage_projects"))
    return render_template("admin/edit_project.html", title="Editar Projeto", form=form, project=project)

@admin_bp.route("/projects/delete/<int:project_id>", methods=["POST"])
@login_required
@admin_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    # db.session.delete(project)
    # db.session.commit()
    flash("Projeto excluído com sucesso! (Placeholder)", "success")
    return redirect(url_for("admin.manage_projects"))

# Gerenciamento de Usuários
@admin_bp.route("/users")
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template("admin/manage_users.html", title="Gerenciar Usuários", users=users)

# Visualizar Mensagens de Contato
@admin_bp.route("/contacts")
@login_required
@admin_required
def view_contact_messages():
    messages = ContactMessage.query.order_by(ContactMessage.sent_at.desc()).all()
    return render_template("admin/view_contacts.html", title="Mensagens de Contato", messages=messages)

# Gerenciar Comentários
@admin_bp.route("/comments")
@login_required
@admin_required
def manage_comments():
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template("admin/manage_comments.html", title="Gerenciar Comentários", comments=comments)

@admin_bp.route("/comments/delete/<int:comment_id>", methods=["POST"])
@login_required
@admin_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    # db.session.delete(comment)
    # db.session.commit()
    flash("Comentário excluído com sucesso! (Placeholder)", "success")
    return redirect(url_for("admin.manage_comments"))

