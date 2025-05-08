from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import db, Project, Comment, ContactMessage
from ..forms import ProjectForm, CommentForm, ContactForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    # Lógica para exibir a página inicial
    return render_template('home.html', title='Início')

@main_bp.route('/about')
def about():
    # Lógica para exibir a página "Sobre"
    return render_template('about.html', title='Sobre Mim')

@main_bp.route('/projects')
def list_projects():
    # Lógica para listar projetos
    projects = Project.query.all() # Exemplo, ajuste conforme necessário
    return render_template('projects.html', projects=projects, title='Projetos')

@main_bp.route('/project/<int:project_id>', methods=['GET', 'POST'])
@login_required # Exemplo de proteção de rota
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, user_id=current_user.id, project_id=project.id)
        db.session.add(comment)
        db.session.commit()
        flash('Seu comentário foi adicionado!', 'success')
        return redirect(url_for('main.project_detail', project_id=project.id))
    comments = Comment.query.filter_by(project_id=project.id).order_by(Comment.timestamp.desc()).all()
    return render_template('project_detail.html', project=project, comments=comments, form=form)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Lógica para processar o formulário de contato
        msg = ContactMessage(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Sua mensagem foi enviada com sucesso!', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', title='Contato', form=form)

