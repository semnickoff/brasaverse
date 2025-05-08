# src/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models.user import User # Supondo que User está em models.user

class RegistrationForm(FlaskForm):
    username = StringField("Nome de Usuário", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo("password")])
    profile_image = FileField("Imagem de Perfil (Opcional)") # Adicionar validadores de arquivo se necessário
    submit = SubmitField("Cadastrar")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Este nome de usuário já está em uso. Por favor, escolha outro.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Este email já está em uso. Por favor, escolha outro.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    remember = BooleanField("Lembrar-me")
    submit = SubmitField("Login")

