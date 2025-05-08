# models/comment.py
from datetime import datetime
from ..extensions import db # Importando db de extensions.py

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    
    # Para respostas a comentários (comentários aninhados)
    parent_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=True)
    replies = db.relationship("Comment", backref=db.backref("parent", remote_side=[id]), lazy="dynamic")

    def __repr__(self):
        return f"<Comment {self.id} by User {self.user_id} on Project {self.project_id}>"

