from flask import current_app as ca

from flask_security import UserMixin

roles_users = ca.db.Table(
    "roles_users",
    ca.db.Column("user_id", ca.db.Integer(), ca.db.ForeignKey("user.id")),
    ca.db.Column("role_id", ca.db.Integer(), ca.db.ForeignKey("role.id")),
)


class User(UserMixin, db.Model):
    id = ca.db.Column(ca.db.Integer, primary_key=True)
    email = ca.db.Column(ca.db.String(255), unique=True)
    password = ca.db.Column(ca.db.String(255))
    active = ca.db.Column(ca.db.Boolean())
    roles = ca.db.relationship(
        "Role",
        secondary=roles_users,
        backref=ca.db.backref("users", lazy="dynamic"),
    )
