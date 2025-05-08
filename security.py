# src/security.py
from flask import request, abort
from functools import wraps
from flask_login import current_user

# Função para limpar e validar dados de entrada
def sanitize_input(data):
    # Implementar lógica de sanitização e validação aqui
    # Exemplo: remover tags HTML, validar tipos de dados, etc.
    return data

# Decorador para proteger rotas que exigem login
def login_required_custom(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.url))
        return func(*args, **kwargs)
    return decorated_view

# Decorador para proteger rotas que exigem papel de administrador
def admin_required_custom(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)  # Acesso proibido
        return func(*args, **kwargs)
    return decorated_view

# Outras funções de segurança podem ser adicionadas aqui, como:
# - Validação de senhas fortes
# - Proteção contra ataques de força bruta
# - Configuração de cabeçalhos de segurança HTTP
# - Logging de atividades suspeitas

# Exemplo de uso de um decorador de segurança (simulado):
# @app.route('/admin/dashboard')
# @login_required_custom
# @admin_required_custom
# def admin_dashboard():
#     # Lógica da rota protegida
#     return "Painel Administrativo"

