# src/routes/admin/notifications.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ...models import db, Notification

notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")

@notifications_bp.route("/")
@login_required
def list_notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template("notifications/list.html", notifications=notifications)

@notifications_bp.route("/mark_as_read/<int:notification_id>", methods=["POST"])
@login_required
def mark_as_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id == current_user.id:
        notification.is_read = True
        db.session.commit()
        flash("Notificação marcada como lida.", "success")
    else:
        flash("Você não tem permissão para marcar esta notificação como lida.", "danger")
    return redirect(url_for("notifications.list_notifications"))

@notifications_bp.route("/mark_all_as_read", methods=["POST"])
@login_required
def mark_all_as_read():
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).all()
    for notification in notifications:
        notification.is_read = True
    db.session.commit()
    flash("Todas as notificações foram marcadas como lidas.", "success")
    return redirect(url_for("notifications.list_notifications"))

