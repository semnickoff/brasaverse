# models/like.py
from datetime import datetime
from ..extensions import db # Importando db de extensions.py

class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Unique constraint to prevent a user from liking a project more than once
    __table_args__ = (db.UniqueConstraint("user_id", "project_id", name="_user_project_uc"),)

    def __repr__(self):
        return f"<Like by User {self.user_id} on Project {self.project_id}>"

