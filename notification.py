# models/notification.py
from datetime import datetime
from ..extensions import db # Importando db de extensions.py

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) # O destinatário da notificação
    # Tipos de notificação podem ser: 'new_like', 'new_comment_reply', 'project_update', 'new_contact_message_admin'
    notification_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    link_related = db.Column(db.String(255), nullable=True) # Link para o projeto, comentário, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    # Relacionamento (opcional, se quisermos buscar o usuário diretamente da notificação)
    # user = db.relationship('User', backref=db.backref('user_notifications', lazy=True))

    def __repr__(self):
        return f"<Notification {self.id} for User {self.user_id} - Type: {self.notification_type}>"

